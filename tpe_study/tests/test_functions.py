"""Тесты benchmark-функций: аналитические градиенты совпадают с конечными разностями,
а минимумы действительно минимумы."""
import numpy as np
import pytest

from tpe_study.functions import make_benchmarks


def finite_diff(f, x, eps=1e-6):
    g = np.zeros_like(x)
    for i in range(len(x)):
        xp = x.copy(); xp[i] += eps
        xm = x.copy(); xm[i] -= eps
        g[i] = (f(xp) - f(xm)) / (2 * eps)
    return g


@pytest.mark.parametrize("bench", make_benchmarks(), ids=lambda b: b.name)
def test_gradient_matches_finite_difference(bench):
    rng = np.random.default_rng(0)
    for _ in range(5):
        x = np.array([rng.uniform(lo, hi) for lo, hi in bench.bounds])
        g_analytic = bench.grad(x)
        g_fd = finite_diff(bench.f, x)
        assert np.allclose(g_analytic, g_fd, atol=1e-3, rtol=1e-3), bench.name


@pytest.mark.parametrize("bench", make_benchmarks(), ids=lambda b: b.name)
def test_minimum_is_a_minimum(bench):
    f_star = bench.f(bench.x_star)
    assert abs(f_star - bench.f_star) < 1e-6
    rng = np.random.default_rng(1)
    for _ in range(20):
        x = np.array([rng.uniform(lo, hi) for lo, hi in bench.bounds])
        assert bench.f(x) >= f_star - 1e-9
