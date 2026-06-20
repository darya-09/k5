#!/usr/bin/env python3
"""
Главный запуск всех экспериментов.

Порядок:
  1) читаем конфиг (configs/default.json или путь из --config);
  2) фиксируем PYTHONHASHSEED и seeds -> детерминизм;
  3) идём по сетке функция × scale × data × algorithm × seed;
  4) считаем метрики по RAW CLEAN функции;
  5) пишем таблицы в results/tables/ и графики в results/figures/.

Запуск:
    PYTHONHASHSEED=0 python run.py
    PYTHONHASHSEED=0 python run.py --config configs/default.json
    PYTHONHASHSEED=0 python run.py --quick           # быстрый прогон (мало seeds)
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from tpe_study.experiment import ALGORITHMS, THRESHOLDS, run_cell     # noqa: E402
from tpe_study.functions import BENCHMARKS                            # noqa: E402
from tpe_study.metrics import steps_to_threshold                      # noqa: E402
from tpe_study.stats import paired_significance_vs_baseline           # noqa: E402
from tpe_study.stats_robust import robust_significance                 # noqa: E402
from tpe_study import plots                                           # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "configs" / "default.json"))
    ap.add_argument("--quick", action="store_true", help="мало seeds/итераций для проверки")
    ap.add_argument("--no-figures", action="store_true")
    args = ap.parse_args()

    cfg = json.load(open(args.config))
    if args.quick:
        cfg.update(seeds=3, max_evals=40)
    if args.no_figures:
        cfg["make_figures"] = False

    seeds = list(range(cfg["seeds"]))
    tables = ROOT / "results" / "tables"; tables.mkdir(parents=True, exist_ok=True)
    figs = ROOT / "results" / "figures"; figs.mkdir(parents=True, exist_ok=True)

    # f_max для нормализации — детерминированно по каждой функции (один раз).
    f_max = {name: BENCHMARKS[name].estimate_fmax() for name in cfg["functions"]}

    rows = []
    per_seed = []                     # по-seed финальные значения -> нужны для парных стат-тестов
    t0 = time.time()
    for fname in cfg["functions"]:
        bench = BENCHMARKS[fname]
        thr = THRESHOLDS[fname]
        for scale in cfg["scales"]:
            for data in cfg["data_types"]:
                curves_by_algo = {}
                for algo in cfg["algorithms"]:
                    row, curves = run_cell(bench, scale, data, algo, seeds, cfg, f_max[fname])
                    rows.append(row)
                    curves_by_algo[algo] = curves
                    for c in curves:          # сохраняем финал каждого seed
                        per_seed.append({
                            "function": fname, "scale": scale, "data": data,
                            "algorithm": algo, "seed": c["seed"],
                            "final_dist_y": float(c["dist_y"][-1]),
                            "final_dist_x": float(c["dist_x"][-1]),
                            "steps": steps_to_threshold(c["dist_y"], thr),
                        })
                    print(f"[{time.time()-t0:6.1f}s] {fname:11s} {scale:4s} {data:8s} "
                          f"{algo:13s} success={row['success_rate_%']:5.1f}% "
                          f"final_dist_y={row['final_dist_y_mean']:.4g}")
                if cfg.get("make_figures", True):
                    tag = f"{fname}_{scale}_{data}"
                    plots.plot_convergence(bench, scale, data, curves_by_algo,
                                           figs / f"conv_{tag}.png")
                    plots.plot_choice_map(bench, scale, data, curves_by_algo,
                                          figs / f"map_{tag}.png")

    df = pd.DataFrame(rows)
    df.to_csv(tables / "all_results.csv", index=False)

    per_seed_df = pd.DataFrame(per_seed)
    per_seed_df.to_csv(tables / "per_seed_final.csv", index=False)

    # Удобная сводка: только ключевые метрики.
    key = df[["function", "scale", "data", "algorithm", "success_rate_%",
              "steps_mean", "final_dist_y_mean", "final_dist_x_mean"]]
    key.to_csv(tables / "summary_key_metrics.csv", index=False)

    # Ablation-таблица: каждая модификация против baseline `tpe` при тех же (function,scale,data).
    abl = _ablation(df)
    abl.to_csv(tables / "ablation_vs_tpe.csv", index=False)

    # СТАТ-ТЕСТЫ значимости (парный Уилкоксон vs baseline `tpe` + поправка Холма).
    sig = paired_significance_vs_baseline(per_seed_df, metric="final_dist_y", baseline="tpe")
    sig.to_csv(tables / "significance_tests.csv", index=False)
    n_sig = int(sig["significant_holm"].sum()) if len(sig) else 0
    print(f"Стат-тестов: {len(sig)}, значимых (Holm, p<0.05): {n_sig}")

    # РОБАСТНОСТЬ к выбору теста: 4 теста × 3 поправки × 2 метрики.
    det, robust_summary = robust_significance(per_seed_df, baseline="tpe")
    det.to_csv(tables / "significance_robust.csv", index=False)
    robust_summary.to_csv(tables / "significance_robust_summary.csv", index=False)
    print(f"Робастных тестов посчитано: {len(det)} строк.")

    print(f"\nГotovo за {time.time()-t0:.1f}s. Строк: {len(df)}.")
    print("Таблицы:", tables)
    print("Графики:", figs)


def _ablation(df: pd.DataFrame) -> pd.DataFrame:
    out = []
    for (fn, sc, dt), g in df.groupby(["function", "scale", "data"]):
        base = g[g["algorithm"] == "tpe"]
        if base.empty:
            continue
        b = base.iloc[0]
        for algo in [a for a in g["algorithm"].unique() if a != "tpe"]:
            r = g[g["algorithm"] == algo]
            if r.empty:
                continue
            r = r.iloc[0]
            out.append({
                "function": fn, "scale": sc, "data": dt, "algorithm": algo,
                "tpe_final_dist_y": b["final_dist_y_mean"],
                "algo_final_dist_y": r["final_dist_y_mean"],
                "delta_dist_y(algo-tpe)": r["final_dist_y_mean"] - b["final_dist_y_mean"],
                "better_than_tpe": bool(r["final_dist_y_mean"] < b["final_dist_y_mean"]),
                "tpe_success_%": b["success_rate_%"],
                "algo_success_%": r["success_rate_%"],
            })
    return pd.DataFrame(out)


if __name__ == "__main__":
    main()
