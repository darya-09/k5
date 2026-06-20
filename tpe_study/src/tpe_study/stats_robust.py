"""
Робастность вывода к ВЫБОРУ статистического теста.

Идея: если «нет значимой разницы» — это не артефакт одного теста, то вывод должен сохраняться
для РАЗНЫХ тестов, метрик и поправок на множественность. Считаем для каждой пары
(модификация vs baseline `tpe`, ячейка) набор тестов и эффект-сайзов, затем сводим,
сколько значимых улучшений даёт каждый алгоритм при каждом сочетании (тест × поправка × метрика).

Тесты (все ПАРНЫЕ по seed, т.к. общие случайные числа):
  - wilcoxon  — критерий Уилкоксона знаковых рангов;
  - ttest     — парный t-критерий Стьюдента;
  - sign      — знаковый критерий (биномиальный на знаках разностей);
  - perm      — перестановочный тест (случайные смены знака разностей, two-sided).
Поправки: none / holm / bh (Benjamini–Hochberg, FDR).
Эффект-сайзы: median_delta (медиана algo−tpe), prob_better (доля seeds, где algo лучше),
              rank_biserial = prob_better − prob_worse.
"""
from __future__ import annotations
from typing import List
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon, ttest_rel, binomtest


def bh_correction(pvals: List[float], alpha: float = 0.05):
    p = np.asarray(pvals, float)
    m = len(p)
    order = np.argsort(p)
    adj = np.empty(m)
    prev = 1.0
    for rank in range(m - 1, -1, -1):
        idx = order[rank]
        val = p[idx] * m / (rank + 1)
        prev = min(prev, val)
        adj[idx] = min(prev, 1.0)
    return adj, adj < alpha


def holm_correction(pvals: List[float], alpha: float = 0.05):
    p = np.asarray(pvals, float)
    m = len(p)
    order = np.argsort(p)
    adj = np.empty(m)
    running = 0.0
    for rank, idx in enumerate(order):
        running = max(running, (m - rank) * p[idx])
        adj[idx] = min(running, 1.0)
    return adj, adj < alpha


def _perm_p(d: np.ndarray, n_perm: int = 5000, seed: int = 0) -> float:
    d = d[np.abs(d) > 0]
    if d.size == 0:
        return 1.0
    rng = np.random.default_rng(seed)
    obs = abs(d.mean())
    signs = rng.choice([-1.0, 1.0], size=(n_perm, d.size))
    perm_means = np.abs((signs * np.abs(d)).mean(axis=1))
    return float((np.sum(perm_means >= obs - 1e-15) + 1) / (n_perm + 1))


def _tests_for_diff(d: np.ndarray) -> dict:
    """Все тесты для вектора парных разностей d = algo - baseline (улучшение => d<0)."""
    nz = d[np.abs(d) > 1e-12]
    n = d.size
    n_better = int(np.sum(d < 0)); n_worse = int(np.sum(d > 0))
    # wilcoxon
    if nz.size == 0:
        p_w = 1.0
    else:
        try:
            p_w = float(wilcoxon(d, zero_method="wilcox").pvalue)
        except ValueError:
            p_w = 1.0
    # paired t
    p_t = float(ttest_rel(d, np.zeros_like(d)).pvalue) if np.std(d) > 0 else 1.0
    # sign test (binomial on better/worse among non-ties)
    k = n_better + n_worse
    p_s = float(binomtest(min(n_better, n_worse), k, 0.5).pvalue) if k > 0 else 1.0
    # permutation
    p_p = _perm_p(d)
    return {
        "median_delta": float(np.median(d)),
        "mean_delta": float(np.mean(d)),
        "prob_better": n_better / n,
        "rank_biserial": (n_better - n_worse) / n,
        "p_wilcoxon": p_w, "p_ttest": p_t, "p_sign": p_s, "p_perm": p_p,
    }


def robust_significance(per_seed: pd.DataFrame, baseline: str = "tpe",
                        metrics=("final_dist_y", "final_dist_x"), alpha: float = 0.05):
    """Возвращает (детальная таблица, сводка по тест×поправка×метрика)."""
    rows = []
    for metric in metrics:
        for (fn, sc, dt), g in per_seed.groupby(["function", "scale", "data"]):
            base = g[g.algorithm == baseline].set_index("seed")[metric]
            if base.empty:
                continue
            for algo in sorted(g.algorithm.unique()):
                if algo == baseline:
                    continue
                cur = g[g.algorithm == algo].set_index("seed")[metric]
                common = base.index.intersection(cur.index)
                d = (cur.loc[common] - base.loc[common]).to_numpy()
                rows.append({"metric": metric, "function": fn, "scale": sc, "data": dt,
                             "algorithm": algo, "n": len(common), **_tests_for_diff(d)})
    det = pd.DataFrame(rows)

    # Поправки применяем внутри семейства (одна метрика, один тест) по всем ячейкам×алгоритмам.
    test_cols = {"wilcoxon": "p_wilcoxon", "ttest": "p_ttest", "sign": "p_sign", "perm": "p_perm"}
    for metric in metrics:
        m = det.metric == metric
        for tname, col in test_cols.items():
            pv = det.loc[m, col].tolist()
            _, rej_holm = holm_correction(pv, alpha)
            _, rej_bh = bh_correction(pv, alpha)
            det.loc[m, f"{tname}_holm_sig"] = rej_holm
            det.loc[m, f"{tname}_bh_sig"] = rej_bh
            det.loc[m, f"{tname}_raw_sig"] = np.asarray(pv) < alpha

    # Сводка: число ЗНАЧИМЫХ УЛУЧШЕНИЙ (sig & median_delta<0) на алгоритм при каждом сочетании.
    better = det["median_delta"] < 0
    summ_rows = []
    for algo in sorted(det.algorithm.unique()):
        a = det.algorithm == algo
        row = {"algorithm": algo}
        for metric in metrics:
            for tname in test_cols:
                for corr in ["raw", "holm", "bh"]:
                    col = f"{tname}_{corr}_sig"
                    mask = a & (det.metric == metric) & det[col] & better
                    row[f"{metric}|{tname}|{corr}"] = int(mask.sum())
        summ_rows.append(row)
    summ = pd.DataFrame(summ_rows)
    return det, summ
