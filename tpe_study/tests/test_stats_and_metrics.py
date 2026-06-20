"""Тесты метрик и статистики: монотонность best-so-far, шаги до порога,
корректность поправки Холма и парного теста на синтетике."""
import numpy as np
import pandas as pd

from tpe_study.functions import BENCHMARKS
from tpe_study.metrics import best_so_far_curves, steps_to_threshold
from tpe_study.stats import holm_correction, paired_significance_vs_baseline


def test_best_so_far_monotone():
    b = BENCHMARKS["Sphere"]
    x_hist = np.array([[3, 3], [1, 1], [2, 2], [0.1, 0.1]], dtype=float)
    y_obs = np.array([b.f(x) for x in x_hist])
    dist_y, dist_x = best_so_far_curves(x_hist, y_obs, b)
    assert np.all(np.diff(dist_y) <= 1e-12)        # не возрастает
    assert np.all(np.diff(dist_x) <= 1e-12)


def test_steps_to_threshold():
    assert steps_to_threshold(np.array([5.0, 2.0, 0.4, 0.1]), 0.5) == 3
    assert steps_to_threshold(np.array([5.0, 2.0, 1.0]), 0.5) is None


def test_holm_monotone_and_bounded():
    adj, rej = holm_correction([0.01, 0.04, 0.03], alpha=0.05)
    assert np.all(adj <= 1.0) and np.all(adj >= 0.0)
    # самый маленький p домножается на m=3
    assert abs(adj[0] - 0.03) < 1e-9


def test_paired_significance_detects_clear_difference():
    rng = np.random.default_rng(0)
    rows = []
    for s in range(20):
        rows.append(dict(function="F", scale="raw", data="clean", algorithm="tpe",
                         seed=s, final_dist_y=1.0 + rng.normal(0, 0.01), final_dist_x=0, steps=None))
        rows.append(dict(function="F", scale="raw", data="clean", algorithm="tpe_gp",
                         seed=s, final_dist_y=0.5 + rng.normal(0, 0.01), final_dist_x=0, steps=None))
    sig = paired_significance_vs_baseline(pd.DataFrame(rows))
    r = sig[sig.algorithm == "tpe_gp"].iloc[0]
    assert r["direction"] == "better" and bool(r["significant_holm"])


def test_bh_correction_and_robust_detects_clear_diff():
    import numpy as np, pandas as pd
    from tpe_study.stats_robust import bh_correction, robust_significance
    adj, rej = bh_correction([0.001, 0.5, 0.9])
    assert adj[0] <= adj[1] <= adj[2] and adj[0] < 0.05
    rng = np.random.default_rng(0); rows = []
    for s in range(30):
        rows.append(dict(function="F", scale="raw", data="clean", algorithm="tpe",
                         seed=s, final_dist_y=1.0 + rng.normal(0, 0.02), final_dist_x=0.0))
        rows.append(dict(function="F", scale="raw", data="clean", algorithm="tpe_gp",
                         seed=s, final_dist_y=0.5 + rng.normal(0, 0.02), final_dist_x=0.0))
    det, summ = robust_significance(pd.DataFrame(rows), metrics=("final_dist_y",))
    r = det[(det.algorithm == "tpe_gp") & (det.metric == "final_dist_y")].iloc[0]
    assert r["median_delta"] < 0 and r["p_wilcoxon"] < 0.05 and bool(r["wilcoxon_bh_sig"])
