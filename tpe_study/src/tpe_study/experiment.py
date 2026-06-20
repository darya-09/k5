"""
Слой эксперимента: реестр алгоритмов + прогон одной ячейки сетки по всем seeds.

Сетка эксперимента (полностью факторная):
    функция × scale(raw|norm) × data(clean|noisy_y) × алгоритм × seed

Алгоритмы (все, кроме random/optuna, — ОДИН и тот же класс TPE с одним изменённым флагом,
поэтому любая пара "tpe vs tpe_*" отличается ровно одним фактором):
    random        — случайный поиск (нижний baseline)
    tpe           — базовый TPE (без модификаций)
    tpe_gradw     — TPE + градиентное взвешивание наблюдений (фактор: weight)
    tpe_gp        — TPE + GP-переранжирование кандидатов (фактор: GP)
    tpe_gradw_gp  — TPE + weight + GP (это и есть "gTPE")
    optuna        — внешний референс TPE

Нормализация — это фактор `scale`, общий для всех алгоритмов (свойство задачи), поэтому
сравнение "нужна ли нормализация" = tpe@raw против tpe@norm.
"""
from __future__ import annotations

from typing import Dict, List

import numpy as np

from .baselines import optuna_tpe, random_search
from .functions import Benchmark
from .metrics import aggregate, best_so_far_curves, steps_to_threshold
from .objective import build_objective
from .tpe import TPE

# Пороги для "успеха" (шаги до порога) — по RAW CLEAN ошибке значения. Единые для всех алгоритмов.
THRESHOLDS = {"Sphere": 1e-3, "Rosenbrock": 5e-2, "Rastrigin": 1.0, "Ackley": 0.5}

# Полный набор алгоритмов. 4 формы w(x) — это отдельный «эксперимент по весу»;
# tpe_gp — только GP; tpe_gp_w — GP + лучший по смыслу вес (smooth_inv, «gTPE»-аналог).
ALGORITHMS = [
    "random",
    "tpe",
    "tpe_w_smooth",       # вес КАНДИДАТА w(x)=tanh, предпочтение БОЛЬШОМУ ‖∇f‖ (механизм fin_4)
    "tpe_w_smooth_inv",   # вес КАНДИДАТА w(x)=-tanh, предпочтение МАЛОМУ ‖∇f‖
    "tpe_w_sign",         # вес КАНДИДАТА w(x)=сигмоида·5, большому ‖∇f‖
    "tpe_w_sign_inv",     # вес КАНДИДАТА, малому ‖∇f‖
    "tpe_refine",         # локальный градиентный шаг по кандидату (механизм refine из fin_5)
    "tpe_gp",             # GP-переранжирование
    "tpe_gp_w",           # GP + взвешивание НАБЛЮДЕНИЙ по 1/‖∇f‖ (механизм gТPE из fin_5)
    "tpe_gp_refine",      # GP + refine (полный аналог gТPE weight+refine+GP по смыслу)
    "optuna",
]

# Классификация для честной интерпретации (по решению: black-box vs white-box).
# black-box — не используют градиент целевой функции; white-box — используют ТОЧНЫЙ ∇f (оракул).
ALGO_FAMILY = {
    "random": "black-box", "tpe": "black-box", "optuna": "black-box", "tpe_gp": "black-box",
    "tpe_w_smooth": "white-box(∇f)", "tpe_w_smooth_inv": "white-box(∇f)",
    "tpe_w_sign": "white-box(∇f)", "tpe_w_sign_inv": "white-box(∇f)",
    "tpe_refine": "white-box(∇f-descent)", "tpe_gp_refine": "white-box(∇f-descent)",
    "tpe_gp_w": "white-box(∇f)",
}


def _run_one(algo: str, objective, bench: Benchmark, n_trials: int,
             n_init: int, n_candidates: int, gamma: float, min_bw_frac: float,
             seed: int) -> dict:
    """Один прогон одного алгоритма на одной objective с заданным seed."""
    bounds = bench.bounds
    if algo == "random":
        return random_search(objective, bounds, n_trials, seed)
    if algo == "optuna":
        return optuna_tpe(objective, bounds, n_trials, n_init, n_candidates, seed)

    # grad_fn — оракул градиента (для веса кандидатов). Берём RAW-градиент функции:
    # нормировка норм по батчу делает вес инвариантным к масштабу, так что scale не важен.
    gfn = bench.grad
    flags = {
        "tpe":              dict(),
        "tpe_w_smooth":     dict(cand_weight_shape="smooth", grad_fn=gfn),
        "tpe_w_smooth_inv": dict(cand_weight_shape="smooth_inv", grad_fn=gfn),
        "tpe_w_sign":       dict(cand_weight_shape="sign", grad_fn=gfn),
        "tpe_w_sign_inv":   dict(cand_weight_shape="sign_inv", grad_fn=gfn),
        "tpe_refine":       dict(refine_steps=2, grad_fn=gfn),
        "tpe_gp":           dict(gp_rerank=True),
        "tpe_gp_w":         dict(gp_rerank=True, obs_gradient_weight=True),
        "tpe_gp_refine":    dict(gp_rerank=True, refine_steps=2, grad_fn=gfn),
    }[algo]
    opt = TPE(bounds=bounds, n_init=n_init, gamma=gamma, n_candidates=n_candidates,
              min_bw_frac=min_bw_frac, seed=seed, **flags)
    return opt.optimize(objective, n_trials)


def run_cell(bench: Benchmark, scale: str, data: str, algo: str, seeds: List[int],
             cfg: dict, f_max: float):
    """
    Прогон одной ячейки (функция, scale, data, algo) по всем seeds.
    Возвращает (агрегированная строка-метрики, список кривых для графиков).
    """
    dist_y_runs, dist_x_runs, steps_runs = [], [], []
    curves = []
    for s in seeds:
        # ВАЖНО: objective с одним и тем же (bench, data, seed) даёт ОДИН и тот же шум
        # для всех алгоритмов и обеих scale -> парность (common random numbers).
        objective = build_objective(bench, scale=scale, data=data, seed=s, f_max=f_max)
        res = _run_one(algo, objective, bench,
                       n_trials=cfg["max_evals"], n_init=cfg["n_init"],
                       n_candidates=cfg["n_candidates"], gamma=cfg["gamma"],
                       min_bw_frac=cfg["min_bw_frac"], seed=s)
        dy, dx = best_so_far_curves(res["x_history"], res["y_history"], bench)
        dist_y_runs.append(dy); dist_x_runs.append(dx)
        steps_runs.append(steps_to_threshold(dy, THRESHOLDS[bench.name]))
        curves.append({"seed": s, "x_history": res["x_history"],
                       "dist_y": dy, "dist_x": dx})

    agg = aggregate(dist_y_runs, dist_x_runs, steps_runs)
    row = {"function": bench.name, "scale": scale, "data": data, "algorithm": algo,
           "threshold_y": THRESHOLDS[bench.name], "n_seeds": len(seeds), **agg}
    return row, curves
