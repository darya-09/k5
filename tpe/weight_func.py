from __future__ import annotations
import numpy as np
from typing import Callable, Optional

_EPS: float = 1e-12

WeightFn = Callable[[np.ndarray], np.ndarray]


def scale_to_range(values: np.ndarray, low: float = 0.8, high: float = 1.2) -> np.ndarray:
    if low >= high:
        raise ValueError(f"low={low} должен быть меньше high={high}")
    v_min, v_max = np.min(values), np.max(values)
    spread = v_max - v_min
    if spread < _EPS:
        return np.full_like(values, (low + high) / 2.0, dtype=float)
    normalized = (values - v_min) / spread
    return np.clip(low + normalized * (high - low), low + _EPS, high - _EPS)


def compute_log_weight(
    x: np.ndarray,
    weight_fn: Optional[WeightFn] = None,
    low: float = 0.8,
    high: float = 1.2,
) -> np.ndarray:
    if weight_fn is None:
        return np.zeros(len(x), dtype=float)
    x = np.asarray(x, dtype=float)
    raw = np.asarray(weight_fn(x), dtype=float)
    if raw.shape != x.shape:
        raise ValueError(f"weight_fn должна возвращать массив той же формы что x")
    if not np.all(np.isfinite(raw)):
        raise ValueError("weight_fn вернула nan или inf")
    return np.log(scale_to_range(raw, low=low, high=high))


# Готовые функции
def smooth(x: np.ndarray) -> np.ndarray:
    return np.tanh(x)

def smooth_inv(x: np.ndarray) -> np.ndarray:
    return -np.tanh(x)

def sign_like(x: np.ndarray, sharpness: float = 5.0) -> np.ndarray:
    z = np.clip(sharpness * x, -500.0, 500.0)
    return 2.0 / (1.0 + np.exp(-z)) - 1.0

def sign_like_inv(x: np.ndarray, sharpness: float = 5.0) -> np.ndarray:
    return -sign_like(x, sharpness=sharpness)
