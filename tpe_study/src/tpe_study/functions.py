"""
benchmark-функции для оптимизации (2D) + аналитические градиенты.

Почему так:
- Все функции имеют ИЗВЕСТНЫЙ глобальный минимум -> можно честно мерить качество
  и по значению (dist_y), и по аргументу (dist_x).
- Градиенты заданы аналитически и возвращаются В ТОЙ ЖЕ точке, что и значение,
  что критично для корректного градиентного взвешивания (в отличие от исходных
  ноутбуков, где градиент случайно считался в точке (mean(x0,x1), 0)).

Единица интерфейса — dataclass `Benchmark`: имя, f(x), grad(x), bounds, x*.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Tuple

import numpy as np

Array = np.ndarray


# --------------------------------------------------------------------------- #
# Сами функции и их аналитические градиенты (2D, но формулы общие по размерности)
# --------------------------------------------------------------------------- #
def sphere(x: Array) -> float:
    x = np.asarray(x, dtype=float)
    return float(np.sum(x ** 2))


def sphere_grad(x: Array) -> Array:
    x = np.asarray(x, dtype=float)
    return 2.0 * x


def rosenbrock(x: Array) -> float:
    x = np.asarray(x, dtype=float)
    return float(np.sum(100.0 * (x[1:] - x[:-1] ** 2) ** 2 + (1.0 - x[:-1]) ** 2))


def rosenbrock_grad(x: Array) -> Array:
    x = np.asarray(x, dtype=float)
    g = np.zeros_like(x)
    g[:-1] += -400.0 * x[:-1] * (x[1:] - x[:-1] ** 2) - 2.0 * (1.0 - x[:-1])
    g[1:] += 200.0 * (x[1:] - x[:-1] ** 2)
    return g


def rastrigin(x: Array) -> float:
    x = np.asarray(x, dtype=float)
    d = len(x)
    return float(10.0 * d + np.sum(x ** 2 - 10.0 * np.cos(2.0 * np.pi * x)))


def rastrigin_grad(x: Array) -> Array:
    x = np.asarray(x, dtype=float)
    return 2.0 * x + 20.0 * np.pi * np.sin(2.0 * np.pi * x)


def ackley(x: Array) -> float:
    x = np.asarray(x, dtype=float)
    d = len(x)
    a, b, c = 20.0, 0.2, 2.0 * np.pi
    s1 = np.sum(x ** 2)
    s2 = np.sum(np.cos(c * x))
    return float(-a * np.exp(-b * np.sqrt(s1 / d)) - np.exp(s2 / d) + a + np.e)


def ackley_grad(x: Array) -> Array:
    x = np.asarray(x, dtype=float)
    d = len(x)
    a, b, c = 20.0, 0.2, 2.0 * np.pi
    s1 = np.sum(x ** 2)
    s2 = np.sum(np.cos(c * x))
    if s1 <= 1e-14:
        t1 = np.zeros_like(x)
    else:
        r = np.sqrt(s1 / d)
        t1 = a * b * np.exp(-b * r) * x / (d * r)
    t2 = np.exp(s2 / d) * (c / d) * np.sin(c * x)
    return t1 + t2


# --------------------------------------------------------------------------- #
# Описание задачи
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Benchmark:
    name: str
    f: Callable[[Array], float]
    grad: Callable[[Array], Array]
    bounds: Tuple[Tuple[float, float], ...]
    x_star: Array            # точка глобального минимума
    f_star: float            # значение в минимуме (обычно 0)

    @property
    def dim(self) -> int:
        return len(self.bounds)

    def estimate_fmax(self, n_samples: int = 50_000, seed: int = 123) -> float:
        """Оценка максимума на bounds (для нормализации). Фиксированный seed -> детерминизм."""
        rng = np.random.default_rng(seed)
        lo = np.array([b[0] for b in self.bounds])
        hi = np.array([b[1] for b in self.bounds])
        X = rng.uniform(lo, hi, size=(n_samples, self.dim))
        return float(max(self.f(x) for x in X))


def make_benchmarks() -> List[Benchmark]:
    """Единый источник правды по набору функций (имена, bounds, минимумы)."""
    return [
        Benchmark("Sphere",     sphere,     sphere_grad,
                  ((-5.0, 5.0), (-5.0, 5.0)),     np.array([0.0, 0.0]), 0.0),
        Benchmark("Rosenbrock", rosenbrock, rosenbrock_grad,
                  ((-2.0, 2.0), (-1.0, 3.0)),     np.array([1.0, 1.0]), 0.0),
        Benchmark("Rastrigin",  rastrigin,  rastrigin_grad,
                  ((-5.12, 5.12), (-5.12, 5.12)), np.array([0.0, 0.0]), 0.0),
        Benchmark("Ackley",     ackley,     ackley_grad,
                  ((-5.0, 5.0), (-5.0, 5.0)),     np.array([0.0, 0.0]), 0.0),
    ]


BENCHMARKS = {b.name: b for b in make_benchmarks()}
