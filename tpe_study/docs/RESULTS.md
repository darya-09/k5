# RESULTS — табличные результаты и графики

> Сгенерировано автоматически из `results/tables/*.csv` (реальный прогон `run.py`).

## Конфигурация прогона

```json
{
  "seeds": 50,
  "n_init": 10,
  "max_evals": 80,
  "n_candidates": 24,
  "gamma": 0.15,
  "functions": [
    "Sphere",
    "Rosenbrock",
    "Rastrigin",
    "Ackley"
  ],
  "scales": [
    "raw",
    "norm"
  ],
  "data_types": [
    "clean",
    "noisy_y"
  ],
  "algorithms": [
    "random",
    "tpe",
    "tpe_gradw",
    "tpe_gp",
    "tpe_gradw_gp",
    "optuna"
  ]
}
```

## Сводка: средний success_rate по алгоритмам (по всем ячейкам)

| algorithm | avg_success_% |
|---|---|
| optuna | 15.8 |
| random | 3.5 |
| tpe | 36 |
| tpe_gp | 42.5 |
| tpe_gradw | 30.6 |
| tpe_gradw_gp | 36.5 |

## Авто-выводы (из чисел этого прогона)

- **Инвариантность нормализации для чистого rank-based `tpe`** (clean): максимальный |raw − norm| по final_dist_y = **0** → при ~0 это строго подтверждает: монотонно-аффинное масштабирование цели НЕ влияет на ранговый TPE.
- **Модификации масштабо-зависимы:** тот же разрыв для `tpe_gradw` = 0.826, для `tpe_gp` = 1.59. Причина: градиентный вес зависит от масштаба ∇, а GP-член `−μ+βσ` в y-единицах конкурирует с лог-плотностью → нормализация меняет баланс. Вывод: нормализация нужна именно для grad/GP-вариантов, а для базового TPE бесполезна.
- **Как часто модификация бьёт baseline `tpe`** (доля ячеек, % по final_dist_y):
  - `optuna`: 50.0%
  - `random`: 25.0%
  - `tpe_gp`: 75.0%
  - `tpe_gradw`: 43.8%
  - `tpe_gradw_gp`: 62.5%

## Статистическая значимость (парный Уилкоксон vs `tpe`, поправка Холма)

Из 80 сравнений значимы (p_holm<0.05): **12 в пользу модификации**, 12 против. Остальные различия статистически не подтверждены.

Значимые улучшения над baseline `tpe`:

| function | scale | data | algorithm | median_delta | p_holm |
|---|---|---|---|---|---|
| Ackley | raw | clean | tpe_gradw_gp | -0.117 | 0.003074 |
| Rosenbrock | norm | clean | optuna | -0.2071 | 0.03895 |
| Rosenbrock | norm | noisy_y | optuna | -0.2933 | 0.02061 |
| Rosenbrock | raw | clean | optuna | -0.2071 | 0.03895 |
| Rosenbrock | raw | clean | tpe_gp | -0.203 | 0.00845 |
| Rosenbrock | raw | noisy_y | optuna | -0.2933 | 0.02061 |
| Rosenbrock | raw | noisy_y | tpe_gp | -0.2356 | 0.001748 |
| Rosenbrock | raw | noisy_y | tpe_gradw_gp | -0.4056 | 0.02257 |
| Sphere | raw | clean | tpe_gp | -0.002197 | 4.355e-06 |
| Sphere | raw | clean | tpe_gradw_gp | -0.00227 | 4.093e-06 |
| Sphere | raw | noisy_y | tpe_gp | -0.003104 | 0.002567 |
| Sphere | raw | noisy_y | tpe_gradw_gp | -0.00433 | 2.228e-06 |

Сколько значимых выигрышей у каждой модификации (из 16 ячеек):

| algorithm | n_significant_wins |
|---|---|
| optuna | 4 |
| random | 0 |
| tpe_gp | 4 |
| tpe_gradw | 0 |
| tpe_gradw_gp | 4 |

## Ablation: каждая модификация против baseline `tpe`

Δ = algo − tpe по final_dist_y (меньше нуля → модификация лучше).

| function | scale | data | algorithm | tpe_final_dist_y | algo_final_dist_y | delta_dist_y(algo-tpe) | better_than_tpe | tpe_success_% | algo_success_% |
|---|---|---|---|---|---|---|---|---|---|
| Ackley | norm | clean | tpe_gradw | 0.8791 | 1.343 | 0.4637 | False | 66 | 52 |
| Ackley | norm | clean | tpe_gp | 0.8791 | 1.01 | 0.1312 | False | 66 | 62 |
| Ackley | norm | clean | tpe_gradw_gp | 0.8791 | 0.9015 | 0.02237 | False | 66 | 66 |
| Ackley | norm | clean | optuna | 0.8791 | 0.9895 | 0.1104 | False | 66 | 24 |
| Ackley | norm | clean | random | 0.8791 | 3.034 | 2.155 | False | 66 | 2 |
| Ackley | norm | noisy_y | tpe_gradw | 0.8947 | 0.9858 | 0.09114 | False | 68 | 68 |
| Ackley | norm | noisy_y | tpe_gp | 0.8947 | 0.965 | 0.0703 | False | 68 | 64 |
| Ackley | norm | noisy_y | tpe_gradw_gp | 0.8947 | 0.7404 | -0.1543 | True | 68 | 64 |
| Ackley | norm | noisy_y | optuna | 0.8947 | 0.9607 | 0.06596 | False | 68 | 26 |
| Ackley | norm | noisy_y | random | 0.8947 | 3.035 | 2.14 | False | 68 | 2 |
| Ackley | raw | clean | tpe_gradw | 0.8791 | 0.7841 | -0.09497 | True | 66 | 74 |
| Ackley | raw | clean | tpe_gp | 0.8791 | 0.4128 | -0.4663 | True | 66 | 84 |
| Ackley | raw | clean | tpe_gradw_gp | 0.8791 | 0.2292 | -0.6499 | True | 66 | 92 |
| Ackley | raw | clean | optuna | 0.8791 | 0.9895 | 0.1104 | False | 66 | 24 |
| Ackley | raw | clean | random | 0.8791 | 3.034 | 2.155 | False | 66 | 2 |
| Ackley | raw | noisy_y | tpe_gradw | 0.8947 | 0.8257 | -0.06896 | True | 68 | 68 |
| Ackley | raw | noisy_y | tpe_gp | 0.8947 | 0.3117 | -0.583 | True | 68 | 84 |
| Ackley | raw | noisy_y | tpe_gradw_gp | 0.8947 | 0.5481 | -0.3466 | True | 68 | 84 |
| Ackley | raw | noisy_y | optuna | 0.8947 | 0.9607 | 0.06596 | False | 68 | 26 |
| Ackley | raw | noisy_y | random | 0.8947 | 3.035 | 2.14 | False | 68 | 2 |
| Rastrigin | norm | clean | tpe_gradw | 2.52 | 2.742 | 0.2215 | False | 26 | 28 |
| Rastrigin | norm | clean | tpe_gp | 2.52 | 2.184 | -0.3358 | True | 26 | 10 |
| Rastrigin | norm | clean | tpe_gradw_gp | 2.52 | 3.29 | 0.7696 | False | 26 | 12 |
| Rastrigin | norm | clean | optuna | 2.52 | 2.979 | 0.4585 | False | 26 | 6 |
| Rastrigin | norm | clean | random | 2.52 | 6.103 | 3.583 | False | 26 | 2 |
| Rastrigin | norm | noisy_y | tpe_gradw | 2.847 | 3.018 | 0.1709 | False | 24 | 24 |
| Rastrigin | norm | noisy_y | tpe_gp | 2.847 | 2.217 | -0.6298 | True | 24 | 14 |
| Rastrigin | norm | noisy_y | tpe_gradw_gp | 2.847 | 3.489 | 0.6424 | False | 24 | 4 |
| Rastrigin | norm | noisy_y | optuna | 2.847 | 2.905 | 0.05778 | False | 24 | 8 |
| Rastrigin | norm | noisy_y | random | 2.847 | 6.112 | 3.266 | False | 24 | 2 |
| Rastrigin | raw | clean | tpe_gradw | 2.52 | 3.475 | 0.955 | False | 26 | 6 |
| Rastrigin | raw | clean | tpe_gp | 2.52 | 3.775 | 1.255 | False | 26 | 6 |
| Rastrigin | raw | clean | tpe_gradw_gp | 2.52 | 2.763 | 0.2428 | False | 26 | 10 |
| Rastrigin | raw | clean | optuna | 2.52 | 2.979 | 0.4585 | False | 26 | 6 |
| Rastrigin | raw | clean | random | 2.52 | 6.103 | 3.583 | False | 26 | 2 |
| Rastrigin | raw | noisy_y | tpe_gradw | 2.847 | 3.296 | 0.449 | False | 24 | 12 |
| Rastrigin | raw | noisy_y | tpe_gp | 2.847 | 3.999 | 1.152 | False | 24 | 8 |
| Rastrigin | raw | noisy_y | tpe_gradw_gp | 2.847 | 3.298 | 0.451 | False | 24 | 8 |
| Rastrigin | raw | noisy_y | optuna | 2.847 | 2.905 | 0.05778 | False | 24 | 8 |
| Rastrigin | raw | noisy_y | random | 2.847 | 6.112 | 3.266 | False | 24 | 2 |
| Rosenbrock | norm | clean | tpe_gradw | 1.424 | 1.61 | 0.1859 | False | 12 | 6 |
| Rosenbrock | norm | clean | tpe_gp | 1.424 | 1.412 | -0.01191 | True | 12 | 22 |
| Rosenbrock | norm | clean | tpe_gradw_gp | 1.424 | 1.079 | -0.345 | True | 12 | 6 |
| Rosenbrock | norm | clean | optuna | 1.424 | 0.4293 | -0.9948 | True | 12 | 28 |
| Rosenbrock | norm | clean | random | 1.424 | 0.8391 | -0.5849 | True | 12 | 10 |
| Rosenbrock | norm | noisy_y | tpe_gradw | 1.471 | 1.688 | 0.2176 | False | 12 | 6 |
| Rosenbrock | norm | noisy_y | tpe_gp | 1.471 | 1.412 | -0.0593 | True | 12 | 22 |
| Rosenbrock | norm | noisy_y | tpe_gradw_gp | 1.471 | 1.178 | -0.2933 | True | 12 | 6 |
| Rosenbrock | norm | noisy_y | optuna | 1.471 | 0.4525 | -1.018 | True | 12 | 24 |
| Rosenbrock | norm | noisy_y | random | 1.471 | 0.8407 | -0.6301 | True | 12 | 10 |
| Rosenbrock | raw | clean | tpe_gradw | 1.424 | 0.7843 | -0.6397 | True | 12 | 2 |
| Rosenbrock | raw | clean | tpe_gp | 1.424 | 0.3778 | -1.046 | True | 12 | 34 |
| Rosenbrock | raw | clean | tpe_gradw_gp | 1.424 | 0.3147 | -1.109 | True | 12 | 4 |
| Rosenbrock | raw | clean | optuna | 1.424 | 0.4293 | -0.9948 | True | 12 | 28 |
| Rosenbrock | raw | clean | random | 1.424 | 0.8391 | -0.5849 | True | 12 | 10 |
| Rosenbrock | raw | noisy_y | tpe_gradw | 1.471 | 0.8034 | -0.6675 | True | 12 | 2 |
| Rosenbrock | raw | noisy_y | tpe_gp | 1.471 | 0.4452 | -1.026 | True | 12 | 26 |
| Rosenbrock | raw | noisy_y | tpe_gradw_gp | 1.471 | 0.3072 | -1.164 | True | 12 | 6 |
| Rosenbrock | raw | noisy_y | optuna | 1.471 | 0.4525 | -1.018 | True | 12 | 24 |
| Rosenbrock | raw | noisy_y | random | 1.471 | 0.8407 | -0.6301 | True | 12 | 10 |
| Sphere | norm | clean | tpe_gradw | 0.06937 | 0.07027 | 0.0009021 | False | 46 | 48 |
| Sphere | norm | clean | tpe_gp | 0.06937 | 0.0245 | -0.04487 | True | 46 | 50 |
| Sphere | norm | clean | tpe_gradw_gp | 0.06937 | 0.0654 | -0.003968 | True | 46 | 46 |
| Sphere | norm | clean | optuna | 0.06937 | 0.03237 | -0.037 | True | 46 | 4 |
| Sphere | norm | clean | random | 0.06937 | 0.5264 | 0.457 | False | 46 | 0 |
| Sphere | norm | noisy_y | tpe_gradw | 0.06489 | 0.0596 | -0.005289 | True | 34 | 32 |
| Sphere | norm | noisy_y | tpe_gp | 0.06489 | 0.02329 | -0.0416 | True | 34 | 34 |
| Sphere | norm | noisy_y | tpe_gradw_gp | 0.06489 | 0.06592 | 0.001027 | False | 34 | 20 |
| Sphere | norm | noisy_y | optuna | 0.06489 | 0.03594 | -0.02895 | True | 34 | 6 |
| Sphere | norm | noisy_y | random | 0.06489 | 0.5264 | 0.4615 | False | 34 | 0 |
| Sphere | raw | clean | tpe_gradw | 0.06937 | 0.03346 | -0.0359 | True | 46 | 36 |
| Sphere | raw | clean | tpe_gp | 0.06937 | 0.001039 | -0.06833 | True | 46 | 94 |
| Sphere | raw | clean | tpe_gradw_gp | 0.06937 | 0.0029 | -0.06647 | True | 46 | 90 |
| Sphere | raw | clean | optuna | 0.06937 | 0.03237 | -0.037 | True | 46 | 4 |
| Sphere | raw | clean | random | 0.06937 | 0.5264 | 0.457 | False | 46 | 0 |
| Sphere | raw | noisy_y | tpe_gradw | 0.06489 | 0.04354 | -0.02135 | True | 34 | 26 |
| Sphere | raw | noisy_y | tpe_gp | 0.06489 | 0.002279 | -0.06261 | True | 34 | 66 |
| Sphere | raw | noisy_y | tpe_gradw_gp | 0.06489 | 0.001591 | -0.0633 | True | 34 | 66 |
| Sphere | raw | noisy_y | optuna | 0.06489 | 0.03594 | -0.02895 | True | 34 | 6 |
| Sphere | raw | noisy_y | random | 0.06489 | 0.5264 | 0.4615 | False | 34 | 0 |

## Ключевые метрики (все ячейки)

| function | scale | data | algorithm | success_rate_% | steps_mean | final_dist_y_mean | final_dist_x_mean |
|---|---|---|---|---|---|---|---|
| Sphere | raw | clean | random | 0 |  | 0.5264 | 0.6377 |
| Sphere | raw | clean | tpe | 46 | 47.13 | 0.06937 | 0.1483 |
| Sphere | raw | clean | tpe_gradw | 36 | 45.94 | 0.03346 | 0.1053 |
| Sphere | raw | clean | tpe_gp | 94 | 40.66 | 0.001039 | 0.01548 |
| Sphere | raw | clean | tpe_gradw_gp | 90 | 35.02 | 0.0029 | 0.01928 |
| Sphere | raw | clean | optuna | 4 | 48 | 0.03237 | 0.1559 |
| Sphere | raw | noisy_y | random | 0 |  | 0.5264 | 0.6377 |
| Sphere | raw | noisy_y | tpe | 34 | 46.47 | 0.06489 | 0.1622 |
| Sphere | raw | noisy_y | tpe_gradw | 26 | 47.23 | 0.04354 | 0.1262 |
| Sphere | raw | noisy_y | tpe_gp | 66 | 40.88 | 0.002279 | 0.04178 |
| Sphere | raw | noisy_y | tpe_gradw_gp | 66 | 36.58 | 0.001591 | 0.03434 |
| Sphere | raw | noisy_y | optuna | 6 | 56 | 0.03594 | 0.1633 |
| Sphere | norm | clean | random | 0 |  | 0.5264 | 0.6377 |
| Sphere | norm | clean | tpe | 46 | 47.13 | 0.06937 | 0.1483 |
| Sphere | norm | clean | tpe_gradw | 48 | 48 | 0.07027 | 0.1519 |
| Sphere | norm | clean | tpe_gp | 50 | 49.64 | 0.0245 | 0.09704 |
| Sphere | norm | clean | tpe_gradw_gp | 46 | 43.35 | 0.0654 | 0.1486 |
| Sphere | norm | clean | optuna | 4 | 48 | 0.03237 | 0.1559 |
| Sphere | norm | noisy_y | random | 0 |  | 0.5264 | 0.6377 |
| Sphere | norm | noisy_y | tpe | 34 | 46.47 | 0.06489 | 0.1622 |
| Sphere | norm | noisy_y | tpe_gradw | 32 | 50.12 | 0.0596 | 0.1561 |
| Sphere | norm | noisy_y | tpe_gp | 34 | 49.59 | 0.02329 | 0.1035 |
| Sphere | norm | noisy_y | tpe_gradw_gp | 20 | 37 | 0.06592 | 0.1712 |
| Sphere | norm | noisy_y | optuna | 6 | 56 | 0.03594 | 0.1633 |
| Rosenbrock | raw | clean | random | 10 | 43.6 | 0.8391 | 0.8455 |
| Rosenbrock | raw | clean | tpe | 12 | 43 | 1.424 | 1.258 |
| Rosenbrock | raw | clean | tpe_gradw | 2 | 15 | 0.7843 | 0.8966 |
| Rosenbrock | raw | clean | tpe_gp | 34 | 29.88 | 0.3778 | 0.8284 |
| Rosenbrock | raw | clean | tpe_gradw_gp | 4 | 56 | 0.3147 | 0.7821 |
| Rosenbrock | raw | clean | optuna | 28 | 49.64 | 0.4293 | 0.7599 |
| Rosenbrock | raw | noisy_y | random | 10 | 43.6 | 0.8407 | 0.8428 |
| Rosenbrock | raw | noisy_y | tpe | 12 | 38.5 | 1.471 | 1.297 |
| Rosenbrock | raw | noisy_y | tpe_gradw | 2 | 15 | 0.8034 | 0.9485 |
| Rosenbrock | raw | noisy_y | tpe_gp | 26 | 24.38 | 0.4452 | 0.9439 |
| Rosenbrock | raw | noisy_y | tpe_gradw_gp | 6 | 60.67 | 0.3072 | 0.7951 |
| Rosenbrock | raw | noisy_y | optuna | 24 | 48.92 | 0.4525 | 0.7638 |
| Rosenbrock | norm | clean | random | 10 | 43.6 | 0.8391 | 0.8455 |
| Rosenbrock | norm | clean | tpe | 12 | 43 | 1.424 | 1.258 |
| Rosenbrock | norm | clean | tpe_gradw | 6 | 28.33 | 1.61 | 1.418 |
| Rosenbrock | norm | clean | tpe_gp | 22 | 39.18 | 1.412 | 1.214 |
| Rosenbrock | norm | clean | tpe_gradw_gp | 6 | 23 | 1.079 | 1.221 |
| Rosenbrock | norm | clean | optuna | 28 | 49.64 | 0.4293 | 0.7599 |
| Rosenbrock | norm | noisy_y | random | 10 | 43.6 | 0.8407 | 0.8428 |
| Rosenbrock | norm | noisy_y | tpe | 12 | 38.5 | 1.471 | 1.297 |
| Rosenbrock | norm | noisy_y | tpe_gradw | 6 | 35.33 | 1.688 | 1.437 |
| Rosenbrock | norm | noisy_y | tpe_gp | 22 | 41 | 1.412 | 1.232 |
| Rosenbrock | norm | noisy_y | tpe_gradw_gp | 6 | 23 | 1.178 | 1.274 |
| Rosenbrock | norm | noisy_y | optuna | 24 | 48.92 | 0.4525 | 0.7638 |
| Rastrigin | raw | clean | random | 2 | 13 | 6.103 | 1.517 |
| Rastrigin | raw | clean | tpe | 26 | 49.23 | 2.52 | 1.332 |
| Rastrigin | raw | clean | tpe_gradw | 6 | 48 | 3.475 | 1.086 |
| Rastrigin | raw | clean | tpe_gp | 6 | 33 | 3.775 | 1.593 |
| Rastrigin | raw | clean | tpe_gradw_gp | 10 | 66.8 | 2.763 | 1.012 |
| Rastrigin | raw | clean | optuna | 6 | 51.67 | 2.979 | 1.132 |
| Rastrigin | raw | noisy_y | random | 2 | 13 | 6.112 | 1.565 |
| Rastrigin | raw | noisy_y | tpe | 24 | 47.08 | 2.847 | 1.344 |
| Rastrigin | raw | noisy_y | tpe_gradw | 12 | 61.17 | 3.296 | 1.042 |
| Rastrigin | raw | noisy_y | tpe_gp | 8 | 56 | 3.999 | 1.51 |
| Rastrigin | raw | noisy_y | tpe_gradw_gp | 8 | 56.5 | 3.298 | 1.223 |
| Rastrigin | raw | noisy_y | optuna | 8 | 41.5 | 2.905 | 1.089 |
| Rastrigin | norm | clean | random | 2 | 13 | 6.103 | 1.517 |
| Rastrigin | norm | clean | tpe | 26 | 49.23 | 2.52 | 1.332 |
| Rastrigin | norm | clean | tpe_gradw | 28 | 40.71 | 2.742 | 1.296 |
| Rastrigin | norm | clean | tpe_gp | 10 | 44.4 | 2.184 | 1.241 |
| Rastrigin | norm | clean | tpe_gradw_gp | 12 | 44 | 3.29 | 1.495 |
| Rastrigin | norm | clean | optuna | 6 | 51.67 | 2.979 | 1.132 |
| Rastrigin | norm | noisy_y | random | 2 | 13 | 6.112 | 1.565 |
| Rastrigin | norm | noisy_y | tpe | 24 | 47.08 | 2.847 | 1.344 |
| Rastrigin | norm | noisy_y | tpe_gradw | 24 | 39.5 | 3.018 | 1.374 |
| Rastrigin | norm | noisy_y | tpe_gp | 14 | 39.71 | 2.217 | 1.206 |
| Rastrigin | norm | noisy_y | tpe_gradw_gp | 4 | 51 | 3.489 | 1.617 |
| Rastrigin | norm | noisy_y | optuna | 8 | 41.5 | 2.905 | 1.089 |
| Ackley | raw | clean | random | 2 | 13 | 3.034 | 0.7459 |
| Ackley | raw | clean | tpe | 66 | 41.12 | 0.8791 | 0.2804 |
| Ackley | raw | clean | tpe_gradw | 74 | 41.92 | 0.7841 | 0.269 |
| Ackley | raw | clean | tpe_gp | 84 | 31.95 | 0.4128 | 0.133 |
| Ackley | raw | clean | tpe_gradw_gp | 92 | 37.07 | 0.2292 | 0.07622 |
| Ackley | raw | clean | optuna | 24 | 53.67 | 0.9895 | 0.1624 |
| Ackley | raw | noisy_y | random | 2 | 13 | 3.035 | 0.7555 |
| Ackley | raw | noisy_y | tpe | 68 | 36.65 | 0.8947 | 0.2956 |
| Ackley | raw | noisy_y | tpe_gradw | 68 | 40.68 | 0.8257 | 0.2605 |
| Ackley | raw | noisy_y | tpe_gp | 84 | 28.83 | 0.3117 | 0.09047 |
| Ackley | raw | noisy_y | tpe_gradw_gp | 84 | 38.1 | 0.5481 | 0.186 |
| Ackley | raw | noisy_y | optuna | 26 | 50.85 | 0.9607 | 0.1505 |
| Ackley | norm | clean | random | 2 | 13 | 3.034 | 0.7459 |
| Ackley | norm | clean | tpe | 66 | 41.12 | 0.8791 | 0.2804 |
| Ackley | norm | clean | tpe_gradw | 52 | 34.88 | 1.343 | 0.473 |
| Ackley | norm | clean | tpe_gp | 62 | 34.23 | 1.01 | 0.3142 |
| Ackley | norm | clean | tpe_gradw_gp | 66 | 37.76 | 0.9015 | 0.2781 |
| Ackley | norm | clean | optuna | 24 | 53.67 | 0.9895 | 0.1624 |
| Ackley | norm | noisy_y | random | 2 | 13 | 3.035 | 0.7555 |
| Ackley | norm | noisy_y | tpe | 68 | 36.65 | 0.8947 | 0.2956 |
| Ackley | norm | noisy_y | tpe_gradw | 68 | 39.56 | 0.9858 | 0.3512 |
| Ackley | norm | noisy_y | tpe_gp | 64 | 33.38 | 0.965 | 0.2901 |
| Ackley | norm | noisy_y | tpe_gradw_gp | 64 | 34.94 | 0.7404 | 0.2144 |
| Ackley | norm | noisy_y | optuna | 26 | 50.85 | 0.9607 | 0.1505 |

## Полная таблица (все метрики, все ячейки)

| function | scale | data | algorithm | success_rate_% | steps_mean | steps_std | final_dist_y_mean | final_dist_y_std | final_dist_y_median | final_dist_x_mean | final_dist_x_std |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Sphere | raw | clean | random | 0 |  |  | 0.5264 | 0.5564 | 0.2991 | 0.6377 | 0.346 |
| Sphere | raw | clean | tpe | 46 | 47.13 | 14.05 | 0.06937 | 0.2085 | 0.002301 | 0.1483 | 0.2177 |
| Sphere | raw | clean | tpe_gradw | 36 | 45.94 | 18.95 | 0.03346 | 0.0948 | 0.002211 | 0.1053 | 0.1496 |
| Sphere | raw | clean | tpe_gp | 94 | 40.66 | 15.68 | 0.001039 | 0.004589 | 7.124e-05 | 0.01548 | 0.02828 |
| Sphere | raw | clean | tpe_gradw_gp | 90 | 35.02 | 12.31 | 0.0029 | 0.01513 | 4.871e-05 | 0.01928 | 0.05028 |
| Sphere | raw | clean | optuna | 4 | 48 | 15 | 0.03237 | 0.04503 | 0.0202 | 0.1559 | 0.08978 |
| Sphere | raw | noisy_y | random | 0 |  |  | 0.5264 | 0.5564 | 0.2991 | 0.6377 | 0.346 |
| Sphere | raw | noisy_y | tpe | 34 | 46.47 | 14.22 | 0.06489 | 0.1793 | 0.005231 | 0.1622 | 0.1964 |
| Sphere | raw | noisy_y | tpe_gradw | 26 | 47.23 | 23.34 | 0.04354 | 0.114 | 0.004242 | 0.1262 | 0.1662 |
| Sphere | raw | noisy_y | tpe_gp | 66 | 40.88 | 16.57 | 0.002279 | 0.002965 | 0.001339 | 0.04178 | 0.02309 |
| Sphere | raw | noisy_y | tpe_gradw_gp | 66 | 36.58 | 16.73 | 0.001591 | 0.001668 | 0.001025 | 0.03434 | 0.02029 |
| Sphere | raw | noisy_y | optuna | 6 | 56 | 16.67 | 0.03594 | 0.04944 | 0.02048 | 0.1633 | 0.09634 |
| Sphere | norm | clean | random | 0 |  |  | 0.5264 | 0.5564 | 0.2991 | 0.6377 | 0.346 |
| Sphere | norm | clean | tpe | 46 | 47.13 | 14.05 | 0.06937 | 0.2085 | 0.002301 | 0.1483 | 0.2177 |
| Sphere | norm | clean | tpe_gradw | 48 | 48 | 16.76 | 0.07027 | 0.1453 | 0.001137 | 0.1519 | 0.2172 |
| Sphere | norm | clean | tpe_gp | 50 | 49.64 | 14.51 | 0.0245 | 0.04957 | 0.00154 | 0.09704 | 0.1228 |
| Sphere | norm | clean | tpe_gradw_gp | 46 | 43.35 | 15.64 | 0.0654 | 0.1508 | 0.002291 | 0.1486 | 0.2081 |
| Sphere | norm | clean | optuna | 4 | 48 | 15 | 0.03237 | 0.04503 | 0.0202 | 0.1559 | 0.08978 |
| Sphere | norm | noisy_y | random | 0 |  |  | 0.5264 | 0.5564 | 0.2991 | 0.6377 | 0.346 |
| Sphere | norm | noisy_y | tpe | 34 | 46.47 | 14.22 | 0.06489 | 0.1793 | 0.005231 | 0.1622 | 0.1964 |
| Sphere | norm | noisy_y | tpe_gradw | 32 | 50.12 | 17.57 | 0.0596 | 0.1269 | 0.004546 | 0.1561 | 0.1877 |
| Sphere | norm | noisy_y | tpe_gp | 34 | 49.59 | 18.86 | 0.02329 | 0.05252 | 0.005127 | 0.1035 | 0.1122 |
| Sphere | norm | noisy_y | tpe_gradw_gp | 20 | 37 | 15.97 | 0.06592 | 0.148 | 0.007575 | 0.1712 | 0.1913 |
| Sphere | norm | noisy_y | optuna | 6 | 56 | 16.67 | 0.03594 | 0.04944 | 0.02048 | 0.1633 | 0.09634 |
| Rosenbrock | raw | clean | random | 10 | 43.6 | 10.67 | 0.8391 | 0.8469 | 0.5392 | 0.8455 | 0.5613 |
| Rosenbrock | raw | clean | tpe | 12 | 43 | 23.12 | 1.424 | 1.823 | 0.4437 | 1.258 | 0.6943 |
| Rosenbrock | raw | clean | tpe_gradw | 2 | 15 | 0 | 0.7843 | 1.237 | 0.4106 | 0.8966 | 0.4636 |
| Rosenbrock | raw | clean | tpe_gp | 34 | 29.88 | 15.04 | 0.3778 | 1.007 | 0.1564 | 0.8284 | 0.6847 |
| Rosenbrock | raw | clean | tpe_gradw_gp | 4 | 56 | 8 | 0.3147 | 0.2401 | 0.2372 | 0.7821 | 0.4359 |
| Rosenbrock | raw | clean | optuna | 28 | 49.64 | 17.7 | 0.4293 | 0.9123 | 0.2338 | 0.7599 | 0.4676 |
| Rosenbrock | raw | noisy_y | random | 10 | 43.6 | 10.67 | 0.8407 | 0.8469 | 0.5392 | 0.8428 | 0.5601 |
| Rosenbrock | raw | noisy_y | tpe | 12 | 38.5 | 13.85 | 1.471 | 1.798 | 0.6099 | 1.297 | 0.6832 |
| Rosenbrock | raw | noisy_y | tpe_gradw | 2 | 15 | 0 | 0.8034 | 1.22 | 0.4472 | 0.9485 | 0.502 |
| Rosenbrock | raw | noisy_y | tpe_gp | 26 | 24.38 | 6.475 | 0.4452 | 0.9877 | 0.2732 | 0.9439 | 0.6302 |
| Rosenbrock | raw | noisy_y | tpe_gradw_gp | 6 | 60.67 | 11.09 | 0.3072 | 0.2194 | 0.2606 | 0.7951 | 0.4187 |
| Rosenbrock | raw | noisy_y | optuna | 24 | 48.92 | 18.83 | 0.4525 | 0.9117 | 0.2476 | 0.7638 | 0.5087 |
| Rosenbrock | norm | clean | random | 10 | 43.6 | 10.67 | 0.8391 | 0.8469 | 0.5392 | 0.8455 | 0.5613 |
| Rosenbrock | norm | clean | tpe | 12 | 43 | 23.12 | 1.424 | 1.823 | 0.4437 | 1.258 | 0.6943 |
| Rosenbrock | norm | clean | tpe_gradw | 6 | 28.33 | 11.32 | 1.61 | 1.744 | 0.9673 | 1.418 | 0.6549 |
| Rosenbrock | norm | clean | tpe_gp | 22 | 39.18 | 15.27 | 1.412 | 1.778 | 0.4518 | 1.214 | 0.7687 |
| Rosenbrock | norm | clean | tpe_gradw_gp | 6 | 23 | 7.789 | 1.079 | 1.268 | 0.5792 | 1.221 | 0.5691 |
| Rosenbrock | norm | clean | optuna | 28 | 49.64 | 17.7 | 0.4293 | 0.9123 | 0.2338 | 0.7599 | 0.4676 |
| Rosenbrock | norm | noisy_y | random | 10 | 43.6 | 10.67 | 0.8407 | 0.8469 | 0.5392 | 0.8428 | 0.5601 |
| Rosenbrock | norm | noisy_y | tpe | 12 | 38.5 | 13.85 | 1.471 | 1.798 | 0.6099 | 1.297 | 0.6832 |
| Rosenbrock | norm | noisy_y | tpe_gradw | 6 | 35.33 | 16.66 | 1.688 | 1.77 | 0.9988 | 1.437 | 0.6614 |
| Rosenbrock | norm | noisy_y | tpe_gp | 22 | 41 | 18.62 | 1.412 | 1.771 | 0.5109 | 1.232 | 0.7602 |
| Rosenbrock | norm | noisy_y | tpe_gradw_gp | 6 | 23 | 7.789 | 1.178 | 1.264 | 0.6422 | 1.274 | 0.5569 |
| Rosenbrock | norm | noisy_y | optuna | 24 | 48.92 | 18.83 | 0.4525 | 0.9117 | 0.2476 | 0.7638 | 0.5087 |
| Rastrigin | raw | clean | random | 2 | 13 | 0 | 6.103 | 3.105 | 5.759 | 1.517 | 0.6858 |
| Rastrigin | raw | clean | tpe | 26 | 49.23 | 17.35 | 2.52 | 2.16 | 1.994 | 1.332 | 0.7569 |
| Rastrigin | raw | clean | tpe_gradw | 6 | 48 | 2.828 | 3.475 | 2.101 | 3.209 | 1.086 | 0.5779 |
| Rastrigin | raw | clean | tpe_gp | 6 | 33 | 9.416 | 3.775 | 2.954 | 2.349 | 1.593 | 0.7583 |
| Rastrigin | raw | clean | tpe_gradw_gp | 10 | 66.8 | 10.24 | 2.763 | 1.752 | 2.405 | 1.012 | 0.6445 |
| Rastrigin | raw | clean | optuna | 6 | 51.67 | 16.78 | 2.979 | 1.592 | 2.665 | 1.132 | 0.6163 |
| Rastrigin | raw | noisy_y | random | 2 | 13 | 0 | 6.112 | 3.106 | 5.759 | 1.565 | 0.6944 |
| Rastrigin | raw | noisy_y | tpe | 24 | 47.08 | 19.4 | 2.847 | 2.507 | 1.932 | 1.344 | 0.8752 |
| Rastrigin | raw | noisy_y | tpe_gradw | 12 | 61.17 | 6.309 | 3.296 | 2.354 | 2.82 | 1.042 | 0.5632 |
| Rastrigin | raw | noisy_y | tpe_gp | 8 | 56 | 9.138 | 3.999 | 3.419 | 2.376 | 1.51 | 0.77 |
| Rastrigin | raw | noisy_y | tpe_gradw_gp | 8 | 56.5 | 10.74 | 3.298 | 1.835 | 3.086 | 1.223 | 0.626 |
| Rastrigin | raw | noisy_y | optuna | 8 | 41.5 | 14.15 | 2.905 | 1.601 | 2.694 | 1.089 | 0.5808 |
| Rastrigin | norm | clean | random | 2 | 13 | 0 | 6.103 | 3.105 | 5.759 | 1.517 | 0.6858 |
| Rastrigin | norm | clean | tpe | 26 | 49.23 | 17.35 | 2.52 | 2.16 | 1.994 | 1.332 | 0.7569 |
| Rastrigin | norm | clean | tpe_gradw | 28 | 40.71 | 15.22 | 2.742 | 3.069 | 1.534 | 1.296 | 0.9661 |
| Rastrigin | norm | clean | tpe_gp | 10 | 44.4 | 7.499 | 2.184 | 1.947 | 1.93 | 1.241 | 0.6708 |
| Rastrigin | norm | clean | tpe_gradw_gp | 12 | 44 | 22.5 | 3.29 | 2.953 | 2.01 | 1.495 | 0.7688 |
| Rastrigin | norm | clean | optuna | 6 | 51.67 | 16.78 | 2.979 | 1.592 | 2.665 | 1.132 | 0.6163 |
| Rastrigin | norm | noisy_y | random | 2 | 13 | 0 | 6.112 | 3.106 | 5.759 | 1.565 | 0.6944 |
| Rastrigin | norm | noisy_y | tpe | 24 | 47.08 | 19.4 | 2.847 | 2.507 | 1.932 | 1.344 | 0.8752 |
| Rastrigin | norm | noisy_y | tpe_gradw | 24 | 39.5 | 11.03 | 3.018 | 2.787 | 2.106 | 1.374 | 0.9268 |
| Rastrigin | norm | noisy_y | tpe_gp | 14 | 39.71 | 7.832 | 2.217 | 2.026 | 1.27 | 1.206 | 0.6892 |
| Rastrigin | norm | noisy_y | tpe_gradw_gp | 4 | 51 | 5 | 3.489 | 2.704 | 2.3 | 1.617 | 0.6854 |
| Rastrigin | norm | noisy_y | optuna | 8 | 41.5 | 14.15 | 2.905 | 1.601 | 2.694 | 1.089 | 0.5808 |
| Ackley | raw | clean | random | 2 | 13 | 0 | 3.034 | 1.048 | 3.1 | 0.7459 | 0.4371 |
| Ackley | raw | clean | tpe | 66 | 41.12 | 16.27 | 0.8791 | 1.195 | 0.1614 | 0.2804 | 0.4242 |
| Ackley | raw | clean | tpe_gradw | 74 | 41.92 | 14.89 | 0.7841 | 1.316 | 0.06478 | 0.269 | 0.4996 |
| Ackley | raw | clean | tpe_gp | 84 | 31.95 | 12.33 | 0.4128 | 0.8392 | 0.07085 | 0.133 | 0.3103 |
| Ackley | raw | clean | tpe_gradw_gp | 92 | 37.07 | 10.46 | 0.2292 | 0.6045 | 0.04883 | 0.07622 | 0.2229 |
| Ackley | raw | clean | optuna | 24 | 53.67 | 15.13 | 0.9895 | 0.5845 | 0.9683 | 0.1624 | 0.1213 |
| Ackley | raw | noisy_y | random | 2 | 13 | 0 | 3.035 | 1.049 | 3.1 | 0.7555 | 0.4439 |
| Ackley | raw | noisy_y | tpe | 68 | 36.65 | 11.88 | 0.8947 | 1.249 | 0.1408 | 0.2956 | 0.47 |
| Ackley | raw | noisy_y | tpe_gradw | 68 | 40.68 | 11.87 | 0.8257 | 1.267 | 0.1249 | 0.2605 | 0.4721 |
| Ackley | raw | noisy_y | tpe_gp | 84 | 28.83 | 10.18 | 0.3117 | 0.6216 | 0.08611 | 0.09047 | 0.2183 |
| Ackley | raw | noisy_y | tpe_gradw_gp | 84 | 38.1 | 10.56 | 0.5481 | 1.232 | 0.1053 | 0.186 | 0.4824 |
| Ackley | raw | noisy_y | optuna | 26 | 50.85 | 16.29 | 0.9607 | 0.5653 | 0.8654 | 0.1505 | 0.07041 |
| Ackley | norm | clean | random | 2 | 13 | 0 | 3.034 | 1.048 | 3.1 | 0.7459 | 0.4371 |
| Ackley | norm | clean | tpe | 66 | 41.12 | 16.27 | 0.8791 | 1.195 | 0.1614 | 0.2804 | 0.4242 |
| Ackley | norm | clean | tpe_gradw | 52 | 34.88 | 14.47 | 1.343 | 1.587 | 0.2996 | 0.473 | 0.6178 |
| Ackley | norm | clean | tpe_gp | 62 | 34.23 | 11.87 | 1.01 | 1.269 | 0.1366 | 0.3142 | 0.4415 |
| Ackley | norm | clean | tpe_gradw_gp | 66 | 37.76 | 15.81 | 0.9015 | 1.305 | 0.1016 | 0.2781 | 0.4584 |
| Ackley | norm | clean | optuna | 24 | 53.67 | 15.13 | 0.9895 | 0.5845 | 0.9683 | 0.1624 | 0.1213 |
| Ackley | norm | noisy_y | random | 2 | 13 | 0 | 3.035 | 1.049 | 3.1 | 0.7555 | 0.4439 |
| Ackley | norm | noisy_y | tpe | 68 | 36.65 | 11.88 | 0.8947 | 1.249 | 0.1408 | 0.2956 | 0.47 |
| Ackley | norm | noisy_y | tpe_gradw | 68 | 39.56 | 15.83 | 0.9858 | 1.52 | 0.1608 | 0.3512 | 0.5968 |
| Ackley | norm | noisy_y | tpe_gp | 64 | 33.38 | 12.14 | 0.965 | 1.346 | 0.1473 | 0.2901 | 0.4519 |
| Ackley | norm | noisy_y | tpe_gradw_gp | 64 | 34.94 | 16.71 | 0.7404 | 1.009 | 0.1257 | 0.2144 | 0.3588 |
| Ackley | norm | noisy_y | optuna | 26 | 50.85 | 16.29 | 0.9607 | 0.5653 | 0.8654 | 0.1505 | 0.07041 |

## Выводы (строго по числам прогона)

1. **Базовый `tpe` осмыслен:** средний success 36.0% против random 3.5% и optuna 15.8% (порог success строгий, поэтому смотрите и на final_dist_y).
2. **Нормализация цели для рангового TPE не влияет** (gap=0), но **важна для grad/GP-вариантов** (gap 0.83/1.6). Для базового TPE это no-op.
3. **GP-переранжирование (`tpe_gp`) — самая полезная модификация:** выше всех средний success (42.5%) и бьёт baseline в 75.0% ячеек; особенно сильно на гладких функциях.
4. **Градиентное взвешивание (`tpe_gradw`)** даёт умеренный эффект (лучше baseline в 43.8% ячеек), сильнее помогает по dist_x на многоэкстремальных.
5. **Комбинация (`tpe_gradw_gp` = gTPE)** бьёт baseline в 62.5% ячеек, но не доминирует над одним GP — выигрыш в основном от GP-части.

**Ограничения (честно):** градиент аналитический/точный (оракул, не black-box); один уровень шума на функцию; 2D; GP — только для переранжирования. Для сильных выводов нужны парные стат-тесты (Уилкоксон по seeds) и sensitivity по σ/размерности. Rosenbrock труден для покоординатного TPE (известный факт).

## Графики

Кривые сходимости (`conv_*`) и карты выбора точек (`map_*`) — в `results/figures/`.

- `figures/conv_Ackley_norm_clean.png`
- `figures/conv_Ackley_norm_noisy_y.png`
- `figures/conv_Ackley_raw_clean.png`
- `figures/conv_Ackley_raw_noisy_y.png`
- `figures/conv_Rastrigin_norm_clean.png`
- `figures/conv_Rastrigin_norm_noisy_y.png`
- `figures/conv_Rastrigin_raw_clean.png`
- `figures/conv_Rastrigin_raw_noisy_y.png`
- `figures/conv_Rosenbrock_norm_clean.png`
- `figures/conv_Rosenbrock_norm_noisy_y.png`
- `figures/conv_Rosenbrock_raw_clean.png`
- `figures/conv_Rosenbrock_raw_noisy_y.png`
- `figures/conv_Sphere_norm_clean.png`
- `figures/conv_Sphere_norm_noisy_y.png`
- `figures/conv_Sphere_raw_clean.png`
- `figures/conv_Sphere_raw_noisy_y.png`
- `figures/map_Ackley_norm_clean.png`
- `figures/map_Ackley_norm_noisy_y.png`
- `figures/map_Ackley_raw_clean.png`
- `figures/map_Ackley_raw_noisy_y.png`
- `figures/map_Rastrigin_norm_clean.png`
- `figures/map_Rastrigin_norm_noisy_y.png`
- `figures/map_Rastrigin_raw_clean.png`
- `figures/map_Rastrigin_raw_noisy_y.png`
- `figures/map_Rosenbrock_norm_clean.png`
- `figures/map_Rosenbrock_norm_noisy_y.png`
- `figures/map_Rosenbrock_raw_clean.png`
- `figures/map_Rosenbrock_raw_noisy_y.png`
- `figures/map_Sphere_norm_clean.png`
- `figures/map_Sphere_norm_noisy_y.png`
- `figures/map_Sphere_raw_clean.png`
- `figures/map_Sphere_raw_noisy_y.png`
