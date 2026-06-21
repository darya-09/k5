#!/usr/bin/env python3
"""
ABLATION МОЕЙ МОДИФИКАЦИИ БАЗЫ TPE: prior-компонента + адаптивная ширина ядра.

Базовый TPE здесь = моя переработка сэмплера (prior + magic-clip bandwidth). Чтобы
ДОКАЗАТЬ, что оба компонента нужны, отключаем их по одному и оба сразу и сравниваем
качество (final_dist_y по raw clean) парным Уилкоксоном vs полный вариант.

Это ФОКУСНЫЙ быстрый прогон (не полная сетка из run.py): 4 функции × {clean, noisy_y},
scale=raw, несколько seeds. Пишет results/tables/ablation_base_tpe.csv.

Запуск:  PYTHONHASHSEED=0 python ablation_base.py
"""
from __future__ import annotations
import json, sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from tpe_study.functions import BENCHMARKS                       # noqa: E402
from tpe_study.objective import build_objective                  # noqa: E402
from tpe_study.metrics import best_so_far_curves, steps_to_threshold  # noqa: E402
from tpe_study.experiment import THRESHOLDS                      # noqa: E402
from tpe_study.stats import paired_significance_vs_baseline      # noqa: E402
from tpe_study.tpe import TPE                                    # noqa: E402

# Варианты базы: full = моя модификация; остальные — её «увечья» (lesions).
VARIANTS = {
    "base_full":  dict(use_prior=True,  adaptive_bandwidth=True),   # моя модификация (контроль)
    "no_prior":   dict(use_prior=False, adaptive_bandwidth=True),   # без prior-компоненты
    "fixed_bw":   dict(use_prior=True,  adaptive_bandwidth=False),  # фикс. ширина (Сильверман)
    "naive_kde":  dict(use_prior=False, adaptive_bandwidth=False),  # оба выключены
}


def main():
    cfg = json.load(open(ROOT / "configs" / "default.json"))
    n_seeds = min(int(cfg["seeds"]), 20)        # фокусно и быстро
    seeds = list(range(n_seeds))
    rows = []
    for name, bench in BENCHMARKS.items():
        f_max = bench.estimate_fmax()
        for data in ("clean", "noisy_y"):
            for variant, flags in VARIANTS.items():
                for s in seeds:
                    obj = build_objective(bench, "raw", data, s, f_max)
                    opt = TPE(bounds=bench.bounds, n_init=cfg["n_init"], gamma=cfg["gamma"],
                              n_candidates=cfg["n_candidates"], min_bw_frac=cfg["min_bw_frac"],
                              seed=s, **flags)
                    res = opt.optimize(obj, cfg["max_evals"])
                    dy, _ = best_so_far_curves(res["x_history"], res["y_history"], bench)
                    rows.append({"function": name, "scale": "raw", "data": data,
                                 "algorithm": variant, "seed": s,
                                 "final_dist_y": float(dy[-1]),
                                 "reached": steps_to_threshold(dy, THRESHOLDS[name]) is not None})
    per_seed = pd.DataFrame(rows)

    # Сводка по ячейкам: медиана final_dist_y и success% каждого варианта.
    summ = (per_seed.groupby(["function", "data", "algorithm"])
            .agg(median_dist_y=("final_dist_y", "median"),
                 mean_dist_y=("final_dist_y", "mean"),
                 success_pct=("reached", lambda x: 100.0 * x.mean()))
            .reset_index())

    # Парный Уилкоксон: каждый lesion vs base_full (меньше final_dist_y = лучше).
    sig = paired_significance_vs_baseline(per_seed, metric="final_dist_y",
                                          baseline="base_full", alpha=0.05)

    # Собираем читаемую таблицу: base vs lesion по ячейкам с p_holm.
    base = summ[summ.algorithm == "base_full"].set_index(["function", "data"])["median_dist_y"]
    out = []
    for _, r in sig.iterrows():
        key = (r["function"], r["data"])
        b = float(base.loc[key])
        a = float(summ[(summ.function == r["function"]) & (summ.data == r["data"]) &
                       (summ.algorithm == r["algorithm"])]["median_dist_y"].iloc[0])
        worse_pct = 100.0 * (a - b) / b if b > 1e-12 else float("nan")
        out.append({"function": r["function"], "data": r["data"], "lesion": r["algorithm"],
                    "base_median_dist_y": b, "lesion_median_dist_y": a,
                    "lesion_worse_by_%": worse_pct, "p_holm": float(r["p_holm"]),
                    "significant_worse": bool(r["significant_holm"] and r["direction"] == "worse")})
    detail = pd.DataFrame(out).sort_values(["function", "data", "lesion"]).reset_index(drop=True)

    tables = ROOT / "results" / "tables"
    detail.to_csv(tables / "ablation_base_tpe.csv", index=False)
    summ.to_csv(tables / "ablation_base_tpe_cells.csv", index=False)

    n_cells = detail.groupby("lesion").size().iloc[0] if len(detail) else 0
    print(f"seeds={n_seeds}, ячеек на lesion={n_cells}")
    print("\n=== Сколько ячеек, где отключение компонента ЗНАЧИМО ухудшает базу ===")
    print(detail.groupby("lesion")["significant_worse"].sum().to_string())
    print("\n=== Медианное ухудшение (%) при отключении ===")
    print(detail.groupby("lesion")["lesion_worse_by_%"].median().round(1).to_string())
    print("\nЗаписано: results/tables/ablation_base_tpe.csv (+ _cells.csv)")


if __name__ == "__main__":
    main()
