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
