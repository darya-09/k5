"""Тесты ядра TPE: воспроизводимость, выход в границах, KDE-плотность,
превосходство над random, и СТРОГАЯ инвариантность нормализации для базового TPE."""
import numpy as np
import pytest

from tpe_study.functions import BENCHMARKS
from tpe_study.objective import build_objective
from tpe_study.tpe import TPE, WeightedKDE1D


def _obj(bench):
    return lambda x: (float(bench.f(x)), bench.grad(x))


def test_reproducible_same_seed():
    b = BENCHMARKS["Sphere"]
    r1 = TPE(bounds=b.bounds, seed=42).optimize(_obj(b), 40)
    r2 = TPE(bounds=b.bounds, seed=42).optimize(_obj(b), 40)
    assert np.allclose(r1["x_history"], r2["x_history"])
    assert r1["best_y"] == r2["best_y"]


def test_samples_within_bounds():
    b = BENCHMARKS["Rosenbrock"]
    res = TPE(bounds=b.bounds, seed=0).optimize(_obj(b), 60)
    for d, (lo, hi) in enumerate(b.bounds):
        assert res["x_history"][:, d].min() >= lo - 1e-9
        assert res["x_history"][:, d].max() <= hi + 1e-9


def test_kde_weights_normalized_and_bounds():
    kde = WeightedKDE1D(samples=np.array([-1.0, 0.5, 2.0]), lo=-5, hi=5)
    assert abs(kde.weights.sum() - 1.0) < 1e-12          # веса компонент нормированы
    assert kde.logpdf(-6.0) == -np.inf and kde.logpdf(6.0) == -np.inf   # вне границ
    assert np.isfinite(kde.logpdf(0.5))                   # внутри — конечно


def test_kde_denser_near_cluster():
    # Плотность выше там, где сосредоточены наблюдения.
    kde = WeightedKDE1D(samples=np.array([1.9, 2.0, 2.1]), lo=-5, hi=5, prior_weight=0.1)
    assert kde.logpdf(2.0) > kde.logpdf(-3.0)


def test_kde_sample_within_bounds():
    kde = WeightedKDE1D(samples=np.array([-1.0, 0.5, 2.0]), lo=-5, hi=5)
    rng = np.random.default_rng(0)
    xs = kde.sample_many(rng, 500)
    assert xs.min() >= -5 - 1e-9 and xs.max() <= 5 + 1e-9


def test_tpe_beats_random_on_sphere():
    b = BENCHMARKS["Sphere"]
    tpe_best, rnd_best = [], []
    for s in range(8):
        tpe_best.append(min(TPE(bounds=b.bounds, gamma=0.15, seed=s).optimize(_obj(b), 80)["y_history"]))
        rng = np.random.default_rng(s)
        rnd_best.append(min(b.f(np.array([rng.uniform(lo, hi) for lo, hi in b.bounds])) for _ in range(80)))
    assert np.mean(tpe_best) < np.mean(rnd_best)


@pytest.mark.parametrize("name", ["Sphere", "Rastrigin", "Ackley"])
def test_normalization_invariance_for_plain_tpe(name):
    """Базовый rank-based TPE на clean инвариантен к нормализации цели: raw == norm ТОЧНО."""
    b = BENCHMARKS[name]
    fmax = b.estimate_fmax()
    raw = TPE(bounds=b.bounds, gamma=0.15, seed=3).optimize(
        build_objective(b, "raw", "clean", 3, fmax), 50)
    norm = TPE(bounds=b.bounds, gamma=0.15, seed=3).optimize(
        build_objective(b, "norm", "clean", 3, fmax), 50)
    # одинаковая траектория по x (нормализация y не меняет ранги -> не меняет выбор)
    assert np.allclose(raw["x_history"], norm["x_history"], atol=1e-9)


def test_prior_keeps_exploration_in_tail():
    """prior-компонента держит ненулевую плотность вдали от схлопнувшегося кластера."""
    # При узких (фиксированных) ядрах без prior хвост схлопывается; prior держит плотность.
    s = np.array([2.00, 2.01, 1.99])           # очень плотный кластер «хороших»
    far = -3.0                                  # далеко от кластера
    no_prior = WeightedKDE1D(s, -5, 5, use_prior=False, adaptive_bandwidth=False)
    with_prior = WeightedKDE1D(s, -5, 5, use_prior=True, adaptive_bandwidth=False, prior_weight=1.0)
    assert with_prior.logpdf(far) > no_prior.logpdf(far)


def test_adaptive_bw_gives_narrow_kernel_in_dense_cluster():
    """Адаптивная ширина даёт более узкое ядро в плотной зоне, чем фиксированная (Сильверман)."""
    s = np.array([0.00, 0.02, 0.04, 4.5])
    adaptive = WeightedKDE1D(s, -5, 5, use_prior=False, adaptive_bandwidth=True)
    fixed = WeightedKDE1D(s, -5, 5, use_prior=False, adaptive_bandwidth=False)
    assert adaptive.bws.min() < fixed.bws.min()


def test_base_modification_beats_naive_kde_on_sphere():
    """Моя база (prior+адаптивная ширина) точнее «наивного» KDE (оба выключены) на Sphere."""
    b = BENCHMARKS["Sphere"]
    full, naive = [], []
    for s in range(6):
        full.append(min(TPE(bounds=b.bounds, seed=s).optimize(_obj(b), 80)["y_history"]))
        naive.append(min(TPE(bounds=b.bounds, seed=s, use_prior=False,
                             adaptive_bandwidth=False).optimize(_obj(b), 80)["y_history"]))
    assert np.mean(full) < np.mean(naive)


def test_refine_reduces_convex_objective():
    # Локальный градиентный refine должен снижать выпуклую функцию (Sphere) от стартовой точки.
    import numpy as np
    from tpe_study.tpe import TPE
    from tpe_study.functions import BENCHMARKS
    b = BENCHMARKS["Sphere"]
    opt = TPE(bounds=b.bounds, refine_steps=5, refine_step_size=0.5, refine_decay=0.8,
              grad_fn=b.grad, seed=0)
    x0 = np.array([3.0, -4.0])
    x1 = opt._refine(x0)
    assert b.f(x1) < b.f(x0)
    for d, (lo, hi) in enumerate(b.bounds):
        assert lo - 1e-9 <= x1[d] <= hi + 1e-9
