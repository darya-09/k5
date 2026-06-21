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

from tpe_study.experiment import ALGO_FAMILY, ALGORITHMS, THRESHOLDS, run_cell   # noqa: E402
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
    all_curves = {}                   # (fn,scale,data,algo) -> список кривых по seeds (для истории)
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
                    all_curves[(fname, scale, data, algo)] = curves
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

    # История по итерациям: среднее±std кривых dist_y/dist_x по seeds (для графиков и проверки).
    iter_rows = []
    for (fn, sc, dt, algo), curves in all_curves.items():
        Y = np.vstack([c["dist_y"] for c in curves])
        X = np.vstack([c["dist_x"] for c in curves])
        for it in range(Y.shape[1]):
            iter_rows.append({"function": fn, "scale": sc, "data": dt, "algorithm": algo,
                              "iteration": it + 1,
                              "dist_y_mean": float(Y[:, it].mean()), "dist_y_std": float(Y[:, it].std()),
                              "dist_x_mean": float(X[:, it].mean()), "dist_x_std": float(X[:, it].std())})
    pd.DataFrame(iter_rows).to_csv(tables / "iteration_history.csv", index=False)

    # Удобная сводка: только ключевые метрики.
    key = df[["function", "scale", "data", "algorithm", "success_rate_%",
              "steps_mean", "final_dist_y_mean", "final_dist_x_mean"]]
    key.to_csv(tables / "summary_key_metrics.csv", index=False)

    # Ablation-таблица: каждая модификация против baseline `tpe` при тех же (function,scale,data).
    abl = _ablation(df)
    abl.to_csv(tables / "ablation_vs_tpe.csv", index=False)

    # Сравнение raw vs norm (как df_compare в fin_3): delta(norm-raw) по функции/алгоритму/данным.
    _raw_vs_norm(df).to_csv(tables / "raw_vs_norm_comparison.csv", index=False)

    # СТАТ-ТЕСТЫ значимости (парный Уилкоксон vs baseline `tpe` + поправка Холма).
    sig = paired_significance_vs_baseline(per_seed_df, metric="final_dist_y", baseline="tpe")
    sig.to_csv(tables / "significance_tests.csv", index=False)
    n_sig = int(sig["significant_holm"].sum()) if len(sig) else 0
    print(f"Стат-тестов: {len(sig)}, значимых (Holm, p<0.05): {n_sig}")

    # ДО/ПОСЛЕ модификаций на ЗАШУМЛЁННЫХ функциях (фокусный срез data=noisy_y).
    nba_detail, nba_summary = noisy_before_after(per_seed_df, sig, baseline="tpe")
    nba_detail.to_csv(tables / "noisy_before_after.csv", index=False)
    nba_summary.to_csv(tables / "noisy_before_after_summary.csv", index=False)
    print(f"До/после на шуме: {len(nba_detail)} ячеек, "
          f"значимо лучше tpe: {int(nba_detail['significant_better'].sum())}.")

    # РОБАСТНОСТЬ к выбору теста: 4 теста × 3 поправки × 2 метрики.
    det, robust_summary = robust_significance(per_seed_df, baseline="tpe")
    det.to_csv(tables / "significance_robust.csv", index=False)
    robust_summary.to_csv(tables / "significance_robust_summary.csv", index=False)
    print(f"Робастных тестов посчитано: {len(det)} строк.")

    print(f"\nГotovo за {time.time()-t0:.1f}s. Строк: {len(df)}.")
    print("Таблицы:", tables)
    print("Графики:", figs)


def noisy_before_after(per_seed_df: pd.DataFrame, sig_df: pd.DataFrame,
                       baseline: str = "tpe") -> "tuple[pd.DataFrame, pd.DataFrame]":
    """До/после ЭФФЕКТА МОДИФИКАЦИЙ на ЗАШУМЛЁННЫХ функциях (data=noisy_y).

    «До»  = baseline `tpe` (без модификаций), «после» = каждая модификация — на тех же
    (функция, scale, seed) -> парное сравнение. Качество = final_dist_y по raw clean.
    Возвращает (детальную таблицу по ячейкам, сводку по алгоритмам).
    """
    d = per_seed_df[per_seed_df["data"] == "noisy_y"]

    def _agg(g):
        finals = g["final_dist_y"].astype(float)
        return pd.Series({
            "median_dist_y": float(finals.median()),
            "mean_dist_y": float(finals.mean()),
            "success_%": 100.0 * g["steps"].notna().sum() / len(g),
        })

    stats = d.groupby(["function", "scale", "algorithm"]).apply(_agg).reset_index()
    base = stats[stats.algorithm == baseline].set_index(["function", "scale"])
    sig = sig_df[sig_df.data == "noisy_y"].set_index(["function", "scale", "algorithm"])

    rows = []
    for _, r in stats[stats.algorithm != baseline].iterrows():
        key = (r["function"], r["scale"])
        if key not in base.index:
            continue
        b = base.loc[key]
        before, after = float(b["median_dist_y"]), float(r["median_dist_y"])
        improve = 100.0 * (before - after) / before if before > 1e-12 else float("nan")
        skey = (r["function"], r["scale"], r["algorithm"])
        s = sig.loc[skey] if skey in sig.index else None
        rows.append({
            "function": r["function"], "scale": r["scale"], "algorithm": r["algorithm"],
            "family": ALGO_FAMILY.get(r["algorithm"], ""),
            "tpe_median_dist_y": before, "algo_median_dist_y": after,
            "delta_median(algo-tpe)": after - before, "improve_%": improve,
            "tpe_success_%": float(b["success_%"]), "algo_success_%": float(r["success_%"]),
            "n_pairs": int(s["n_pairs"]) if s is not None else 0,
            "p_holm": float(s["p_holm"]) if s is not None else float("nan"),
            "significant_better": bool(s["significant_and_better"]) if s is not None else False,
        })
    detail = pd.DataFrame(rows).sort_values(["function", "scale", "algorithm"]).reset_index(drop=True)

    # Сводка по алгоритму: в скольких из 8 (функция×scale) ячеек он лучше/значимо лучше на шуме.
    summ = (detail.assign(better=detail["delta_median(algo-tpe)"] < 0)
            .groupby(["algorithm", "family"])
            .agg(cells_better_of_8=("better", "sum"),
                 cells_significant_better=("significant_better", "sum"),
                 mean_improve_pct=("improve_%", "mean"),
                 median_improve_pct=("improve_%", "median"))
            .reset_index().sort_values("cells_significant_better", ascending=False))
    return detail, summ


def _raw_vs_norm(df: pd.DataFrame) -> pd.DataFrame:
    """Side-by-side raw vs norm по final_dist_y (как df_compare в fin_3). delta = norm - raw."""
    out = []
    for (fn, algo, dt), g in df.groupby(["function", "algorithm", "data"]):
        raw = g[g.scale == "raw"]; norm = g[g.scale == "norm"]
        if raw.empty or norm.empty:
            continue
        r = float(raw.final_dist_y_mean.iloc[0]); n = float(norm.final_dist_y_mean.iloc[0])
        out.append({"function": fn, "algorithm": algo, "data": dt,
                    "raw_final_dist_y": r, "norm_final_dist_y": n,
                    "delta_norm_minus_raw": n - r,
                    "identical": bool(abs(n - r) < 1e-9)})
    return pd.DataFrame(out)


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
