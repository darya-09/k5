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
    "tpe_w_smooth",
    "tpe_w_smooth_inv",
    "tpe_w_sign",
    "tpe_w_sign_inv",
    "tpe_gp",
    "tpe_gp_w",
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
| tpe_gp_w | 41.9 |
| tpe_w_sign | 33 |
| tpe_w_sign_inv | 33.8 |
| tpe_w_smooth | 35.8 |
| tpe_w_smooth_inv | 39.2 |

## Авто-выводы (из чисел этого прогона)

- **Инвариантность нормализации для чистого rank-based `tpe`** (clean): максимальный |raw − norm| по final_dist_y = **0** → при ~0 это строго подтверждает: монотонно-аффинное масштабирование цели НЕ влияет на ранговый TPE.
- **Формы w(x) тоже инвариантны** (`tpe_w_smooth` gap = 0): вес считается по min-max-рангу норм градиента, и постоянный множитель от нормализации сокращается. **Масштабо-зависим только GP** (`tpe_gp` gap = 1.59): член `−μ+βσ` в y-единицах конкурирует с лог-плотностью. Вывод: нормализация бесполезна для всех rank/вес-вариантов TPE и важна лишь для GP.
- **Как часто модификация бьёт baseline `tpe`** (доля ячеек, % по final_dist_y):
  - `optuna`: 50.0%
  - `random`: 25.0%
  - `tpe_gp`: 75.0%
  - `tpe_gp_w`: 68.8%
  - `tpe_w_sign`: 37.5%
  - `tpe_w_sign_inv`: 12.5%
  - `tpe_w_smooth`: 87.5%
  - `tpe_w_smooth_inv`: 37.5%

## Статистическая значимость (парный Уилкоксон vs `tpe`, поправка Холма)

Из 128 сравнений значимы (p_holm<0.05): **9 в пользу модификации**, 12 против. Остальные различия статистически не подтверждены.

Значимые улучшения над baseline `tpe`:

| function | scale | data | algorithm | median_delta | p_holm |
|---|---|---|---|---|---|
| Rosenbrock | norm | noisy_y | optuna | -0.2933 | 0.03683 |
| Rosenbrock | raw | clean | tpe_gp | -0.203 | 0.01513 |
| Rosenbrock | raw | noisy_y | optuna | -0.2933 | 0.03683 |
| Rosenbrock | raw | noisy_y | tpe_gp | -0.2356 | 0.003038 |
| Rosenbrock | raw | noisy_y | tpe_gp_w | -0.2629 | 0.01873 |
| Sphere | raw | clean | tpe_gp | -0.002197 | 7.34e-06 |
| Sphere | raw | clean | tpe_gp_w | -0.002175 | 5.329e-07 |
| Sphere | raw | noisy_y | tpe_gp | -0.003104 | 0.004493 |
| Sphere | raw | noisy_y | tpe_gp_w | -0.004035 | 3.985e-06 |

Сколько значимых выигрышей у каждой модификации (из 16 ячеек):

| algorithm | n_significant_wins |
|---|---|
| optuna | 2 |
| random | 0 |
| tpe_gp | 4 |
| tpe_gp_w | 3 |
| tpe_w_sign | 0 |
| tpe_w_sign_inv | 0 |
| tpe_w_smooth | 0 |
| tpe_w_smooth_inv | 0 |

## Ablation: каждая модификация против baseline `tpe`

Δ = algo − tpe по final_dist_y (меньше нуля → модификация лучше).

| function | scale | data | algorithm | tpe_final_dist_y | algo_final_dist_y | delta_dist_y(algo-tpe) | better_than_tpe | tpe_success_% | algo_success_% |
|---|---|---|---|---|---|---|---|---|---|
| Ackley | norm | clean | random | 0.8791 | 3.034 | 2.155 | False | 66 | 2 |
| Ackley | norm | clean | tpe_w_smooth | 0.8791 | 0.7253 | -0.1538 | True | 66 | 72 |
| Ackley | norm | clean | tpe_w_smooth_inv | 0.8791 | 1.179 | 0.2998 | False | 66 | 56 |
| Ackley | norm | clean | tpe_w_sign | 0.8791 | 0.736 | -0.1431 | True | 66 | 72 |
| Ackley | norm | clean | tpe_w_sign_inv | 0.8791 | 1.233 | 0.3537 | False | 66 | 52 |
| Ackley | norm | clean | tpe_gp | 0.8791 | 1.01 | 0.1312 | False | 66 | 62 |
| Ackley | norm | clean | tpe_gp_w | 0.8791 | 0.8358 | -0.04331 | True | 66 | 68 |
| Ackley | norm | clean | optuna | 0.8791 | 0.9895 | 0.1104 | False | 66 | 24 |
| Ackley | norm | noisy_y | random | 0.8947 | 3.035 | 2.14 | False | 68 | 2 |
| Ackley | norm | noisy_y | tpe_w_smooth | 0.8947 | 0.7765 | -0.1182 | True | 68 | 70 |
| Ackley | norm | noisy_y | tpe_w_smooth_inv | 0.8947 | 0.9995 | 0.1048 | False | 68 | 70 |
| Ackley | norm | noisy_y | tpe_w_sign | 0.8947 | 0.9471 | 0.05241 | False | 68 | 64 |
| Ackley | norm | noisy_y | tpe_w_sign_inv | 0.8947 | 1.199 | 0.3046 | False | 68 | 60 |
| Ackley | norm | noisy_y | tpe_gp | 0.8947 | 0.965 | 0.0703 | False | 68 | 64 |
| Ackley | norm | noisy_y | tpe_gp_w | 0.8947 | 0.8926 | -0.002063 | True | 68 | 68 |
| Ackley | norm | noisy_y | optuna | 0.8947 | 0.9607 | 0.06596 | False | 68 | 26 |
| Ackley | raw | clean | random | 0.8791 | 3.034 | 2.155 | False | 66 | 2 |
| Ackley | raw | clean | tpe_w_smooth | 0.8791 | 0.7253 | -0.1538 | True | 66 | 72 |
| Ackley | raw | clean | tpe_w_smooth_inv | 0.8791 | 1.179 | 0.2998 | False | 66 | 56 |
| Ackley | raw | clean | tpe_w_sign | 0.8791 | 0.736 | -0.1431 | True | 66 | 72 |
| Ackley | raw | clean | tpe_w_sign_inv | 0.8791 | 1.233 | 0.3537 | False | 66 | 52 |
| Ackley | raw | clean | tpe_gp | 0.8791 | 0.4128 | -0.4663 | True | 66 | 84 |
| Ackley | raw | clean | tpe_gp_w | 0.8791 | 0.58 | -0.2991 | True | 66 | 78 |
| Ackley | raw | clean | optuna | 0.8791 | 0.9895 | 0.1104 | False | 66 | 24 |
| Ackley | raw | noisy_y | random | 0.8947 | 3.035 | 2.14 | False | 68 | 2 |
| Ackley | raw | noisy_y | tpe_w_smooth | 0.8947 | 0.7765 | -0.1182 | True | 68 | 70 |
| Ackley | raw | noisy_y | tpe_w_smooth_inv | 0.8947 | 0.9995 | 0.1048 | False | 68 | 70 |
| Ackley | raw | noisy_y | tpe_w_sign | 0.8947 | 0.9471 | 0.05241 | False | 68 | 64 |
| Ackley | raw | noisy_y | tpe_w_sign_inv | 0.8947 | 1.199 | 0.3046 | False | 68 | 60 |
| Ackley | raw | noisy_y | tpe_gp | 0.8947 | 0.3117 | -0.583 | True | 68 | 84 |
| Ackley | raw | noisy_y | tpe_gp_w | 0.8947 | 0.591 | -0.3037 | True | 68 | 82 |
| Ackley | raw | noisy_y | optuna | 0.8947 | 0.9607 | 0.06596 | False | 68 | 26 |
| Rastrigin | norm | clean | random | 2.52 | 6.103 | 3.583 | False | 26 | 2 |
| Rastrigin | norm | clean | tpe_w_smooth | 2.52 | 2.949 | 0.4289 | False | 26 | 14 |
| Rastrigin | norm | clean | tpe_w_smooth_inv | 2.52 | 2.556 | 0.03587 | False | 26 | 24 |
| Rastrigin | norm | clean | tpe_w_sign | 2.52 | 2.853 | 0.3324 | False | 26 | 16 |
| Rastrigin | norm | clean | tpe_w_sign_inv | 2.52 | 2.859 | 0.3388 | False | 26 | 12 |
| Rastrigin | norm | clean | tpe_gp | 2.52 | 2.184 | -0.3358 | True | 26 | 10 |
| Rastrigin | norm | clean | tpe_gp_w | 2.52 | 2.629 | 0.1084 | False | 26 | 20 |
| Rastrigin | norm | clean | optuna | 2.52 | 2.979 | 0.4585 | False | 26 | 6 |
| Rastrigin | norm | noisy_y | random | 2.847 | 6.112 | 3.266 | False | 24 | 2 |
| Rastrigin | norm | noisy_y | tpe_w_smooth | 2.847 | 2.802 | -0.04464 | True | 24 | 8 |
| Rastrigin | norm | noisy_y | tpe_w_smooth_inv | 2.847 | 2.636 | -0.2112 | True | 24 | 22 |
| Rastrigin | norm | noisy_y | tpe_w_sign | 2.847 | 2.896 | 0.04885 | False | 24 | 14 |
| Rastrigin | norm | noisy_y | tpe_w_sign_inv | 2.847 | 3.084 | 0.2374 | False | 24 | 8 |
| Rastrigin | norm | noisy_y | tpe_gp | 2.847 | 2.217 | -0.6298 | True | 24 | 14 |
| Rastrigin | norm | noisy_y | tpe_gp_w | 2.847 | 2.811 | -0.03606 | True | 24 | 14 |
| Rastrigin | norm | noisy_y | optuna | 2.847 | 2.905 | 0.05778 | False | 24 | 8 |
| Rastrigin | raw | clean | random | 2.52 | 6.103 | 3.583 | False | 26 | 2 |
| Rastrigin | raw | clean | tpe_w_smooth | 2.52 | 2.949 | 0.4289 | False | 26 | 14 |
| Rastrigin | raw | clean | tpe_w_smooth_inv | 2.52 | 2.556 | 0.03587 | False | 26 | 24 |
| Rastrigin | raw | clean | tpe_w_sign | 2.52 | 2.853 | 0.3324 | False | 26 | 16 |
| Rastrigin | raw | clean | tpe_w_sign_inv | 2.52 | 2.859 | 0.3388 | False | 26 | 12 |
| Rastrigin | raw | clean | tpe_gp | 2.52 | 3.775 | 1.255 | False | 26 | 6 |
| Rastrigin | raw | clean | tpe_gp_w | 2.52 | 3.779 | 1.259 | False | 26 | 8 |
| Rastrigin | raw | clean | optuna | 2.52 | 2.979 | 0.4585 | False | 26 | 6 |
| Rastrigin | raw | noisy_y | random | 2.847 | 6.112 | 3.266 | False | 24 | 2 |
| Rastrigin | raw | noisy_y | tpe_w_smooth | 2.847 | 2.802 | -0.04464 | True | 24 | 8 |
| Rastrigin | raw | noisy_y | tpe_w_smooth_inv | 2.847 | 2.636 | -0.2112 | True | 24 | 22 |
| Rastrigin | raw | noisy_y | tpe_w_sign | 2.847 | 2.896 | 0.04885 | False | 24 | 14 |
| Rastrigin | raw | noisy_y | tpe_w_sign_inv | 2.847 | 3.084 | 0.2374 | False | 24 | 8 |
| Rastrigin | raw | noisy_y | tpe_gp | 2.847 | 3.999 | 1.152 | False | 24 | 8 |
| Rastrigin | raw | noisy_y | tpe_gp_w | 2.847 | 3.717 | 0.8702 | False | 24 | 12 |
| Rastrigin | raw | noisy_y | optuna | 2.847 | 2.905 | 0.05778 | False | 24 | 8 |
| Rosenbrock | norm | clean | random | 1.424 | 0.8391 | -0.5849 | True | 12 | 10 |
| Rosenbrock | norm | clean | tpe_w_smooth | 1.424 | 1.31 | -0.1145 | True | 12 | 24 |
| Rosenbrock | norm | clean | tpe_w_smooth_inv | 1.424 | 1.482 | 0.05762 | False | 12 | 24 |
| Rosenbrock | norm | clean | tpe_w_sign | 1.424 | 1.357 | -0.0671 | True | 12 | 16 |
| Rosenbrock | norm | clean | tpe_w_sign_inv | 1.424 | 1.477 | 0.05345 | False | 12 | 24 |
| Rosenbrock | norm | clean | tpe_gp | 1.424 | 1.412 | -0.01191 | True | 12 | 22 |
| Rosenbrock | norm | clean | tpe_gp_w | 1.424 | 1.445 | 0.02146 | False | 12 | 14 |
| Rosenbrock | norm | clean | optuna | 1.424 | 0.4293 | -0.9948 | True | 12 | 28 |
| Rosenbrock | norm | noisy_y | random | 1.471 | 0.8407 | -0.6301 | True | 12 | 10 |
| Rosenbrock | norm | noisy_y | tpe_w_smooth | 1.471 | 1.314 | -0.1564 | True | 12 | 24 |
| Rosenbrock | norm | noisy_y | tpe_w_smooth_inv | 1.471 | 1.521 | 0.05017 | False | 12 | 22 |
| Rosenbrock | norm | noisy_y | tpe_w_sign | 1.471 | 1.331 | -0.1401 | True | 12 | 14 |
| Rosenbrock | norm | noisy_y | tpe_w_sign_inv | 1.471 | 1.497 | 0.02625 | False | 12 | 22 |
| Rosenbrock | norm | noisy_y | tpe_gp | 1.471 | 1.412 | -0.0593 | True | 12 | 22 |
| Rosenbrock | norm | noisy_y | tpe_gp_w | 1.471 | 1.486 | 0.01473 | False | 12 | 12 |
| Rosenbrock | norm | noisy_y | optuna | 1.471 | 0.4525 | -1.018 | True | 12 | 24 |
| Rosenbrock | raw | clean | random | 1.424 | 0.8391 | -0.5849 | True | 12 | 10 |
| Rosenbrock | raw | clean | tpe_w_smooth | 1.424 | 1.31 | -0.1145 | True | 12 | 24 |
| Rosenbrock | raw | clean | tpe_w_smooth_inv | 1.424 | 1.482 | 0.05762 | False | 12 | 24 |
| Rosenbrock | raw | clean | tpe_w_sign | 1.424 | 1.357 | -0.0671 | True | 12 | 16 |
| Rosenbrock | raw | clean | tpe_w_sign_inv | 1.424 | 1.477 | 0.05345 | False | 12 | 24 |
| Rosenbrock | raw | clean | tpe_gp | 1.424 | 0.3778 | -1.046 | True | 12 | 34 |
| Rosenbrock | raw | clean | tpe_gp_w | 1.424 | 0.3259 | -1.098 | True | 12 | 22 |
| Rosenbrock | raw | clean | optuna | 1.424 | 0.4293 | -0.9948 | True | 12 | 28 |
| Rosenbrock | raw | noisy_y | random | 1.471 | 0.8407 | -0.6301 | True | 12 | 10 |
| Rosenbrock | raw | noisy_y | tpe_w_smooth | 1.471 | 1.314 | -0.1564 | True | 12 | 24 |
| Rosenbrock | raw | noisy_y | tpe_w_smooth_inv | 1.471 | 1.521 | 0.05017 | False | 12 | 22 |
| Rosenbrock | raw | noisy_y | tpe_w_sign | 1.471 | 1.331 | -0.1401 | True | 12 | 14 |
| Rosenbrock | raw | noisy_y | tpe_w_sign_inv | 1.471 | 1.497 | 0.02625 | False | 12 | 22 |
| Rosenbrock | raw | noisy_y | tpe_gp | 1.471 | 0.4452 | -1.026 | True | 12 | 26 |
| Rosenbrock | raw | noisy_y | tpe_gp_w | 1.471 | 0.3036 | -1.167 | True | 12 | 20 |
| Rosenbrock | raw | noisy_y | optuna | 1.471 | 0.4525 | -1.018 | True | 12 | 24 |
| Sphere | norm | clean | random | 0.06937 | 0.5264 | 0.457 | False | 46 | 0 |
| Sphere | norm | clean | tpe_w_smooth | 0.06937 | 0.04871 | -0.02066 | True | 46 | 48 |
| Sphere | norm | clean | tpe_w_smooth_inv | 0.06937 | 0.04728 | -0.02208 | True | 46 | 58 |
| Sphere | norm | clean | tpe_w_sign | 0.06937 | 0.1302 | 0.06086 | False | 46 | 42 |
| Sphere | norm | clean | tpe_w_sign_inv | 0.06937 | 0.06441 | -0.004954 | True | 46 | 56 |
| Sphere | norm | clean | tpe_gp | 0.06937 | 0.0245 | -0.04487 | True | 46 | 50 |
| Sphere | norm | clean | tpe_gp_w | 0.06937 | 0.01586 | -0.0535 | True | 46 | 50 |
| Sphere | norm | clean | optuna | 0.06937 | 0.03237 | -0.037 | True | 46 | 4 |
| Sphere | norm | noisy_y | random | 0.06489 | 0.5264 | 0.4615 | False | 34 | 0 |
| Sphere | norm | noisy_y | tpe_w_smooth | 0.06489 | 0.0478 | -0.01709 | True | 34 | 26 |
| Sphere | norm | noisy_y | tpe_w_smooth_inv | 0.06489 | 0.05103 | -0.01386 | True | 34 | 38 |
| Sphere | norm | noisy_y | tpe_w_sign | 0.06489 | 0.1488 | 0.08392 | False | 34 | 26 |
| Sphere | norm | noisy_y | tpe_w_sign_inv | 0.06489 | 0.0817 | 0.01681 | False | 34 | 36 |
| Sphere | norm | noisy_y | tpe_gp | 0.06489 | 0.02329 | -0.0416 | True | 34 | 34 |
| Sphere | norm | noisy_y | tpe_gp_w | 0.06489 | 0.02954 | -0.03535 | True | 34 | 36 |
| Sphere | norm | noisy_y | optuna | 0.06489 | 0.03594 | -0.02895 | True | 34 | 6 |
| Sphere | raw | clean | random | 0.06937 | 0.5264 | 0.457 | False | 46 | 0 |
| Sphere | raw | clean | tpe_w_smooth | 0.06937 | 0.04871 | -0.02066 | True | 46 | 48 |
| Sphere | raw | clean | tpe_w_smooth_inv | 0.06937 | 0.04728 | -0.02208 | True | 46 | 58 |
| Sphere | raw | clean | tpe_w_sign | 0.06937 | 0.1302 | 0.06086 | False | 46 | 42 |
| Sphere | raw | clean | tpe_w_sign_inv | 0.06937 | 0.06441 | -0.004954 | True | 46 | 56 |
| Sphere | raw | clean | tpe_gp | 0.06937 | 0.001039 | -0.06833 | True | 46 | 94 |
| Sphere | raw | clean | tpe_gp_w | 0.06937 | 0.0002211 | -0.06915 | True | 46 | 96 |
| Sphere | raw | clean | optuna | 0.06937 | 0.03237 | -0.037 | True | 46 | 4 |
| Sphere | raw | noisy_y | random | 0.06489 | 0.5264 | 0.4615 | False | 34 | 0 |
| Sphere | raw | noisy_y | tpe_w_smooth | 0.06489 | 0.0478 | -0.01709 | True | 34 | 26 |
| Sphere | raw | noisy_y | tpe_w_smooth_inv | 0.06489 | 0.05103 | -0.01386 | True | 34 | 38 |
| Sphere | raw | noisy_y | tpe_w_sign | 0.06489 | 0.1488 | 0.08392 | False | 34 | 26 |
| Sphere | raw | noisy_y | tpe_w_sign_inv | 0.06489 | 0.0817 | 0.01681 | False | 34 | 36 |
| Sphere | raw | noisy_y | tpe_gp | 0.06489 | 0.002279 | -0.06261 | True | 34 | 66 |
| Sphere | raw | noisy_y | tpe_gp_w | 0.06489 | 0.001662 | -0.06323 | True | 34 | 70 |
| Sphere | raw | noisy_y | optuna | 0.06489 | 0.03594 | -0.02895 | True | 34 | 6 |

## Ключевые метрики (все ячейки)

| function | scale | data | algorithm | success_rate_% | steps_mean | final_dist_y_mean | final_dist_x_mean |
|---|---|---|---|---|---|---|---|
| Sphere | raw | clean | random | 0 |  | 0.5264 | 0.6377 |
| Sphere | raw | clean | tpe | 46 | 47.13 | 0.06937 | 0.1483 |
| Sphere | raw | clean | tpe_w_smooth | 48 | 47.96 | 0.04871 | 0.1305 |
| Sphere | raw | clean | tpe_w_smooth_inv | 58 | 44.66 | 0.04728 | 0.1008 |
| Sphere | raw | clean | tpe_w_sign | 42 | 48.19 | 0.1302 | 0.1826 |
| Sphere | raw | clean | tpe_w_sign_inv | 56 | 47.96 | 0.06441 | 0.1262 |
| Sphere | raw | clean | tpe_gp | 94 | 40.66 | 0.001039 | 0.01548 |
| Sphere | raw | clean | tpe_gp_w | 96 | 36.08 | 0.0002211 | 0.01059 |
| Sphere | raw | clean | optuna | 4 | 48 | 0.03237 | 0.1559 |
| Sphere | raw | noisy_y | random | 0 |  | 0.5264 | 0.6377 |
| Sphere | raw | noisy_y | tpe | 34 | 46.47 | 0.06489 | 0.1622 |
| Sphere | raw | noisy_y | tpe_w_smooth | 26 | 54.92 | 0.0478 | 0.1458 |
| Sphere | raw | noisy_y | tpe_w_smooth_inv | 38 | 38.63 | 0.05103 | 0.1246 |
| Sphere | raw | noisy_y | tpe_w_sign | 26 | 49.69 | 0.1488 | 0.2274 |
| Sphere | raw | noisy_y | tpe_w_sign_inv | 36 | 41.17 | 0.0817 | 0.1641 |
| Sphere | raw | noisy_y | tpe_gp | 66 | 40.88 | 0.002279 | 0.04178 |
| Sphere | raw | noisy_y | tpe_gp_w | 70 | 43.66 | 0.001662 | 0.03505 |
| Sphere | raw | noisy_y | optuna | 6 | 56 | 0.03594 | 0.1633 |
| Sphere | norm | clean | random | 0 |  | 0.5264 | 0.6377 |
| Sphere | norm | clean | tpe | 46 | 47.13 | 0.06937 | 0.1483 |
| Sphere | norm | clean | tpe_w_smooth | 48 | 47.96 | 0.04871 | 0.1305 |
| Sphere | norm | clean | tpe_w_smooth_inv | 58 | 44.66 | 0.04728 | 0.1008 |
| Sphere | norm | clean | tpe_w_sign | 42 | 48.19 | 0.1302 | 0.1826 |
| Sphere | norm | clean | tpe_w_sign_inv | 56 | 47.96 | 0.06441 | 0.1262 |
| Sphere | norm | clean | tpe_gp | 50 | 49.64 | 0.0245 | 0.09704 |
| Sphere | norm | clean | tpe_gp_w | 50 | 44.2 | 0.01586 | 0.06417 |
| Sphere | norm | clean | optuna | 4 | 48 | 0.03237 | 0.1559 |
| Sphere | norm | noisy_y | random | 0 |  | 0.5264 | 0.6377 |
| Sphere | norm | noisy_y | tpe | 34 | 46.47 | 0.06489 | 0.1622 |
| Sphere | norm | noisy_y | tpe_w_smooth | 26 | 54.92 | 0.0478 | 0.1458 |
| Sphere | norm | noisy_y | tpe_w_smooth_inv | 38 | 38.63 | 0.05103 | 0.1246 |
| Sphere | norm | noisy_y | tpe_w_sign | 26 | 49.69 | 0.1488 | 0.2274 |
| Sphere | norm | noisy_y | tpe_w_sign_inv | 36 | 41.17 | 0.0817 | 0.1641 |
| Sphere | norm | noisy_y | tpe_gp | 34 | 49.59 | 0.02329 | 0.1035 |
| Sphere | norm | noisy_y | tpe_gp_w | 36 | 34.11 | 0.02954 | 0.1089 |
| Sphere | norm | noisy_y | optuna | 6 | 56 | 0.03594 | 0.1633 |
| Rosenbrock | raw | clean | random | 10 | 43.6 | 0.8391 | 0.8455 |
| Rosenbrock | raw | clean | tpe | 12 | 43 | 1.424 | 1.258 |
| Rosenbrock | raw | clean | tpe_w_smooth | 24 | 36.25 | 1.31 | 1.191 |
| Rosenbrock | raw | clean | tpe_w_smooth_inv | 24 | 35.58 | 1.482 | 1.193 |
| Rosenbrock | raw | clean | tpe_w_sign | 16 | 36.88 | 1.357 | 1.203 |
| Rosenbrock | raw | clean | tpe_w_sign_inv | 24 | 37.08 | 1.477 | 1.229 |
| Rosenbrock | raw | clean | tpe_gp | 34 | 29.88 | 0.3778 | 0.8284 |
| Rosenbrock | raw | clean | tpe_gp_w | 22 | 32.27 | 0.3259 | 0.8928 |
| Rosenbrock | raw | clean | optuna | 28 | 49.64 | 0.4293 | 0.7599 |
| Rosenbrock | raw | noisy_y | random | 10 | 43.6 | 0.8407 | 0.8428 |
| Rosenbrock | raw | noisy_y | tpe | 12 | 38.5 | 1.471 | 1.297 |
| Rosenbrock | raw | noisy_y | tpe_w_smooth | 24 | 34.92 | 1.314 | 1.208 |
| Rosenbrock | raw | noisy_y | tpe_w_smooth_inv | 22 | 36.18 | 1.521 | 1.223 |
| Rosenbrock | raw | noisy_y | tpe_w_sign | 14 | 37.57 | 1.331 | 1.232 |
| Rosenbrock | raw | noisy_y | tpe_w_sign_inv | 22 | 35.36 | 1.497 | 1.252 |
| Rosenbrock | raw | noisy_y | tpe_gp | 26 | 24.38 | 0.4452 | 0.9439 |
| Rosenbrock | raw | noisy_y | tpe_gp_w | 20 | 33.7 | 0.3036 | 0.9156 |
| Rosenbrock | raw | noisy_y | optuna | 24 | 48.92 | 0.4525 | 0.7638 |
| Rosenbrock | norm | clean | random | 10 | 43.6 | 0.8391 | 0.8455 |
| Rosenbrock | norm | clean | tpe | 12 | 43 | 1.424 | 1.258 |
| Rosenbrock | norm | clean | tpe_w_smooth | 24 | 36.25 | 1.31 | 1.191 |
| Rosenbrock | norm | clean | tpe_w_smooth_inv | 24 | 35.58 | 1.482 | 1.193 |
| Rosenbrock | norm | clean | tpe_w_sign | 16 | 36.88 | 1.357 | 1.203 |
| Rosenbrock | norm | clean | tpe_w_sign_inv | 24 | 37.08 | 1.477 | 1.229 |
| Rosenbrock | norm | clean | tpe_gp | 22 | 39.18 | 1.412 | 1.214 |
| Rosenbrock | norm | clean | tpe_gp_w | 14 | 34.43 | 1.445 | 1.253 |
| Rosenbrock | norm | clean | optuna | 28 | 49.64 | 0.4293 | 0.7599 |
| Rosenbrock | norm | noisy_y | random | 10 | 43.6 | 0.8407 | 0.8428 |
| Rosenbrock | norm | noisy_y | tpe | 12 | 38.5 | 1.471 | 1.297 |
| Rosenbrock | norm | noisy_y | tpe_w_smooth | 24 | 34.92 | 1.314 | 1.208 |
| Rosenbrock | norm | noisy_y | tpe_w_smooth_inv | 22 | 36.18 | 1.521 | 1.223 |
| Rosenbrock | norm | noisy_y | tpe_w_sign | 14 | 37.57 | 1.331 | 1.232 |
| Rosenbrock | norm | noisy_y | tpe_w_sign_inv | 22 | 35.36 | 1.497 | 1.252 |
| Rosenbrock | norm | noisy_y | tpe_gp | 22 | 41 | 1.412 | 1.232 |
| Rosenbrock | norm | noisy_y | tpe_gp_w | 12 | 37.83 | 1.486 | 1.265 |
| Rosenbrock | norm | noisy_y | optuna | 24 | 48.92 | 0.4525 | 0.7638 |
| Rastrigin | raw | clean | random | 2 | 13 | 6.103 | 1.517 |
| Rastrigin | raw | clean | tpe | 26 | 49.23 | 2.52 | 1.332 |
| Rastrigin | raw | clean | tpe_w_smooth | 14 | 53.43 | 2.949 | 1.481 |
| Rastrigin | raw | clean | tpe_w_smooth_inv | 24 | 37.92 | 2.556 | 1.26 |
| Rastrigin | raw | clean | tpe_w_sign | 16 | 38 | 2.853 | 1.37 |
| Rastrigin | raw | clean | tpe_w_sign_inv | 12 | 43.33 | 2.859 | 1.427 |
| Rastrigin | raw | clean | tpe_gp | 6 | 33 | 3.775 | 1.593 |
| Rastrigin | raw | clean | tpe_gp_w | 8 | 52.25 | 3.779 | 1.563 |
| Rastrigin | raw | clean | optuna | 6 | 51.67 | 2.979 | 1.132 |
| Rastrigin | raw | noisy_y | random | 2 | 13 | 6.112 | 1.565 |
| Rastrigin | raw | noisy_y | tpe | 24 | 47.08 | 2.847 | 1.344 |
| Rastrigin | raw | noisy_y | tpe_w_smooth | 8 | 48 | 2.802 | 1.432 |
| Rastrigin | raw | noisy_y | tpe_w_smooth_inv | 22 | 40.27 | 2.636 | 1.262 |
| Rastrigin | raw | noisy_y | tpe_w_sign | 14 | 34.71 | 2.896 | 1.354 |
| Rastrigin | raw | noisy_y | tpe_w_sign_inv | 8 | 33 | 3.084 | 1.434 |
| Rastrigin | raw | noisy_y | tpe_gp | 8 | 56 | 3.999 | 1.51 |
| Rastrigin | raw | noisy_y | tpe_gp_w | 12 | 45 | 3.717 | 1.523 |
| Rastrigin | raw | noisy_y | optuna | 8 | 41.5 | 2.905 | 1.089 |
| Rastrigin | norm | clean | random | 2 | 13 | 6.103 | 1.517 |
| Rastrigin | norm | clean | tpe | 26 | 49.23 | 2.52 | 1.332 |
| Rastrigin | norm | clean | tpe_w_smooth | 14 | 53.43 | 2.949 | 1.481 |
| Rastrigin | norm | clean | tpe_w_smooth_inv | 24 | 37.92 | 2.556 | 1.26 |
| Rastrigin | norm | clean | tpe_w_sign | 16 | 38 | 2.853 | 1.37 |
| Rastrigin | norm | clean | tpe_w_sign_inv | 12 | 43.33 | 2.859 | 1.427 |
| Rastrigin | norm | clean | tpe_gp | 10 | 44.4 | 2.184 | 1.241 |
| Rastrigin | norm | clean | tpe_gp_w | 20 | 36.8 | 2.629 | 1.341 |
| Rastrigin | norm | clean | optuna | 6 | 51.67 | 2.979 | 1.132 |
| Rastrigin | norm | noisy_y | random | 2 | 13 | 6.112 | 1.565 |
| Rastrigin | norm | noisy_y | tpe | 24 | 47.08 | 2.847 | 1.344 |
| Rastrigin | norm | noisy_y | tpe_w_smooth | 8 | 48 | 2.802 | 1.432 |
| Rastrigin | norm | noisy_y | tpe_w_smooth_inv | 22 | 40.27 | 2.636 | 1.262 |
| Rastrigin | norm | noisy_y | tpe_w_sign | 14 | 34.71 | 2.896 | 1.354 |
| Rastrigin | norm | noisy_y | tpe_w_sign_inv | 8 | 33 | 3.084 | 1.434 |
| Rastrigin | norm | noisy_y | tpe_gp | 14 | 39.71 | 2.217 | 1.206 |
| Rastrigin | norm | noisy_y | tpe_gp_w | 14 | 38.43 | 2.811 | 1.369 |
| Rastrigin | norm | noisy_y | optuna | 8 | 41.5 | 2.905 | 1.089 |
| Ackley | raw | clean | random | 2 | 13 | 3.034 | 0.7459 |
| Ackley | raw | clean | tpe | 66 | 41.12 | 0.8791 | 0.2804 |
| Ackley | raw | clean | tpe_w_smooth | 72 | 40.19 | 0.7253 | 0.2363 |
| Ackley | raw | clean | tpe_w_smooth_inv | 56 | 35.14 | 1.179 | 0.3871 |
| Ackley | raw | clean | tpe_w_sign | 72 | 34.94 | 0.736 | 0.2358 |
| Ackley | raw | clean | tpe_w_sign_inv | 52 | 35.38 | 1.233 | 0.4394 |
| Ackley | raw | clean | tpe_gp | 84 | 31.95 | 0.4128 | 0.133 |
| Ackley | raw | clean | tpe_gp_w | 78 | 35.26 | 0.58 | 0.1921 |
| Ackley | raw | clean | optuna | 24 | 53.67 | 0.9895 | 0.1624 |
| Ackley | raw | noisy_y | random | 2 | 13 | 3.035 | 0.7555 |
| Ackley | raw | noisy_y | tpe | 68 | 36.65 | 0.8947 | 0.2956 |
| Ackley | raw | noisy_y | tpe_w_smooth | 70 | 35.97 | 0.7765 | 0.2475 |
| Ackley | raw | noisy_y | tpe_w_smooth_inv | 70 | 39.69 | 0.9995 | 0.3476 |
| Ackley | raw | noisy_y | tpe_w_sign | 64 | 36.69 | 0.9471 | 0.31 |
| Ackley | raw | noisy_y | tpe_w_sign_inv | 60 | 33.97 | 1.199 | 0.4214 |
| Ackley | raw | noisy_y | tpe_gp | 84 | 28.83 | 0.3117 | 0.09047 |
| Ackley | raw | noisy_y | tpe_gp_w | 82 | 35.44 | 0.591 | 0.2044 |
| Ackley | raw | noisy_y | optuna | 26 | 50.85 | 0.9607 | 0.1505 |
| Ackley | norm | clean | random | 2 | 13 | 3.034 | 0.7459 |
| Ackley | norm | clean | tpe | 66 | 41.12 | 0.8791 | 0.2804 |
| Ackley | norm | clean | tpe_w_smooth | 72 | 40.19 | 0.7253 | 0.2363 |
| Ackley | norm | clean | tpe_w_smooth_inv | 56 | 35.14 | 1.179 | 0.3871 |
| Ackley | norm | clean | tpe_w_sign | 72 | 34.94 | 0.736 | 0.2358 |
| Ackley | norm | clean | tpe_w_sign_inv | 52 | 35.38 | 1.233 | 0.4394 |
| Ackley | norm | clean | tpe_gp | 62 | 34.23 | 1.01 | 0.3142 |
| Ackley | norm | clean | tpe_gp_w | 68 | 34.76 | 0.8358 | 0.2625 |
| Ackley | norm | clean | optuna | 24 | 53.67 | 0.9895 | 0.1624 |
| Ackley | norm | noisy_y | random | 2 | 13 | 3.035 | 0.7555 |
| Ackley | norm | noisy_y | tpe | 68 | 36.65 | 0.8947 | 0.2956 |
| Ackley | norm | noisy_y | tpe_w_smooth | 70 | 35.97 | 0.7765 | 0.2475 |
| Ackley | norm | noisy_y | tpe_w_smooth_inv | 70 | 39.69 | 0.9995 | 0.3476 |
| Ackley | norm | noisy_y | tpe_w_sign | 64 | 36.69 | 0.9471 | 0.31 |
| Ackley | norm | noisy_y | tpe_w_sign_inv | 60 | 33.97 | 1.199 | 0.4214 |
| Ackley | norm | noisy_y | tpe_gp | 64 | 33.38 | 0.965 | 0.2901 |
| Ackley | norm | noisy_y | tpe_gp_w | 68 | 39.06 | 0.8926 | 0.2965 |
| Ackley | norm | noisy_y | optuna | 26 | 50.85 | 0.9607 | 0.1505 |

## Полная таблица (все метрики, все ячейки)

| function | scale | data | algorithm | success_rate_% | steps_mean | steps_std | final_dist_y_mean | final_dist_y_std | final_dist_y_median | final_dist_x_mean | final_dist_x_std |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Sphere | raw | clean | random | 0 |  |  | 0.5264 | 0.5564 | 0.2991 | 0.6377 | 0.346 |
| Sphere | raw | clean | tpe | 46 | 47.13 | 14.05 | 0.06937 | 0.2085 | 0.002301 | 0.1483 | 0.2177 |
| Sphere | raw | clean | tpe_w_smooth | 48 | 47.96 | 14.77 | 0.04871 | 0.1163 | 0.001511 | 0.1305 | 0.178 |
| Sphere | raw | clean | tpe_w_smooth_inv | 58 | 44.66 | 13.94 | 0.04728 | 0.1572 | 0.0003775 | 0.1008 | 0.1927 |
| Sphere | raw | clean | tpe_w_sign | 42 | 48.19 | 17.23 | 0.1302 | 0.4366 | 0.005844 | 0.1826 | 0.3113 |
| Sphere | raw | clean | tpe_w_sign_inv | 56 | 47.96 | 17.53 | 0.06441 | 0.1746 | 0.0003601 | 0.1262 | 0.2202 |
| Sphere | raw | clean | tpe_gp | 94 | 40.66 | 15.68 | 0.001039 | 0.004589 | 7.124e-05 | 0.01548 | 0.02828 |
| Sphere | raw | clean | tpe_gp_w | 96 | 36.08 | 11.72 | 0.0002211 | 0.0006029 | 7.179e-05 | 0.01059 | 0.01044 |
| Sphere | raw | clean | optuna | 4 | 48 | 15 | 0.03237 | 0.04503 | 0.0202 | 0.1559 | 0.08978 |
| Sphere | raw | noisy_y | random | 0 |  |  | 0.5264 | 0.5564 | 0.2991 | 0.6377 | 0.346 |
| Sphere | raw | noisy_y | tpe | 34 | 46.47 | 14.22 | 0.06489 | 0.1793 | 0.005231 | 0.1622 | 0.1964 |
| Sphere | raw | noisy_y | tpe_w_smooth | 26 | 54.92 | 16.55 | 0.0478 | 0.1159 | 0.007428 | 0.1458 | 0.1629 |
| Sphere | raw | noisy_y | tpe_w_smooth_inv | 38 | 38.63 | 16.41 | 0.05103 | 0.1644 | 0.002661 | 0.1246 | 0.1885 |
| Sphere | raw | noisy_y | tpe_w_sign | 26 | 49.69 | 12.82 | 0.1488 | 0.4219 | 0.01131 | 0.2274 | 0.3116 |
| Sphere | raw | noisy_y | tpe_w_sign_inv | 36 | 41.17 | 17.64 | 0.0817 | 0.1839 | 0.003679 | 0.1641 | 0.234 |
| Sphere | raw | noisy_y | tpe_gp | 66 | 40.88 | 16.57 | 0.002279 | 0.002965 | 0.001339 | 0.04178 | 0.02309 |
| Sphere | raw | noisy_y | tpe_gp_w | 70 | 43.66 | 17.09 | 0.001662 | 0.002104 | 0.000865 | 0.03505 | 0.02083 |
| Sphere | raw | noisy_y | optuna | 6 | 56 | 16.67 | 0.03594 | 0.04944 | 0.02048 | 0.1633 | 0.09634 |
| Sphere | norm | clean | random | 0 |  |  | 0.5264 | 0.5564 | 0.2991 | 0.6377 | 0.346 |
| Sphere | norm | clean | tpe | 46 | 47.13 | 14.05 | 0.06937 | 0.2085 | 0.002301 | 0.1483 | 0.2177 |
| Sphere | norm | clean | tpe_w_smooth | 48 | 47.96 | 14.77 | 0.04871 | 0.1163 | 0.001511 | 0.1305 | 0.178 |
| Sphere | norm | clean | tpe_w_smooth_inv | 58 | 44.66 | 13.94 | 0.04728 | 0.1572 | 0.0003775 | 0.1008 | 0.1927 |
| Sphere | norm | clean | tpe_w_sign | 42 | 48.19 | 17.23 | 0.1302 | 0.4366 | 0.005844 | 0.1826 | 0.3113 |
| Sphere | norm | clean | tpe_w_sign_inv | 56 | 47.96 | 17.53 | 0.06441 | 0.1746 | 0.0003601 | 0.1262 | 0.2202 |
| Sphere | norm | clean | tpe_gp | 50 | 49.64 | 14.51 | 0.0245 | 0.04957 | 0.00154 | 0.09704 | 0.1228 |
| Sphere | norm | clean | tpe_gp_w | 50 | 44.2 | 18.38 | 0.01586 | 0.06683 | 0.001062 | 0.06417 | 0.1084 |
| Sphere | norm | clean | optuna | 4 | 48 | 15 | 0.03237 | 0.04503 | 0.0202 | 0.1559 | 0.08978 |
| Sphere | norm | noisy_y | random | 0 |  |  | 0.5264 | 0.5564 | 0.2991 | 0.6377 | 0.346 |
| Sphere | norm | noisy_y | tpe | 34 | 46.47 | 14.22 | 0.06489 | 0.1793 | 0.005231 | 0.1622 | 0.1964 |
| Sphere | norm | noisy_y | tpe_w_smooth | 26 | 54.92 | 16.55 | 0.0478 | 0.1159 | 0.007428 | 0.1458 | 0.1629 |
| Sphere | norm | noisy_y | tpe_w_smooth_inv | 38 | 38.63 | 16.41 | 0.05103 | 0.1644 | 0.002661 | 0.1246 | 0.1885 |
| Sphere | norm | noisy_y | tpe_w_sign | 26 | 49.69 | 12.82 | 0.1488 | 0.4219 | 0.01131 | 0.2274 | 0.3116 |
| Sphere | norm | noisy_y | tpe_w_sign_inv | 36 | 41.17 | 17.64 | 0.0817 | 0.1839 | 0.003679 | 0.1641 | 0.234 |
| Sphere | norm | noisy_y | tpe_gp | 34 | 49.59 | 18.86 | 0.02329 | 0.05252 | 0.005127 | 0.1035 | 0.1122 |
| Sphere | norm | noisy_y | tpe_gp_w | 36 | 34.11 | 15.01 | 0.02954 | 0.08725 | 0.004375 | 0.1089 | 0.133 |
| Sphere | norm | noisy_y | optuna | 6 | 56 | 16.67 | 0.03594 | 0.04944 | 0.02048 | 0.1633 | 0.09634 |
| Rosenbrock | raw | clean | random | 10 | 43.6 | 10.67 | 0.8391 | 0.8469 | 0.5392 | 0.8455 | 0.5613 |
| Rosenbrock | raw | clean | tpe | 12 | 43 | 23.12 | 1.424 | 1.823 | 0.4437 | 1.258 | 0.6943 |
| Rosenbrock | raw | clean | tpe_w_smooth | 24 | 36.25 | 12.74 | 1.31 | 1.63 | 0.6166 | 1.191 | 0.7422 |
| Rosenbrock | raw | clean | tpe_w_smooth_inv | 24 | 35.58 | 13.67 | 1.482 | 1.943 | 0.6136 | 1.193 | 0.824 |
| Rosenbrock | raw | clean | tpe_w_sign | 16 | 36.88 | 11.44 | 1.357 | 1.789 | 0.5211 | 1.203 | 0.7127 |
| Rosenbrock | raw | clean | tpe_w_sign_inv | 24 | 37.08 | 13.56 | 1.477 | 1.81 | 0.7236 | 1.229 | 0.7438 |
| Rosenbrock | raw | clean | tpe_gp | 34 | 29.88 | 15.04 | 0.3778 | 1.007 | 0.1564 | 0.8284 | 0.6847 |
| Rosenbrock | raw | clean | tpe_gp_w | 22 | 32.27 | 12.47 | 0.3259 | 0.3776 | 0.2441 | 0.8928 | 0.5236 |
| Rosenbrock | raw | clean | optuna | 28 | 49.64 | 17.7 | 0.4293 | 0.9123 | 0.2338 | 0.7599 | 0.4676 |
| Rosenbrock | raw | noisy_y | random | 10 | 43.6 | 10.67 | 0.8407 | 0.8469 | 0.5392 | 0.8428 | 0.5601 |
| Rosenbrock | raw | noisy_y | tpe | 12 | 38.5 | 13.85 | 1.471 | 1.798 | 0.6099 | 1.297 | 0.6832 |
| Rosenbrock | raw | noisy_y | tpe_w_smooth | 24 | 34.92 | 9.734 | 1.314 | 1.651 | 0.6079 | 1.208 | 0.7287 |
| Rosenbrock | raw | noisy_y | tpe_w_smooth_inv | 22 | 36.18 | 12.15 | 1.521 | 1.951 | 0.5535 | 1.223 | 0.8174 |
| Rosenbrock | raw | noisy_y | tpe_w_sign | 14 | 37.57 | 13.08 | 1.331 | 1.808 | 0.5096 | 1.232 | 0.696 |
| Rosenbrock | raw | noisy_y | tpe_w_sign_inv | 22 | 35.36 | 13.12 | 1.497 | 1.799 | 0.7216 | 1.252 | 0.7263 |
| Rosenbrock | raw | noisy_y | tpe_gp | 26 | 24.38 | 6.475 | 0.4452 | 0.9877 | 0.2732 | 0.9439 | 0.6302 |
| Rosenbrock | raw | noisy_y | tpe_gp_w | 20 | 33.7 | 16.6 | 0.3036 | 0.2588 | 0.2397 | 0.9156 | 0.467 |
| Rosenbrock | raw | noisy_y | optuna | 24 | 48.92 | 18.83 | 0.4525 | 0.9117 | 0.2476 | 0.7638 | 0.5087 |
| Rosenbrock | norm | clean | random | 10 | 43.6 | 10.67 | 0.8391 | 0.8469 | 0.5392 | 0.8455 | 0.5613 |
| Rosenbrock | norm | clean | tpe | 12 | 43 | 23.12 | 1.424 | 1.823 | 0.4437 | 1.258 | 0.6943 |
| Rosenbrock | norm | clean | tpe_w_smooth | 24 | 36.25 | 12.74 | 1.31 | 1.63 | 0.6166 | 1.191 | 0.7422 |
| Rosenbrock | norm | clean | tpe_w_smooth_inv | 24 | 35.58 | 13.67 | 1.482 | 1.943 | 0.6136 | 1.193 | 0.824 |
| Rosenbrock | norm | clean | tpe_w_sign | 16 | 36.88 | 11.44 | 1.357 | 1.789 | 0.5211 | 1.203 | 0.7127 |
| Rosenbrock | norm | clean | tpe_w_sign_inv | 24 | 37.08 | 13.56 | 1.477 | 1.81 | 0.7236 | 1.229 | 0.7438 |
| Rosenbrock | norm | clean | tpe_gp | 22 | 39.18 | 15.27 | 1.412 | 1.778 | 0.4518 | 1.214 | 0.7687 |
| Rosenbrock | norm | clean | tpe_gp_w | 14 | 34.43 | 14.12 | 1.445 | 1.853 | 0.5155 | 1.253 | 0.7706 |
| Rosenbrock | norm | clean | optuna | 28 | 49.64 | 17.7 | 0.4293 | 0.9123 | 0.2338 | 0.7599 | 0.4676 |
| Rosenbrock | norm | noisy_y | random | 10 | 43.6 | 10.67 | 0.8407 | 0.8469 | 0.5392 | 0.8428 | 0.5601 |
| Rosenbrock | norm | noisy_y | tpe | 12 | 38.5 | 13.85 | 1.471 | 1.798 | 0.6099 | 1.297 | 0.6832 |
| Rosenbrock | norm | noisy_y | tpe_w_smooth | 24 | 34.92 | 9.734 | 1.314 | 1.651 | 0.6079 | 1.208 | 0.7287 |
| Rosenbrock | norm | noisy_y | tpe_w_smooth_inv | 22 | 36.18 | 12.15 | 1.521 | 1.951 | 0.5535 | 1.223 | 0.8174 |
| Rosenbrock | norm | noisy_y | tpe_w_sign | 14 | 37.57 | 13.08 | 1.331 | 1.808 | 0.5096 | 1.232 | 0.696 |
| Rosenbrock | norm | noisy_y | tpe_w_sign_inv | 22 | 35.36 | 13.12 | 1.497 | 1.799 | 0.7216 | 1.252 | 0.7263 |
| Rosenbrock | norm | noisy_y | tpe_gp | 22 | 41 | 18.62 | 1.412 | 1.771 | 0.5109 | 1.232 | 0.7602 |
| Rosenbrock | norm | noisy_y | tpe_gp_w | 12 | 37.83 | 12.42 | 1.486 | 1.87 | 0.4912 | 1.265 | 0.7734 |
| Rosenbrock | norm | noisy_y | optuna | 24 | 48.92 | 18.83 | 0.4525 | 0.9117 | 0.2476 | 0.7638 | 0.5087 |
| Rastrigin | raw | clean | random | 2 | 13 | 0 | 6.103 | 3.105 | 5.759 | 1.517 | 0.6858 |
| Rastrigin | raw | clean | tpe | 26 | 49.23 | 17.35 | 2.52 | 2.16 | 1.994 | 1.332 | 0.7569 |
| Rastrigin | raw | clean | tpe_w_smooth | 14 | 53.43 | 17.24 | 2.949 | 2.64 | 2.009 | 1.481 | 0.7071 |
| Rastrigin | raw | clean | tpe_w_smooth_inv | 24 | 37.92 | 14.41 | 2.556 | 2.772 | 1.594 | 1.26 | 0.7896 |
| Rastrigin | raw | clean | tpe_w_sign | 16 | 38 | 14.58 | 2.853 | 2.625 | 2.051 | 1.37 | 0.8704 |
| Rastrigin | raw | clean | tpe_w_sign_inv | 12 | 43.33 | 15.94 | 2.859 | 2.571 | 2.003 | 1.427 | 0.7185 |
| Rastrigin | raw | clean | tpe_gp | 6 | 33 | 9.416 | 3.775 | 2.954 | 2.349 | 1.593 | 0.7583 |
| Rastrigin | raw | clean | tpe_gp_w | 8 | 52.25 | 11.69 | 3.779 | 2.566 | 3.337 | 1.563 | 0.7965 |
| Rastrigin | raw | clean | optuna | 6 | 51.67 | 16.78 | 2.979 | 1.592 | 2.665 | 1.132 | 0.6163 |
| Rastrigin | raw | noisy_y | random | 2 | 13 | 0 | 6.112 | 3.106 | 5.759 | 1.565 | 0.6944 |
| Rastrigin | raw | noisy_y | tpe | 24 | 47.08 | 19.4 | 2.847 | 2.507 | 1.932 | 1.344 | 0.8752 |
| Rastrigin | raw | noisy_y | tpe_w_smooth | 8 | 48 | 11.42 | 2.802 | 2.234 | 2.018 | 1.432 | 0.6664 |
| Rastrigin | raw | noisy_y | tpe_w_smooth_inv | 22 | 40.27 | 13.49 | 2.636 | 2.632 | 1.309 | 1.262 | 0.8131 |
| Rastrigin | raw | noisy_y | tpe_w_sign | 14 | 34.71 | 8.762 | 2.896 | 2.895 | 2.035 | 1.354 | 0.843 |
| Rastrigin | raw | noisy_y | tpe_w_sign_inv | 8 | 33 | 6.285 | 3.084 | 2.384 | 2.221 | 1.434 | 0.7045 |
| Rastrigin | raw | noisy_y | tpe_gp | 8 | 56 | 9.138 | 3.999 | 3.419 | 2.376 | 1.51 | 0.77 |
| Rastrigin | raw | noisy_y | tpe_gp_w | 12 | 45 | 14.78 | 3.717 | 2.556 | 3.934 | 1.523 | 0.7939 |
| Rastrigin | raw | noisy_y | optuna | 8 | 41.5 | 14.15 | 2.905 | 1.601 | 2.694 | 1.089 | 0.5808 |
| Rastrigin | norm | clean | random | 2 | 13 | 0 | 6.103 | 3.105 | 5.759 | 1.517 | 0.6858 |
| Rastrigin | norm | clean | tpe | 26 | 49.23 | 17.35 | 2.52 | 2.16 | 1.994 | 1.332 | 0.7569 |
| Rastrigin | norm | clean | tpe_w_smooth | 14 | 53.43 | 17.24 | 2.949 | 2.64 | 2.009 | 1.481 | 0.7071 |
| Rastrigin | norm | clean | tpe_w_smooth_inv | 24 | 37.92 | 14.41 | 2.556 | 2.772 | 1.594 | 1.26 | 0.7896 |
| Rastrigin | norm | clean | tpe_w_sign | 16 | 38 | 14.58 | 2.853 | 2.625 | 2.051 | 1.37 | 0.8704 |
| Rastrigin | norm | clean | tpe_w_sign_inv | 12 | 43.33 | 15.94 | 2.859 | 2.571 | 2.003 | 1.427 | 0.7185 |
| Rastrigin | norm | clean | tpe_gp | 10 | 44.4 | 7.499 | 2.184 | 1.947 | 1.93 | 1.241 | 0.6708 |
| Rastrigin | norm | clean | tpe_gp_w | 20 | 36.8 | 18.76 | 2.629 | 2.495 | 1.995 | 1.341 | 0.816 |
| Rastrigin | norm | clean | optuna | 6 | 51.67 | 16.78 | 2.979 | 1.592 | 2.665 | 1.132 | 0.6163 |
| Rastrigin | norm | noisy_y | random | 2 | 13 | 0 | 6.112 | 3.106 | 5.759 | 1.565 | 0.6944 |
| Rastrigin | norm | noisy_y | tpe | 24 | 47.08 | 19.4 | 2.847 | 2.507 | 1.932 | 1.344 | 0.8752 |
| Rastrigin | norm | noisy_y | tpe_w_smooth | 8 | 48 | 11.42 | 2.802 | 2.234 | 2.018 | 1.432 | 0.6664 |
| Rastrigin | norm | noisy_y | tpe_w_smooth_inv | 22 | 40.27 | 13.49 | 2.636 | 2.632 | 1.309 | 1.262 | 0.8131 |
| Rastrigin | norm | noisy_y | tpe_w_sign | 14 | 34.71 | 8.762 | 2.896 | 2.895 | 2.035 | 1.354 | 0.843 |
| Rastrigin | norm | noisy_y | tpe_w_sign_inv | 8 | 33 | 6.285 | 3.084 | 2.384 | 2.221 | 1.434 | 0.7045 |
| Rastrigin | norm | noisy_y | tpe_gp | 14 | 39.71 | 7.832 | 2.217 | 2.026 | 1.27 | 1.206 | 0.6892 |
| Rastrigin | norm | noisy_y | tpe_gp_w | 14 | 38.43 | 14.15 | 2.811 | 2.367 | 2.074 | 1.369 | 0.7697 |
| Rastrigin | norm | noisy_y | optuna | 8 | 41.5 | 14.15 | 2.905 | 1.601 | 2.694 | 1.089 | 0.5808 |
| Ackley | raw | clean | random | 2 | 13 | 0 | 3.034 | 1.048 | 3.1 | 0.7459 | 0.4371 |
| Ackley | raw | clean | tpe | 66 | 41.12 | 16.27 | 0.8791 | 1.195 | 0.1614 | 0.2804 | 0.4242 |
| Ackley | raw | clean | tpe_w_smooth | 72 | 40.19 | 16.11 | 0.7253 | 1.248 | 0.1111 | 0.2363 | 0.4841 |
| Ackley | raw | clean | tpe_w_smooth_inv | 56 | 35.14 | 13.11 | 1.179 | 1.483 | 0.2099 | 0.3871 | 0.5454 |
| Ackley | raw | clean | tpe_w_sign | 72 | 34.94 | 11.14 | 0.736 | 1.197 | 0.06786 | 0.2358 | 0.4403 |
| Ackley | raw | clean | tpe_w_sign_inv | 52 | 35.38 | 15.84 | 1.233 | 1.511 | 0.3887 | 0.4394 | 0.5949 |
| Ackley | raw | clean | tpe_gp | 84 | 31.95 | 12.33 | 0.4128 | 0.8392 | 0.07085 | 0.133 | 0.3103 |
| Ackley | raw | clean | tpe_gp_w | 78 | 35.26 | 13.28 | 0.58 | 0.9576 | 0.1464 | 0.1921 | 0.3591 |
| Ackley | raw | clean | optuna | 24 | 53.67 | 15.13 | 0.9895 | 0.5845 | 0.9683 | 0.1624 | 0.1213 |
| Ackley | raw | noisy_y | random | 2 | 13 | 0 | 3.035 | 1.049 | 3.1 | 0.7555 | 0.4439 |
| Ackley | raw | noisy_y | tpe | 68 | 36.65 | 11.88 | 0.8947 | 1.249 | 0.1408 | 0.2956 | 0.47 |
| Ackley | raw | noisy_y | tpe_w_smooth | 70 | 35.97 | 11.42 | 0.7765 | 1.184 | 0.09923 | 0.2475 | 0.4276 |
| Ackley | raw | noisy_y | tpe_w_smooth_inv | 70 | 39.69 | 16.91 | 0.9995 | 1.504 | 0.127 | 0.3476 | 0.5835 |
| Ackley | raw | noisy_y | tpe_w_sign | 64 | 36.69 | 12.95 | 0.9471 | 1.433 | 0.1273 | 0.31 | 0.5249 |
| Ackley | raw | noisy_y | tpe_w_sign_inv | 60 | 33.97 | 13.67 | 1.199 | 1.534 | 0.1707 | 0.4214 | 0.5937 |
| Ackley | raw | noisy_y | tpe_gp | 84 | 28.83 | 10.18 | 0.3117 | 0.6216 | 0.08611 | 0.09047 | 0.2183 |
| Ackley | raw | noisy_y | tpe_gp_w | 82 | 35.44 | 15.79 | 0.591 | 1.007 | 0.1294 | 0.2044 | 0.3731 |
| Ackley | raw | noisy_y | optuna | 26 | 50.85 | 16.29 | 0.9607 | 0.5653 | 0.8654 | 0.1505 | 0.07041 |
| Ackley | norm | clean | random | 2 | 13 | 0 | 3.034 | 1.048 | 3.1 | 0.7459 | 0.4371 |
| Ackley | norm | clean | tpe | 66 | 41.12 | 16.27 | 0.8791 | 1.195 | 0.1614 | 0.2804 | 0.4242 |
| Ackley | norm | clean | tpe_w_smooth | 72 | 40.19 | 16.11 | 0.7253 | 1.248 | 0.1111 | 0.2363 | 0.4841 |
| Ackley | norm | clean | tpe_w_smooth_inv | 56 | 35.14 | 13.11 | 1.179 | 1.483 | 0.2099 | 0.3871 | 0.5454 |
| Ackley | norm | clean | tpe_w_sign | 72 | 34.94 | 11.14 | 0.736 | 1.197 | 0.06786 | 0.2358 | 0.4403 |
| Ackley | norm | clean | tpe_w_sign_inv | 52 | 35.38 | 15.84 | 1.233 | 1.511 | 0.3887 | 0.4394 | 0.5949 |
| Ackley | norm | clean | tpe_gp | 62 | 34.23 | 11.87 | 1.01 | 1.269 | 0.1366 | 0.3142 | 0.4415 |
| Ackley | norm | clean | tpe_gp_w | 68 | 34.76 | 15.47 | 0.8358 | 1.2 | 0.09499 | 0.2625 | 0.4201 |
| Ackley | norm | clean | optuna | 24 | 53.67 | 15.13 | 0.9895 | 0.5845 | 0.9683 | 0.1624 | 0.1213 |
| Ackley | norm | noisy_y | random | 2 | 13 | 0 | 3.035 | 1.049 | 3.1 | 0.7555 | 0.4439 |
| Ackley | norm | noisy_y | tpe | 68 | 36.65 | 11.88 | 0.8947 | 1.249 | 0.1408 | 0.2956 | 0.47 |
| Ackley | norm | noisy_y | tpe_w_smooth | 70 | 35.97 | 11.42 | 0.7765 | 1.184 | 0.09923 | 0.2475 | 0.4276 |
| Ackley | norm | noisy_y | tpe_w_smooth_inv | 70 | 39.69 | 16.91 | 0.9995 | 1.504 | 0.127 | 0.3476 | 0.5835 |
| Ackley | norm | noisy_y | tpe_w_sign | 64 | 36.69 | 12.95 | 0.9471 | 1.433 | 0.1273 | 0.31 | 0.5249 |
| Ackley | norm | noisy_y | tpe_w_sign_inv | 60 | 33.97 | 13.67 | 1.199 | 1.534 | 0.1707 | 0.4214 | 0.5937 |
| Ackley | norm | noisy_y | tpe_gp | 64 | 33.38 | 12.14 | 0.965 | 1.346 | 0.1473 | 0.2901 | 0.4519 |
| Ackley | norm | noisy_y | tpe_gp_w | 68 | 39.06 | 15.87 | 0.8926 | 1.346 | 0.1188 | 0.2965 | 0.5078 |
| Ackley | norm | noisy_y | optuna | 26 | 50.85 | 16.29 | 0.9607 | 0.5653 | 0.8654 | 0.1505 | 0.07041 |

## Выводы (строго по числам прогона)

1. **Базовый `tpe` осмыслен:** средний success 36.0% против random 3.5% и optuna 15.8% (порог success строгий, поэтому смотрите и на final_dist_y).
2. **Нормализация цели не влияет на TPE и на все формы w(x)** (gap=0, инвариантность), и **важна только для GP** (gap 1.6).
3. **GP-переранжирование — единственная модификация со значимым эффектом:** `tpe_gp` даёт 4 значимых улучшений, `tpe_gp_w` — 3 (гладкая Sphere и овражная Rosenbrock).
4. **Ни одна из 4 форм w(x) не даёт значимого улучшения** (`tpe_w_smooth/smooth_inv/sign/sign_inv`: всего 0 значимых), хотя по СРЕДНИМ `tpe_w_smooth` «бьёт» baseline в 87.5% ячеек — яркий пример, что средние обманывают.
5. **Комбинация `tpe_gp_w` (GP+вес, аналог gTPE)** не превосходит чистый `tpe_gp` — выигрыш идёт от GP, а не от градиентного веса.

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
