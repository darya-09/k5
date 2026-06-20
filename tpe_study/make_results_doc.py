#!/usr/bin/env python3
"""
Генерирует docs/RESULTS.md из реальных CSV в results/tables.
Все числа берутся из прогона run.py (ничего не выдумывается).
Также собирает все таблицы в results/tables/all_results.xlsx (если есть openpyxl).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
T = ROOT / "results" / "tables"
F = ROOT / "results" / "figures"


def md_table(df: pd.DataFrame, floatfmt="{:.4g}") -> str:
    df = df.copy()
    for c in df.columns:
        if pd.api.types.is_float_dtype(df[c]):
            df[c] = df[c].map(lambda v: "" if pd.isna(v) else floatfmt.format(v))
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(out)


def main():
    df = pd.read_csv(T / "all_results.csv")
    summ = pd.read_csv(T / "summary_key_metrics.csv")
    abl = pd.read_csv(T / "ablation_vs_tpe.csv")
    cfg = json.load(open(ROOT / "configs" / "default.json"))

    # Авто-выводы из реальных чисел -------------------------------------------
    # 1) Инвариантность нормализации для rank-based: tpe raw vs norm на clean.
    inv_rows = []
    for fn in df["function"].unique():
        for algo in ["tpe", "tpe_gradw"]:
            r = df[(df.function == fn) & (df.algorithm == algo) & (df.data == "clean")]
            raw = r[r.scale == "raw"]; norm = r[r.scale == "norm"]
            if len(raw) and len(norm):
                d = abs(float(raw.final_dist_y_mean.iloc[0]) - float(norm.final_dist_y_mean.iloc[0]))
                inv_rows.append((fn, algo, d))
    max_inv_gap = max((d for *_, d in inv_rows), default=float("nan"))

    # 2) Сколько раз модификация лучше baseline tpe (по final_dist_y).
    win = abl.groupby("algorithm")["better_than_tpe"].mean().mul(100).round(1)

    # 3) tpe vs random / optuna: средний success.
    succ = summ.groupby("algorithm")["success_rate_%"].mean().round(1)

    lines = []
    lines.append("# RESULTS — табличные результаты и графики\n")
    lines.append("> Сгенерировано автоматически из `results/tables/*.csv` (реальный прогон `run.py`).\n")
    lines.append("## Конфигурация прогона\n")
    lines.append("```json")
    lines.append(json.dumps({k: cfg[k] for k in
                 ["seeds", "n_init", "max_evals", "n_candidates", "gamma",
                  "functions", "scales", "data_types", "algorithms"]}, ensure_ascii=False, indent=2))
    lines.append("```\n")

    lines.append("## Сводка: средний success_rate по алгоритмам (по всем ячейкам)\n")
    lines.append(md_table(succ.reset_index().rename(columns={"success_rate_%": "avg_success_%"})))
    lines.append("")

    lines.append("## Авто-выводы (из чисел этого прогона)\n")
    lines.append(f"- **Инвариантность нормализации** (rank-based TPE, clean): максимальный разрыв "
                 f"|raw − norm| по final_dist_y = **{max_inv_gap:.3g}** "
                 f"(чем ближе к 0, тем полнее подтверждается инвариантность).")
    lines.append("- **Как часто модификация бьёт baseline `tpe`** (доля ячеек, % по final_dist_y):")
    for a, v in win.items():
        lines.append(f"  - `{a}`: {v}%")
    lines.append("")

    lines.append("## Ablation: каждая модификация против baseline `tpe`\n")
    lines.append("Δ = algo − tpe по final_dist_y (меньше нуля → модификация лучше).\n")
    lines.append(md_table(abl))
    lines.append("")

    lines.append("## Ключевые метрики (все ячейки)\n")
    lines.append(md_table(summ))
    lines.append("")

    lines.append("## Полная таблица (все метрики, все ячейки)\n")
    full_cols = ["function", "scale", "data", "algorithm", "success_rate_%",
                 "steps_mean", "steps_std", "final_dist_y_mean", "final_dist_y_std",
                 "final_dist_y_median", "final_dist_x_mean", "final_dist_x_std"]
    lines.append(md_table(df[full_cols]))
    lines.append("")

    lines.append("## Графики\n")
    lines.append("Кривые сходимости (`conv_*`) и карты выбора точек (`map_*`) — в `results/figures/`.\n")
    for p in sorted(F.glob("*.png")):
        lines.append(f"- `figures/{p.name}`")
    lines.append("")

    (ROOT / "docs" / "RESULTS.md").write_text("\n".join(lines))
    print("wrote docs/RESULTS.md")

    # xlsx со всеми таблицами
    try:
        with pd.ExcelWriter(T / "all_results.xlsx") as xw:
            df.to_excel(xw, "all_results", index=False)
            summ.to_excel(xw, "summary", index=False)
            abl.to_excel(xw, "ablation_vs_tpe", index=False)
        print("wrote results/tables/all_results.xlsx")
    except Exception as e:
        print("xlsx skipped:", repr(e))


if __name__ == "__main__":
    main()
