"""
Метрики качества. ВАЖНО: всё считается по RAW CLEAN функции, независимо от того,
какую шкалу/шум видел оптимизатор. Так сравнение методов честное.

Кривые строятся по "best-so-far": лучшая по НАБЛЮДАЕМОМУ значению точка на каждом шаге,
а её качество меряется истинной функцией (так действует реальный пользователь, который
выбирает лучшую по наблюдениям конфигурацию).
"""
from __future__ import annotations

from typing import Optional

import numpy as np

from .functions import Benchmark

Array = np.ndarray


def best_so_far_curves(x_history: Array, y_observed: Array, bench: Benchmark):
    """Возвращает кривые dist_y(t) и dist_x(t) по best-so-far точке (по наблюдаемому y)."""
    best_obs = np.inf
    best_x = None
    dist_y, dist_x = [], []
    for x, y in zip(x_history, y_observed):
        if y < best_obs:
            best_obs = float(y); best_x = np.asarray(x, float)
        dist_y.append(abs(bench.f(best_x) - bench.f_star))           # ошибка по значению
        dist_x.append(float(np.linalg.norm(best_x - bench.x_star)))  # ошибка по аргументу
    return np.array(dist_y), np.array(dist_x)


def steps_to_threshold(dist_y_curve: Array, threshold: float) -> Optional[int]:
    """Номер итерации (1-based), на которой dist_y впервые <= threshold; иначе None."""
    for i, v in enumerate(dist_y_curve):
        if v <= threshold:
            return i + 1
    return None


def aggregate(dist_y_runs, dist_x_runs, steps_runs):
    """Сводные статистики по набору повторов (seeds)."""
    final_y = np.array([c[-1] for c in dist_y_runs])
    final_x = np.array([c[-1] for c in dist_x_runs])
    reached = [s for s in steps_runs if s is not None]
    return {
        "success_rate_%": 100.0 * len(reached) / len(steps_runs),
        "steps_mean": float(np.mean(reached)) if reached else np.nan,
        "steps_std": float(np.std(reached)) if reached else np.nan,
        "final_dist_y_mean": float(np.mean(final_y)),
        "final_dist_y_std": float(np.std(final_y)),
        "final_dist_y_median": float(np.median(final_y)),
        "final_dist_x_mean": float(np.mean(final_x)),
        "final_dist_x_std": float(np.std(final_x)),
        "final_dist_x_median": float(np.median(final_x)),
    }
