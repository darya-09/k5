"""
Построение objective, который ВИДИТ оптимизатор, из чистой benchmark-функции.

Здесь собраны два фактора, которые мы варьируем как эксперименты:
  1) scale: 'raw' либо 'norm' (нормализация целевой функции в [0, 1]);
  2) data : 'clean' либо 'noisy_y' (гауссов шум в наблюдаемом значении).

ВАЖНЫЕ ПРИНЦИПЫ (чтобы сравнение было честным):
- Качество ВСЕГДА оценивается по raw clean функции (см. metrics.py), что бы ни видел
  оптимизатор. Поэтому здесь мы возвращаем и "наблюдаемое" значение, и истинные f/grad.
- Шум зависит ТОЛЬКО от (имя функции, seed) и НЕ зависит от scale. Это убирает дефект
  исходного ноутбука fin_3, где seed шума включал scale_type, и raw/norm видели разный шум.
- Градиент возвращается в ТОЙ ЖЕ точке x (аналитический). В norm-режиме он делится на
  (f_max - f_min) по правилу цепочки — масштаб, не меняющий направление.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np

from .functions import Benchmark

Array = np.ndarray


# Уровень шума на RAW-шкале для каждой функции (умеренный: заметен, но не разрушает задачу).
NOISE_SIGMA_RAW = {
    "Sphere": 0.005,
    "Rosenbrock": 0.05,
    "Rastrigin": 0.25,
    "Ackley": 0.05,
}


@dataclass
class Objective:
    """
    Объект, который передаётся оптимизатору. Метод __call__ возвращает кортеж:
        (observed_value, gradient_at_x)
    где observed_value учитывает scale и шум, а gradient_at_x — аналитический градиент
    наблюдаемой шкалы в точке x (без шума: шум добавляется только к значению).
    """
    bench: Benchmark
    scale: str          # 'raw' | 'norm'
    data: str           # 'clean' | 'noisy_y'
    seed: int
    f_max: float        # для нормализации (f_min считаем 0)

    def __post_init__(self):
        assert self.scale in ("raw", "norm")
        assert self.data in ("clean", "noisy_y")
        self._denom = max(self.f_max, 1e-12)              # f_min = 0
        self._sigma_raw = NOISE_SIGMA_RAW[self.bench.name]
        self._sigma = self._sigma_raw / (self._denom if self.scale == "norm" else 1.0)
        # ГСЧ шума зависит только от (имя, seed) -> raw и norm видят ОДИН и тот же шум.
        self._rng = np.random.default_rng(
            abs(hash((self.bench.name, int(self.seed)))) % (2 ** 32)
        )

    def _scaled_value(self, x: Array) -> float:
        v = self.bench.f(x)
        return v / self._denom if self.scale == "norm" else v

    def _scaled_grad(self, x: Array) -> Array:
        g = self.bench.grad(x)
        return g / self._denom if self.scale == "norm" else g

    def __call__(self, x: Array) -> Tuple[float, Array]:
        x = np.asarray(x, dtype=float)
        value = self._scaled_value(x)
        if self.data == "noisy_y":
            value = value + float(self._rng.normal(0.0, self._sigma))
        return float(value), self._scaled_grad(x)


def build_objective(bench: Benchmark, scale: str, data: str, seed: int, f_max: float) -> Objective:
    return Objective(bench=bench, scale=scale, data=data, seed=seed, f_max=f_max)
