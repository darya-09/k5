"""
Внешние базовые алгоритмы для честного контекста сравнения:
  - random_search: нижняя граница (любой осмысленный метод должен её бить);
  - optuna_tpe   : независимая зрелая реализация TPE (верхний референс).

Оба возвращают тот же словарь, что и наш TPE.optimize: x_history, y_history, best_*.
Optuna видит ту же objective (scale/data), оценка качества — снаружи, по raw clean.
"""
from __future__ import annotations

from typing import Callable, Sequence, Tuple

import numpy as np

Array = np.ndarray
ObjectiveFn = Callable[[Array], Tuple[float, Array]]   # x -> (value, grad)


def random_search(objective: ObjectiveFn, bounds: Sequence[Tuple[float, float]],
                  n_trials: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    xs, ys = [], []
    for _ in range(n_trials):
        x = np.array([rng.uniform(lo, hi) for lo, hi in bounds])
        value, _ = objective(x)
        xs.append(x); ys.append(float(value))
    best_i = int(np.argmin(ys))
    return {"x_history": np.array(xs), "y_history": np.array(ys),
            "best_x": xs[best_i], "best_y": ys[best_i]}


def optuna_tpe(objective: ObjectiveFn, bounds: Sequence[Tuple[float, float]],
               n_trials: int, n_init: int, n_candidates: int, seed: int) -> dict:
    import optuna
    optuna.logging.set_verbosity(optuna.logging.WARNING)

    xs, ys = [], []

    def _obj(trial):
        x = np.array([trial.suggest_float(f"x{d}", lo, hi)
                      for d, (lo, hi) in enumerate(bounds)])
        value, _ = objective(x)
        xs.append(x); ys.append(float(value))
        return float(value)

    sampler = optuna.samplers.TPESampler(
        seed=seed, n_startup_trials=n_init, n_ei_candidates=n_candidates)
    study = optuna.create_study(direction="minimize", sampler=sampler)
    study.optimize(_obj, n_trials=n_trials, show_progress_bar=False)

    best_i = int(np.argmin(ys))
    return {"x_history": np.array(xs), "y_history": np.array(ys),
            "best_x": xs[best_i], "best_y": ys[best_i]}
