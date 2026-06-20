"""
Статистические тесты значимости различий между алгоритмами.

Зачем: средние («algo лучше tpe») сами по себе не доказывают эффект — нужен тест значимости.
Так как все алгоритмы при данном seed видят ОДИН и тот же шум (common random numbers),
сравнение ПАРНОЕ по seed -> используем парный критерий Уилкоксона (Wilcoxon signed-rank).

Множественные сравнения (много пар algo×ячейка) -> поправка Холма (Holm-Bonferroni),
контролирующая FWER, чтобы не «выловить» значимость случайно.

Интерпретация колонок significance_tests.csv:
  median_delta  = медиана (algo - tpe) по seeds; <0 -> модификация лучше (меньше ошибка);
  p_value       = сырой p парного Уилкоксона;
  p_holm        = p после поправки Холма;
  significant_holm = p_holm < alpha;
  direction     = 'better'/'worse'/'tie' по знаку median_delta.
"""
from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon


def holm_correction(pvals: List[float], alpha: float = 0.05):
    """Поправка Холма. Возвращает (adjusted_p, reject) в исходном порядке."""
    p = np.asarray(pvals, dtype=float)
    m = len(p)
    order = np.argsort(p)
    adj = np.empty(m)
    running = 0.0
    for rank, idx in enumerate(order):
        val = (m - rank) * p[idx]
        running = max(running, val)         # монотонность по Холму
        adj[idx] = min(running, 1.0)
    return adj, adj < alpha


def paired_significance_vs_baseline(per_seed: pd.DataFrame, metric: str = "final_dist_y",
                                    baseline: str = "tpe", alpha: float = 0.05) -> pd.DataFrame:
    """
    Для каждой ячейки (function, scale, data) сравниваем каждый algo != baseline с baseline
    парным Уилкоксоном по seeds на метрике `metric`. Затем общая поправка Холма по всем тестам.
    """
    rows = []
    for (fn, sc, dt), g in per_seed.groupby(["function", "scale", "data"]):
        base = g[g["algorithm"] == baseline].set_index("seed")[metric]
        if base.empty:
            continue
        for algo in sorted(g["algorithm"].unique()):
            if algo == baseline:
                continue
            cur = g[g["algorithm"] == algo].set_index("seed")[metric]
            common = base.index.intersection(cur.index)
            b = base.loc[common].to_numpy()
            a = cur.loc[common].to_numpy()
            diff = a - b
            median_delta = float(np.median(diff))
            if np.allclose(diff, 0.0):
                p = 1.0                       # идентичны (напр. инвариантность нормализации)
            else:
                try:
                    p = float(wilcoxon(a, b, zero_method="wilcox").pvalue)
                except ValueError:
                    p = 1.0
            direction = "tie" if abs(median_delta) < 1e-12 else ("better" if median_delta < 0 else "worse")
            rows.append({"function": fn, "scale": sc, "data": dt, "algorithm": algo,
                         "n_pairs": int(len(common)), "median_delta": median_delta,
                         "p_value": p, "direction": direction})

    res = pd.DataFrame(rows)
    if len(res):
        adj, rej = holm_correction(res["p_value"].tolist(), alpha=alpha)
        res["p_holm"] = adj
        res["significant_holm"] = rej
        res["significant_and_better"] = rej & (res["direction"] == "better")
    return res
