# RESULTS — табличные результаты и графики

> Сгенерировано автоматически из `results/tables/*.csv` (реальный прогон `run.py`).

## Конфигурация прогона

```json
{
  "seeds": 50,
  "n_init": 10,
  "max_evals": 100,
  "n_candidates": 24,
  "gamma": 0.2,
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
    "tpe_refine",
    "tpe_gp",
    "tpe_gp_w",
    "tpe_gp_refine",
    "optuna"
  ]
}
```

## Сводка: средний success_rate по алгоритмам (по всем ячейкам)

| algorithm | avg_success_% |
|---|---|
| optuna | 21.2 |
| random | 4 |
| tpe | 25 |
| tpe_gp | 40.9 |
| tpe_gp_refine | 62.1 |
| tpe_gp_w | 34.5 |
| tpe_refine | 63.8 |
| tpe_w_sign | 22 |
| tpe_w_sign_inv | 29.5 |
| tpe_w_smooth | 21.2 |
| tpe_w_smooth_inv | 29.2 |

## Авто-выводы (из чисел этого прогона)

- **Инвариантность нормализации для чистого rank-based `tpe`** (clean): максимальный |raw − norm| по final_dist_y = **0** → при ~0 это строго подтверждает: монотонно-аффинное масштабирование цели НЕ влияет на ранговый TPE.
- **Формы w(x) тоже инвариантны** (`tpe_w_smooth` gap = 0): вес считается по min-max-рангу норм градиента, и постоянный множитель от нормализации сокращается. **Масштабо-зависим только GP** (`tpe_gp` gap = 1.37): член `−μ+βσ` в y-единицах конкурирует с лог-плотностью. Вывод: нормализация бесполезна для всех rank/вес-вариантов TPE и важна лишь для GP.
- **Как часто модификация бьёт baseline `tpe`** (доля ячеек, % по final_dist_y):
  - `optuna`: 100.0%
  - `random`: 25.0%
  - `tpe_gp`: 75.0%
  - `tpe_gp_refine`: 100.0%
  - `tpe_gp_w`: 100.0%
  - `tpe_refine`: 100.0%
  - `tpe_w_sign`: 25.0%
  - `tpe_w_sign_inv`: 87.5%
  - `tpe_w_smooth`: 62.5%
  - `tpe_w_smooth_inv`: 87.5%

## Статистическая значимость (парный Уилкоксон vs `tpe`, поправка Холма)

Из 160 сравнений значимы (p_holm<0.05): **42 в пользу модификации**, 6 против. Остальные различия статистически не подтверждены.

Значимые улучшения над baseline `tpe`:

| function | scale | data | algorithm | median_delta | p_holm |
|---|---|---|---|---|---|
| Ackley | norm | clean | optuna | -1.77 | 0.0001104 |
| Ackley | norm | clean | tpe_gp_refine | -0.3842 | 0.000123 |
| Ackley | norm | clean | tpe_refine | -1.31 | 0.001065 |
| Ackley | norm | noisy_y | tpe_gp_refine | -0.222 | 0.002601 |
| Ackley | raw | clean | optuna | -1.77 | 0.0001104 |
| Ackley | raw | clean | tpe_gp | -1.627 | 1.331e-05 |
| Ackley | raw | clean | tpe_gp_refine | -2.098 | 6.127e-07 |
| Ackley | raw | clean | tpe_gp_w | -2.408 | 1.456e-06 |
| Ackley | raw | clean | tpe_refine | -1.31 | 0.001065 |
| Ackley | raw | noisy_y | tpe_gp | -0.6536 | 0.0002287 |
| Ackley | raw | noisy_y | tpe_gp_refine | -1.118 | 5.632e-07 |
| Ackley | raw | noisy_y | tpe_gp_w | -1.109 | 4.44e-05 |
| Rastrigin | norm | noisy_y | tpe_gp_refine | -0.374 | 0.02543 |
| Rastrigin | norm | noisy_y | tpe_refine | -1.03 | 0.003689 |
| Rastrigin | raw | noisy_y | tpe_refine | -1.03 | 0.003689 |
| Rosenbrock | norm | clean | optuna | -0.3723 | 0.001228 |
| Rosenbrock | norm | clean | tpe_refine | -0.209 | 0.02478 |
| Rosenbrock | norm | noisy_y | optuna | -0.4121 | 0.001962 |
| Rosenbrock | norm | noisy_y | tpe_gp_refine | -0.2501 | 0.01354 |
| Rosenbrock | norm | noisy_y | tpe_refine | -0.1962 | 0.03122 |
| Rosenbrock | raw | clean | optuna | -0.3723 | 0.001228 |
| Rosenbrock | raw | clean | tpe_gp | -0.317 | 0.0001042 |
| Rosenbrock | raw | clean | tpe_gp_refine | -0.4561 | 0.0003882 |
| Rosenbrock | raw | clean | tpe_gp_w | -0.3705 | 0.02009 |
| Rosenbrock | raw | clean | tpe_refine | -0.209 | 0.02478 |
| Rosenbrock | raw | noisy_y | optuna | -0.4121 | 0.001962 |
| Rosenbrock | raw | noisy_y | tpe_gp | -0.459 | 0.0001162 |
| Rosenbrock | raw | noisy_y | tpe_gp_refine | -0.4162 | 5.055e-05 |
| Rosenbrock | raw | noisy_y | tpe_gp_w | -0.4542 | 0.005576 |
| Rosenbrock | raw | noisy_y | tpe_refine | -0.1962 | 0.03122 |
| Sphere | norm | clean | tpe_gp_refine | -0.01457 | 2.842e-13 |
| Sphere | norm | clean | tpe_refine | -0.01457 | 5.649e-13 |
| Sphere | norm | noisy_y | tpe_gp_refine | -0.008637 | 2.924e-10 |
| Sphere | norm | noisy_y | tpe_refine | -0.008916 | 2.505e-10 |
| Sphere | raw | clean | tpe_gp | -0.01456 | 6.661e-07 |
| Sphere | raw | clean | tpe_gp_refine | -0.01457 | 3.904e-12 |
| Sphere | raw | clean | tpe_gp_w | -0.0117 | 4.579e-06 |
| Sphere | raw | clean | tpe_refine | -0.01457 | 5.649e-13 |
| Sphere | raw | noisy_y | tpe_gp | -0.006564 | 0.0003079 |
| Sphere | raw | noisy_y | tpe_gp_refine | -0.009669 | 6.455e-10 |
| Sphere | raw | noisy_y | tpe_gp_w | -0.008296 | 0.001171 |
| Sphere | raw | noisy_y | tpe_refine | -0.008916 | 2.505e-10 |

Сколько значимых выигрышей у каждой модификации (из 16 ячеек):

| algorithm | n_significant_wins |
|---|---|
| optuna | 6 |
| random | 0 |
| tpe_gp | 6 |
| tpe_gp_refine | 12 |
| tpe_gp_w | 6 |
| tpe_refine | 12 |
| tpe_w_sign | 0 |
| tpe_w_sign_inv | 0 |
| tpe_w_smooth | 0 |
| tpe_w_smooth_inv | 0 |

## Ablation: каждая модификация против baseline `tpe`

Δ = algo − tpe по final_dist_y (меньше нуля → модификация лучше).

| function | scale | data | algorithm | tpe_final_dist_y | algo_final_dist_y | delta_dist_y(algo-tpe) | better_than_tpe | tpe_success_% | algo_success_% |
|---|---|---|---|---|---|---|---|---|---|
| Ackley | norm | clean | random | 2.043 | 2.843 | 0.8 | False | 32 | 2 |
| Ackley | norm | clean | tpe_w_smooth | 2.043 | 1.429 | -0.6135 | True | 32 | 42 |
| Ackley | norm | clean | tpe_w_smooth_inv | 2.043 | 2.073 | 0.03021 | False | 32 | 30 |
| Ackley | norm | clean | tpe_w_sign | 2.043 | 1.603 | -0.4395 | True | 32 | 44 |
| Ackley | norm | clean | tpe_w_sign_inv | 2.043 | 1.674 | -0.3685 | True | 32 | 40 |
| Ackley | norm | clean | tpe_refine | 2.043 | 0.7898 | -1.253 | True | 32 | 76 |
| Ackley | norm | clean | tpe_gp | 2.043 | 1.278 | -0.7651 | True | 32 | 52 |
| Ackley | norm | clean | tpe_gp_w | 2.043 | 1.388 | -0.6546 | True | 32 | 48 |
| Ackley | norm | clean | tpe_gp_refine | 2.043 | 0.889 | -1.154 | True | 32 | 68 |
| Ackley | norm | clean | optuna | 2.043 | 0.655 | -1.388 | True | 32 | 40 |
| Ackley | norm | noisy_y | random | 1.812 | 2.844 | 1.032 | False | 44 | 2 |
| Ackley | norm | noisy_y | tpe_w_smooth | 1.812 | 1.456 | -0.3566 | True | 44 | 46 |
| Ackley | norm | noisy_y | tpe_w_smooth_inv | 1.812 | 1.62 | -0.1922 | True | 44 | 44 |
| Ackley | norm | noisy_y | tpe_w_sign | 1.812 | 1.476 | -0.3361 | True | 44 | 50 |
| Ackley | norm | noisy_y | tpe_w_sign_inv | 1.812 | 1.533 | -0.2795 | True | 44 | 40 |
| Ackley | norm | noisy_y | tpe_refine | 1.812 | 1.065 | -0.7469 | True | 44 | 66 |
| Ackley | norm | noisy_y | tpe_gp | 1.812 | 1.27 | -0.5424 | True | 44 | 56 |
| Ackley | norm | noisy_y | tpe_gp_w | 1.812 | 1.716 | -0.09636 | True | 44 | 36 |
| Ackley | norm | noisy_y | tpe_gp_refine | 1.812 | 0.9148 | -0.8974 | True | 44 | 66 |
| Ackley | norm | noisy_y | optuna | 1.812 | 0.7508 | -1.061 | True | 44 | 36 |
| Ackley | raw | clean | random | 2.043 | 2.843 | 0.8 | False | 32 | 2 |
| Ackley | raw | clean | tpe_w_smooth | 2.043 | 1.429 | -0.6135 | True | 32 | 42 |
| Ackley | raw | clean | tpe_w_smooth_inv | 2.043 | 2.073 | 0.03021 | False | 32 | 30 |
| Ackley | raw | clean | tpe_w_sign | 2.043 | 1.603 | -0.4395 | True | 32 | 44 |
| Ackley | raw | clean | tpe_w_sign_inv | 2.043 | 1.674 | -0.3685 | True | 32 | 40 |
| Ackley | raw | clean | tpe_refine | 2.043 | 0.7898 | -1.253 | True | 32 | 76 |
| Ackley | raw | clean | tpe_gp | 2.043 | 0.4545 | -1.588 | True | 32 | 86 |
| Ackley | raw | clean | tpe_gp_w | 2.043 | 0.3911 | -1.652 | True | 32 | 90 |
| Ackley | raw | clean | tpe_gp_refine | 2.043 | 0.4359 | -1.607 | True | 32 | 84 |
| Ackley | raw | clean | optuna | 2.043 | 0.655 | -1.388 | True | 32 | 40 |
| Ackley | raw | noisy_y | random | 1.812 | 2.844 | 1.032 | False | 44 | 2 |
| Ackley | raw | noisy_y | tpe_w_smooth | 1.812 | 1.456 | -0.3566 | True | 44 | 46 |
| Ackley | raw | noisy_y | tpe_w_smooth_inv | 1.812 | 1.62 | -0.1922 | True | 44 | 44 |
| Ackley | raw | noisy_y | tpe_w_sign | 1.812 | 1.476 | -0.3361 | True | 44 | 50 |
| Ackley | raw | noisy_y | tpe_w_sign_inv | 1.812 | 1.533 | -0.2795 | True | 44 | 40 |
| Ackley | raw | noisy_y | tpe_refine | 1.812 | 1.065 | -0.7469 | True | 44 | 66 |
| Ackley | raw | noisy_y | tpe_gp | 1.812 | 0.4187 | -1.394 | True | 44 | 88 |
| Ackley | raw | noisy_y | tpe_gp_w | 1.812 | 0.4513 | -1.361 | True | 44 | 84 |
| Ackley | raw | noisy_y | tpe_gp_refine | 1.812 | 0.2954 | -1.517 | True | 44 | 90 |
| Ackley | raw | noisy_y | optuna | 1.812 | 0.7508 | -1.061 | True | 44 | 36 |
| Rastrigin | norm | clean | random | 2.775 | 5.46 | 2.684 | False | 28 | 2 |
| Rastrigin | norm | clean | tpe_w_smooth | 2.775 | 3.43 | 0.6549 | False | 28 | 8 |
| Rastrigin | norm | clean | tpe_w_smooth_inv | 2.775 | 2.721 | -0.05398 | True | 28 | 36 |
| Rastrigin | norm | clean | tpe_w_sign | 2.775 | 3.915 | 1.14 | False | 28 | 8 |
| Rastrigin | norm | clean | tpe_w_sign_inv | 2.775 | 2.553 | -0.2224 | True | 28 | 26 |
| Rastrigin | norm | clean | tpe_refine | 2.775 | 1.136 | -1.639 | True | 28 | 76 |
| Rastrigin | norm | clean | tpe_gp | 2.775 | 2.436 | -0.3393 | True | 28 | 24 |
| Rastrigin | norm | clean | tpe_gp_w | 2.775 | 2.674 | -0.1012 | True | 28 | 18 |
| Rastrigin | norm | clean | tpe_gp_refine | 2.775 | 1.043 | -1.733 | True | 28 | 64 |
| Rastrigin | norm | clean | optuna | 2.775 | 2.58 | -0.195 | True | 28 | 10 |
| Rastrigin | norm | noisy_y | random | 3.453 | 5.465 | 2.013 | False | 16 | 2 |
| Rastrigin | norm | noisy_y | tpe_w_smooth | 3.453 | 3.435 | -0.01724 | True | 16 | 8 |
| Rastrigin | norm | noisy_y | tpe_w_smooth_inv | 3.453 | 2.914 | -0.5384 | True | 16 | 24 |
| Rastrigin | norm | noisy_y | tpe_w_sign | 3.453 | 3.769 | 0.3165 | False | 16 | 4 |
| Rastrigin | norm | noisy_y | tpe_w_sign_inv | 3.453 | 2.701 | -0.752 | True | 16 | 20 |
| Rastrigin | norm | noisy_y | tpe_refine | 3.453 | 1.189 | -2.263 | True | 16 | 52 |
| Rastrigin | norm | noisy_y | tpe_gp | 3.453 | 3.168 | -0.285 | True | 16 | 18 |
| Rastrigin | norm | noisy_y | tpe_gp_w | 3.453 | 2.951 | -0.5016 | True | 16 | 12 |
| Rastrigin | norm | noisy_y | tpe_gp_refine | 3.453 | 1.248 | -2.204 | True | 16 | 48 |
| Rastrigin | norm | noisy_y | optuna | 3.453 | 2.523 | -0.9294 | True | 16 | 12 |
| Rastrigin | raw | clean | random | 2.775 | 5.46 | 2.684 | False | 28 | 2 |
| Rastrigin | raw | clean | tpe_w_smooth | 2.775 | 3.43 | 0.6549 | False | 28 | 8 |
| Rastrigin | raw | clean | tpe_w_smooth_inv | 2.775 | 2.721 | -0.05398 | True | 28 | 36 |
| Rastrigin | raw | clean | tpe_w_sign | 2.775 | 3.915 | 1.14 | False | 28 | 8 |
| Rastrigin | raw | clean | tpe_w_sign_inv | 2.775 | 2.553 | -0.2224 | True | 28 | 26 |
| Rastrigin | raw | clean | tpe_refine | 2.775 | 1.136 | -1.639 | True | 28 | 76 |
| Rastrigin | raw | clean | tpe_gp | 2.775 | 3.599 | 0.824 | False | 28 | 8 |
| Rastrigin | raw | clean | tpe_gp_w | 2.775 | 2.127 | -0.6486 | True | 28 | 20 |
| Rastrigin | raw | clean | tpe_gp_refine | 2.775 | 1.226 | -1.549 | True | 28 | 58 |
| Rastrigin | raw | clean | optuna | 2.775 | 2.58 | -0.195 | True | 28 | 10 |
| Rastrigin | raw | noisy_y | random | 3.453 | 5.465 | 2.013 | False | 16 | 2 |
| Rastrigin | raw | noisy_y | tpe_w_smooth | 3.453 | 3.435 | -0.01724 | True | 16 | 8 |
| Rastrigin | raw | noisy_y | tpe_w_smooth_inv | 3.453 | 2.914 | -0.5384 | True | 16 | 24 |
| Rastrigin | raw | noisy_y | tpe_w_sign | 3.453 | 3.769 | 0.3165 | False | 16 | 4 |
| Rastrigin | raw | noisy_y | tpe_w_sign_inv | 3.453 | 2.701 | -0.752 | True | 16 | 20 |
| Rastrigin | raw | noisy_y | tpe_refine | 3.453 | 1.189 | -2.263 | True | 16 | 52 |
| Rastrigin | raw | noisy_y | tpe_gp | 3.453 | 3.456 | 0.003334 | False | 16 | 12 |
| Rastrigin | raw | noisy_y | tpe_gp_w | 3.453 | 2.2 | -1.252 | True | 16 | 18 |
| Rastrigin | raw | noisy_y | tpe_gp_refine | 3.453 | 1.521 | -1.932 | True | 16 | 44 |
| Rastrigin | raw | noisy_y | optuna | 3.453 | 2.523 | -0.9294 | True | 16 | 12 |
| Rosenbrock | norm | clean | random | 1.533 | 0.6699 | -0.8636 | True | 8 | 12 |
| Rosenbrock | norm | clean | tpe_w_smooth | 1.533 | 1.379 | -0.1547 | True | 8 | 14 |
| Rosenbrock | norm | clean | tpe_w_smooth_inv | 1.533 | 1.376 | -0.1576 | True | 8 | 18 |
| Rosenbrock | norm | clean | tpe_w_sign | 1.533 | 1.589 | 0.05502 | False | 8 | 8 |
| Rosenbrock | norm | clean | tpe_w_sign_inv | 1.533 | 1.531 | -0.002057 | True | 8 | 14 |
| Rosenbrock | norm | clean | tpe_refine | 1.533 | 0.3954 | -1.138 | True | 8 | 24 |
| Rosenbrock | norm | clean | tpe_gp | 1.533 | 1.78 | 0.2468 | False | 8 | 12 |
| Rosenbrock | norm | clean | tpe_gp_w | 1.533 | 1.47 | -0.06308 | True | 8 | 10 |
| Rosenbrock | norm | clean | tpe_gp_refine | 1.533 | 0.5048 | -1.029 | True | 8 | 26 |
| Rosenbrock | norm | clean | optuna | 1.533 | 0.3045 | -1.229 | True | 8 | 32 |
| Rosenbrock | norm | noisy_y | random | 1.593 | 0.6715 | -0.9218 | True | 10 | 12 |
| Rosenbrock | norm | noisy_y | tpe_w_smooth | 1.593 | 1.483 | -0.1101 | True | 10 | 16 |
| Rosenbrock | norm | noisy_y | tpe_w_smooth_inv | 1.593 | 1.461 | -0.1327 | True | 10 | 12 |
| Rosenbrock | norm | noisy_y | tpe_w_sign | 1.593 | 1.651 | 0.05728 | False | 10 | 12 |
| Rosenbrock | norm | noisy_y | tpe_w_sign_inv | 1.593 | 1.62 | 0.02718 | False | 10 | 12 |
| Rosenbrock | norm | noisy_y | tpe_refine | 1.593 | 0.4284 | -1.165 | True | 10 | 18 |
| Rosenbrock | norm | noisy_y | tpe_gp | 1.593 | 1.865 | 0.2718 | False | 10 | 12 |
| Rosenbrock | norm | noisy_y | tpe_gp_w | 1.593 | 1.455 | -0.1378 | True | 10 | 10 |
| Rosenbrock | norm | noisy_y | tpe_gp_refine | 1.593 | 0.4575 | -1.136 | True | 10 | 26 |
| Rosenbrock | norm | noisy_y | optuna | 1.593 | 0.3558 | -1.237 | True | 10 | 26 |
| Rosenbrock | raw | clean | random | 1.533 | 0.6699 | -0.8636 | True | 8 | 12 |
| Rosenbrock | raw | clean | tpe_w_smooth | 1.533 | 1.379 | -0.1547 | True | 8 | 14 |
| Rosenbrock | raw | clean | tpe_w_smooth_inv | 1.533 | 1.376 | -0.1576 | True | 8 | 18 |
| Rosenbrock | raw | clean | tpe_w_sign | 1.533 | 1.589 | 0.05502 | False | 8 | 8 |
| Rosenbrock | raw | clean | tpe_w_sign_inv | 1.533 | 1.531 | -0.002057 | True | 8 | 14 |
| Rosenbrock | raw | clean | tpe_refine | 1.533 | 0.3954 | -1.138 | True | 8 | 24 |
| Rosenbrock | raw | clean | tpe_gp | 1.533 | 0.4135 | -1.12 | True | 8 | 34 |
| Rosenbrock | raw | clean | tpe_gp_w | 1.533 | 0.2954 | -1.238 | True | 8 | 8 |
| Rosenbrock | raw | clean | tpe_gp_refine | 1.533 | 0.2261 | -1.307 | True | 8 | 14 |
| Rosenbrock | raw | clean | optuna | 1.533 | 0.3045 | -1.229 | True | 8 | 32 |
| Rosenbrock | raw | noisy_y | random | 1.593 | 0.6715 | -0.9218 | True | 10 | 12 |
| Rosenbrock | raw | noisy_y | tpe_w_smooth | 1.593 | 1.483 | -0.1101 | True | 10 | 16 |
| Rosenbrock | raw | noisy_y | tpe_w_smooth_inv | 1.593 | 1.461 | -0.1327 | True | 10 | 12 |
| Rosenbrock | raw | noisy_y | tpe_w_sign | 1.593 | 1.651 | 0.05728 | False | 10 | 12 |
| Rosenbrock | raw | noisy_y | tpe_w_sign_inv | 1.593 | 1.62 | 0.02718 | False | 10 | 12 |
| Rosenbrock | raw | noisy_y | tpe_refine | 1.593 | 0.4284 | -1.165 | True | 10 | 18 |
| Rosenbrock | raw | noisy_y | tpe_gp | 1.593 | 0.2657 | -1.328 | True | 10 | 32 |
| Rosenbrock | raw | noisy_y | tpe_gp_w | 1.593 | 0.3183 | -1.275 | True | 10 | 8 |
| Rosenbrock | raw | noisy_y | tpe_gp_refine | 1.593 | 0.23 | -1.363 | True | 10 | 12 |
| Rosenbrock | raw | noisy_y | optuna | 1.593 | 0.3558 | -1.237 | True | 10 | 26 |
| Sphere | norm | clean | random | 0.1392 | 0.4018 | 0.2626 | False | 36 | 0 |
| Sphere | norm | clean | tpe_w_smooth | 0.1392 | 0.1765 | 0.03729 | False | 36 | 20 |
| Sphere | norm | clean | tpe_w_smooth_inv | 0.1392 | 0.09304 | -0.04618 | True | 36 | 46 |
| Sphere | norm | clean | tpe_w_sign | 0.1392 | 0.1648 | 0.02559 | False | 36 | 28 |
| Sphere | norm | clean | tpe_w_sign_inv | 0.1392 | 0.0918 | -0.04741 | True | 36 | 48 |
| Sphere | norm | clean | tpe_refine | 0.1392 | 6.981e-07 | -0.1392 | True | 36 | 100 |
| Sphere | norm | clean | tpe_gp | 0.1392 | 0.08402 | -0.0552 | True | 36 | 46 |
| Sphere | norm | clean | tpe_gp_w | 0.1392 | 0.1011 | -0.0381 | True | 36 | 28 |
| Sphere | norm | clean | tpe_gp_refine | 0.1392 | 4.024e-07 | -0.1392 | True | 36 | 100 |
| Sphere | norm | clean | optuna | 0.1392 | 0.01705 | -0.1222 | True | 36 | 6 |
| Sphere | norm | noisy_y | random | 0.126 | 0.4018 | 0.2759 | False | 26 | 0 |
| Sphere | norm | noisy_y | tpe_w_smooth | 0.126 | 0.1708 | 0.04482 | False | 26 | 16 |
| Sphere | norm | noisy_y | tpe_w_smooth_inv | 0.126 | 0.09846 | -0.0275 | True | 26 | 24 |
| Sphere | norm | noisy_y | tpe_w_sign | 0.126 | 0.1999 | 0.07391 | False | 26 | 22 |
| Sphere | norm | noisy_y | tpe_w_sign_inv | 0.126 | 0.09839 | -0.02758 | True | 26 | 36 |
| Sphere | norm | noisy_y | tpe_refine | 0.126 | 0.0006047 | -0.1254 | True | 26 | 98 |
| Sphere | norm | noisy_y | tpe_gp | 0.126 | 0.08345 | -0.04251 | True | 26 | 32 |
| Sphere | norm | noisy_y | tpe_gp_w | 0.126 | 0.08862 | -0.03734 | True | 26 | 24 |
| Sphere | norm | noisy_y | tpe_gp_refine | 0.126 | 0.00107 | -0.1249 | True | 26 | 96 |
| Sphere | norm | noisy_y | optuna | 0.126 | 0.01714 | -0.1088 | True | 26 | 8 |
| Sphere | raw | clean | random | 0.1392 | 0.4018 | 0.2626 | False | 36 | 0 |
| Sphere | raw | clean | tpe_w_smooth | 0.1392 | 0.1765 | 0.03729 | False | 36 | 20 |
| Sphere | raw | clean | tpe_w_smooth_inv | 0.1392 | 0.09304 | -0.04618 | True | 36 | 46 |
| Sphere | raw | clean | tpe_w_sign | 0.1392 | 0.1648 | 0.02559 | False | 36 | 28 |
| Sphere | raw | clean | tpe_w_sign_inv | 0.1392 | 0.0918 | -0.04741 | True | 36 | 48 |
| Sphere | raw | clean | tpe_refine | 0.1392 | 6.981e-07 | -0.1392 | True | 36 | 100 |
| Sphere | raw | clean | tpe_gp | 0.1392 | 0.003201 | -0.136 | True | 36 | 84 |
| Sphere | raw | clean | tpe_gp_w | 0.1392 | 0.002107 | -0.1371 | True | 36 | 82 |
| Sphere | raw | clean | tpe_gp_refine | 0.1392 | 1.542e-06 | -0.1392 | True | 36 | 100 |
| Sphere | raw | clean | optuna | 0.1392 | 0.01705 | -0.1222 | True | 36 | 6 |
| Sphere | raw | noisy_y | random | 0.126 | 0.4018 | 0.2759 | False | 26 | 0 |
| Sphere | raw | noisy_y | tpe_w_smooth | 0.126 | 0.1708 | 0.04482 | False | 26 | 16 |
| Sphere | raw | noisy_y | tpe_w_smooth_inv | 0.126 | 0.09846 | -0.0275 | True | 26 | 24 |
| Sphere | raw | noisy_y | tpe_w_sign | 0.126 | 0.1999 | 0.07391 | False | 26 | 22 |
| Sphere | raw | noisy_y | tpe_w_sign_inv | 0.126 | 0.09839 | -0.02758 | True | 26 | 36 |
| Sphere | raw | noisy_y | tpe_refine | 0.126 | 0.0006047 | -0.1254 | True | 26 | 98 |
| Sphere | raw | noisy_y | tpe_gp | 0.126 | 0.004551 | -0.1214 | True | 26 | 58 |
| Sphere | raw | noisy_y | tpe_gp_w | 0.126 | 0.005578 | -0.1204 | True | 26 | 56 |
| Sphere | raw | noisy_y | tpe_gp_refine | 0.126 | 0.0007766 | -0.1252 | True | 26 | 98 |
| Sphere | raw | noisy_y | optuna | 0.126 | 0.01714 | -0.1088 | True | 26 | 8 |

## Ключевые метрики (все ячейки)

| function | scale | data | algorithm | success_rate_% | steps_mean | final_dist_y_mean | final_dist_x_mean |
|---|---|---|---|---|---|---|---|
| Sphere | raw | clean | random | 0 |  | 0.4018 | 0.5556 |
| Sphere | raw | clean | tpe | 36 | 59.28 | 0.1392 | 0.2364 |
| Sphere | raw | clean | tpe_w_smooth | 20 | 48.8 | 0.1765 | 0.2854 |
| Sphere | raw | clean | tpe_w_smooth_inv | 46 | 56.52 | 0.09304 | 0.19 |
| Sphere | raw | clean | tpe_w_sign | 28 | 61.79 | 0.1648 | 0.2486 |
| Sphere | raw | clean | tpe_w_sign_inv | 48 | 59.71 | 0.0918 | 0.1792 |
| Sphere | raw | clean | tpe_refine | 100 | 19.92 | 6.981e-07 | 0.0005607 |
| Sphere | raw | clean | tpe_gp | 84 | 45.9 | 0.003201 | 0.02371 |
| Sphere | raw | clean | tpe_gp_w | 82 | 45.59 | 0.002107 | 0.02206 |
| Sphere | raw | clean | tpe_gp_refine | 100 | 15.06 | 1.542e-06 | 0.0007865 |
| Sphere | raw | clean | optuna | 6 | 64 | 0.01705 | 0.1141 |
| Sphere | raw | noisy_y | random | 0 |  | 0.4018 | 0.5556 |
| Sphere | raw | noisy_y | tpe | 26 | 64.92 | 0.126 | 0.229 |
| Sphere | raw | noisy_y | tpe_w_smooth | 16 | 61.88 | 0.1708 | 0.2826 |
| Sphere | raw | noisy_y | tpe_w_smooth_inv | 24 | 60.58 | 0.09846 | 0.2027 |
| Sphere | raw | noisy_y | tpe_w_sign | 22 | 67.45 | 0.1999 | 0.2726 |
| Sphere | raw | noisy_y | tpe_w_sign_inv | 36 | 68.33 | 0.09839 | 0.1966 |
| Sphere | raw | noisy_y | tpe_refine | 98 | 24.92 | 0.0006047 | 0.01943 |
| Sphere | raw | noisy_y | tpe_gp | 58 | 46.55 | 0.004551 | 0.05501 |
| Sphere | raw | noisy_y | tpe_gp_w | 56 | 45.86 | 0.005578 | 0.05767 |
| Sphere | raw | noisy_y | tpe_gp_refine | 98 | 18.86 | 0.0007766 | 0.02245 |
| Sphere | raw | noisy_y | optuna | 8 | 66 | 0.01714 | 0.1154 |
| Sphere | norm | clean | random | 0 |  | 0.4018 | 0.5556 |
| Sphere | norm | clean | tpe | 36 | 59.28 | 0.1392 | 0.2364 |
| Sphere | norm | clean | tpe_w_smooth | 20 | 48.8 | 0.1765 | 0.2854 |
| Sphere | norm | clean | tpe_w_smooth_inv | 46 | 56.52 | 0.09304 | 0.19 |
| Sphere | norm | clean | tpe_w_sign | 28 | 61.79 | 0.1648 | 0.2486 |
| Sphere | norm | clean | tpe_w_sign_inv | 48 | 59.71 | 0.0918 | 0.1792 |
| Sphere | norm | clean | tpe_refine | 100 | 19.92 | 6.981e-07 | 0.0005607 |
| Sphere | norm | clean | tpe_gp | 46 | 54.48 | 0.08402 | 0.1776 |
| Sphere | norm | clean | tpe_gp_w | 28 | 62.43 | 0.1011 | 0.211 |
| Sphere | norm | clean | tpe_gp_refine | 100 | 18.92 | 4.024e-07 | 0.0004692 |
| Sphere | norm | clean | optuna | 6 | 64 | 0.01705 | 0.1141 |
| Sphere | norm | noisy_y | random | 0 |  | 0.4018 | 0.5556 |
| Sphere | norm | noisy_y | tpe | 26 | 64.92 | 0.126 | 0.229 |
| Sphere | norm | noisy_y | tpe_w_smooth | 16 | 61.88 | 0.1708 | 0.2826 |
| Sphere | norm | noisy_y | tpe_w_smooth_inv | 24 | 60.58 | 0.09846 | 0.2027 |
| Sphere | norm | noisy_y | tpe_w_sign | 22 | 67.45 | 0.1999 | 0.2726 |
| Sphere | norm | noisy_y | tpe_w_sign_inv | 36 | 68.33 | 0.09839 | 0.1966 |
| Sphere | norm | noisy_y | tpe_refine | 98 | 24.92 | 0.0006047 | 0.01943 |
| Sphere | norm | noisy_y | tpe_gp | 32 | 62.75 | 0.08345 | 0.1855 |
| Sphere | norm | noisy_y | tpe_gp_w | 24 | 63.08 | 0.08862 | 0.2087 |
| Sphere | norm | noisy_y | tpe_gp_refine | 96 | 24.12 | 0.00107 | 0.02769 |
| Sphere | norm | noisy_y | optuna | 8 | 66 | 0.01714 | 0.1154 |
| Rosenbrock | raw | clean | random | 12 | 50.5 | 0.6699 | 0.8094 |
| Rosenbrock | raw | clean | tpe | 8 | 20 | 1.533 | 1.274 |
| Rosenbrock | raw | clean | tpe_w_smooth | 14 | 25 | 1.379 | 1.236 |
| Rosenbrock | raw | clean | tpe_w_smooth_inv | 18 | 36.22 | 1.376 | 1.248 |
| Rosenbrock | raw | clean | tpe_w_sign | 8 | 26.5 | 1.589 | 1.322 |
| Rosenbrock | raw | clean | tpe_w_sign_inv | 14 | 32.29 | 1.531 | 1.292 |
| Rosenbrock | raw | clean | tpe_refine | 24 | 38.5 | 0.3954 | 0.9035 |
| Rosenbrock | raw | clean | tpe_gp | 34 | 28.88 | 0.4135 | 0.7635 |
| Rosenbrock | raw | clean | tpe_gp_w | 8 | 42 | 0.2954 | 0.8261 |
| Rosenbrock | raw | clean | tpe_gp_refine | 14 | 32 | 0.2261 | 0.7095 |
| Rosenbrock | raw | clean | optuna | 32 | 55.25 | 0.3045 | 0.6479 |
| Rosenbrock | raw | noisy_y | random | 12 | 50.5 | 0.6715 | 0.8068 |
| Rosenbrock | raw | noisy_y | tpe | 10 | 21.6 | 1.593 | 1.323 |
| Rosenbrock | raw | noisy_y | tpe_w_smooth | 16 | 26.25 | 1.483 | 1.253 |
| Rosenbrock | raw | noisy_y | tpe_w_smooth_inv | 12 | 21.17 | 1.461 | 1.285 |
| Rosenbrock | raw | noisy_y | tpe_w_sign | 12 | 28.33 | 1.651 | 1.305 |
| Rosenbrock | raw | noisy_y | tpe_w_sign_inv | 12 | 24.67 | 1.62 | 1.301 |
| Rosenbrock | raw | noisy_y | tpe_refine | 18 | 46.11 | 0.4284 | 1.017 |
| Rosenbrock | raw | noisy_y | tpe_gp | 32 | 28.44 | 0.2657 | 0.8299 |
| Rosenbrock | raw | noisy_y | tpe_gp_w | 8 | 60 | 0.3183 | 0.8663 |
| Rosenbrock | raw | noisy_y | tpe_gp_refine | 12 | 20.67 | 0.23 | 0.6716 |
| Rosenbrock | raw | noisy_y | optuna | 26 | 51.77 | 0.3558 | 0.6932 |
| Rosenbrock | norm | clean | random | 12 | 50.5 | 0.6699 | 0.8094 |
| Rosenbrock | norm | clean | tpe | 8 | 20 | 1.533 | 1.274 |
| Rosenbrock | norm | clean | tpe_w_smooth | 14 | 25 | 1.379 | 1.236 |
| Rosenbrock | norm | clean | tpe_w_smooth_inv | 18 | 36.22 | 1.376 | 1.248 |
| Rosenbrock | norm | clean | tpe_w_sign | 8 | 26.5 | 1.589 | 1.322 |
| Rosenbrock | norm | clean | tpe_w_sign_inv | 14 | 32.29 | 1.531 | 1.292 |
| Rosenbrock | norm | clean | tpe_refine | 24 | 38.5 | 0.3954 | 0.9035 |
| Rosenbrock | norm | clean | tpe_gp | 12 | 28.5 | 1.78 | 1.307 |
| Rosenbrock | norm | clean | tpe_gp_w | 10 | 25.2 | 1.47 | 1.298 |
| Rosenbrock | norm | clean | tpe_gp_refine | 26 | 28.46 | 0.5048 | 0.8659 |
| Rosenbrock | norm | clean | optuna | 32 | 55.25 | 0.3045 | 0.6479 |
| Rosenbrock | norm | noisy_y | random | 12 | 50.5 | 0.6715 | 0.8068 |
| Rosenbrock | norm | noisy_y | tpe | 10 | 21.6 | 1.593 | 1.323 |
| Rosenbrock | norm | noisy_y | tpe_w_smooth | 16 | 26.25 | 1.483 | 1.253 |
| Rosenbrock | norm | noisy_y | tpe_w_smooth_inv | 12 | 21.17 | 1.461 | 1.285 |
| Rosenbrock | norm | noisy_y | tpe_w_sign | 12 | 28.33 | 1.651 | 1.305 |
| Rosenbrock | norm | noisy_y | tpe_w_sign_inv | 12 | 24.67 | 1.62 | 1.301 |
| Rosenbrock | norm | noisy_y | tpe_refine | 18 | 46.11 | 0.4284 | 1.017 |
| Rosenbrock | norm | noisy_y | tpe_gp | 12 | 32.5 | 1.865 | 1.33 |
| Rosenbrock | norm | noisy_y | tpe_gp_w | 10 | 23.2 | 1.455 | 1.3 |
| Rosenbrock | norm | noisy_y | tpe_gp_refine | 26 | 30.23 | 0.4575 | 0.8704 |
| Rosenbrock | norm | noisy_y | optuna | 26 | 51.77 | 0.3558 | 0.6932 |
| Rastrigin | raw | clean | random | 2 | 13 | 5.46 | 1.474 |
| Rastrigin | raw | clean | tpe | 28 | 44.71 | 2.775 | 1.328 |
| Rastrigin | raw | clean | tpe_w_smooth | 8 | 38.5 | 3.43 | 1.445 |
| Rastrigin | raw | clean | tpe_w_smooth_inv | 36 | 51.94 | 2.721 | 1.32 |
| Rastrigin | raw | clean | tpe_w_sign | 8 | 49.5 | 3.915 | 1.559 |
| Rastrigin | raw | clean | tpe_w_sign_inv | 26 | 43.69 | 2.553 | 1.307 |
| Rastrigin | raw | clean | tpe_refine | 76 | 29.66 | 1.136 | 0.8131 |
| Rastrigin | raw | clean | tpe_gp | 8 | 59.5 | 3.599 | 1.456 |
| Rastrigin | raw | clean | tpe_gp_w | 20 | 80.5 | 2.127 | 1.096 |
| Rastrigin | raw | clean | tpe_gp_refine | 58 | 38.86 | 1.226 | 0.8937 |
| Rastrigin | raw | clean | optuna | 10 | 70.6 | 2.58 | 1.026 |
| Rastrigin | raw | noisy_y | random | 2 | 13 | 5.465 | 1.493 |
| Rastrigin | raw | noisy_y | tpe | 16 | 28.5 | 3.453 | 1.46 |
| Rastrigin | raw | noisy_y | tpe_w_smooth | 8 | 49 | 3.435 | 1.426 |
| Rastrigin | raw | noisy_y | tpe_w_smooth_inv | 24 | 41.75 | 2.914 | 1.414 |
| Rastrigin | raw | noisy_y | tpe_w_sign | 4 | 31.5 | 3.769 | 1.527 |
| Rastrigin | raw | noisy_y | tpe_w_sign_inv | 20 | 35.9 | 2.701 | 1.312 |
| Rastrigin | raw | noisy_y | tpe_refine | 52 | 28.12 | 1.189 | 0.8913 |
| Rastrigin | raw | noisy_y | tpe_gp | 12 | 38.5 | 3.456 | 1.491 |
| Rastrigin | raw | noisy_y | tpe_gp_w | 18 | 72.89 | 2.2 | 1.092 |
| Rastrigin | raw | noisy_y | tpe_gp_refine | 44 | 37.55 | 1.521 | 0.8836 |
| Rastrigin | raw | noisy_y | optuna | 12 | 60 | 2.523 | 1.003 |
| Rastrigin | norm | clean | random | 2 | 13 | 5.46 | 1.474 |
| Rastrigin | norm | clean | tpe | 28 | 44.71 | 2.775 | 1.328 |
| Rastrigin | norm | clean | tpe_w_smooth | 8 | 38.5 | 3.43 | 1.445 |
| Rastrigin | norm | clean | tpe_w_smooth_inv | 36 | 51.94 | 2.721 | 1.32 |
| Rastrigin | norm | clean | tpe_w_sign | 8 | 49.5 | 3.915 | 1.559 |
| Rastrigin | norm | clean | tpe_w_sign_inv | 26 | 43.69 | 2.553 | 1.307 |
| Rastrigin | norm | clean | tpe_refine | 76 | 29.66 | 1.136 | 0.8131 |
| Rastrigin | norm | clean | tpe_gp | 24 | 46 | 2.436 | 1.283 |
| Rastrigin | norm | clean | tpe_gp_w | 18 | 37 | 2.674 | 1.341 |
| Rastrigin | norm | clean | tpe_gp_refine | 64 | 31.31 | 1.043 | 0.7949 |
| Rastrigin | norm | clean | optuna | 10 | 70.6 | 2.58 | 1.026 |
| Rastrigin | norm | noisy_y | random | 2 | 13 | 5.465 | 1.493 |
| Rastrigin | norm | noisy_y | tpe | 16 | 28.5 | 3.453 | 1.46 |
| Rastrigin | norm | noisy_y | tpe_w_smooth | 8 | 49 | 3.435 | 1.426 |
| Rastrigin | norm | noisy_y | tpe_w_smooth_inv | 24 | 41.75 | 2.914 | 1.414 |
| Rastrigin | norm | noisy_y | tpe_w_sign | 4 | 31.5 | 3.769 | 1.527 |
| Rastrigin | norm | noisy_y | tpe_w_sign_inv | 20 | 35.9 | 2.701 | 1.312 |
| Rastrigin | norm | noisy_y | tpe_refine | 52 | 28.12 | 1.189 | 0.8913 |
| Rastrigin | norm | noisy_y | tpe_gp | 18 | 54.89 | 3.168 | 1.428 |
| Rastrigin | norm | noisy_y | tpe_gp_w | 12 | 36.67 | 2.951 | 1.389 |
| Rastrigin | norm | noisy_y | tpe_gp_refine | 48 | 38.46 | 1.248 | 0.911 |
| Rastrigin | norm | noisy_y | optuna | 12 | 60 | 2.523 | 1.003 |
| Ackley | raw | clean | random | 2 | 13 | 2.843 | 0.6475 |
| Ackley | raw | clean | tpe | 32 | 40.44 | 2.043 | 0.7313 |
| Ackley | raw | clean | tpe_w_smooth | 42 | 36.29 | 1.429 | 0.4699 |
| Ackley | raw | clean | tpe_w_smooth_inv | 30 | 39.07 | 2.073 | 0.7205 |
| Ackley | raw | clean | tpe_w_sign | 44 | 37.45 | 1.603 | 0.5353 |
| Ackley | raw | clean | tpe_w_sign_inv | 40 | 50.25 | 1.674 | 0.5648 |
| Ackley | raw | clean | tpe_refine | 76 | 31.05 | 0.7898 | 0.2999 |
| Ackley | raw | clean | tpe_gp | 86 | 39.23 | 0.4545 | 0.159 |
| Ackley | raw | clean | tpe_gp_w | 90 | 44.33 | 0.3911 | 0.1296 |
| Ackley | raw | clean | tpe_gp_refine | 84 | 18.95 | 0.4359 | 0.1614 |
| Ackley | raw | clean | optuna | 40 | 69.5 | 0.655 | 0.1112 |
| Ackley | raw | noisy_y | random | 2 | 13 | 2.844 | 0.657 |
| Ackley | raw | noisy_y | tpe | 44 | 40.23 | 1.812 | 0.6559 |
| Ackley | raw | noisy_y | tpe_w_smooth | 46 | 35.57 | 1.456 | 0.4717 |
| Ackley | raw | noisy_y | tpe_w_smooth_inv | 44 | 50.05 | 1.62 | 0.5333 |
| Ackley | raw | noisy_y | tpe_w_sign | 50 | 41.16 | 1.476 | 0.4761 |
| Ackley | raw | noisy_y | tpe_w_sign_inv | 40 | 48.85 | 1.533 | 0.5214 |
| Ackley | raw | noisy_y | tpe_refine | 66 | 28.3 | 1.065 | 0.4021 |
| Ackley | raw | noisy_y | tpe_gp | 88 | 39.52 | 0.4187 | 0.1347 |
| Ackley | raw | noisy_y | tpe_gp_w | 84 | 42.69 | 0.4513 | 0.1448 |
| Ackley | raw | noisy_y | tpe_gp_refine | 90 | 22.18 | 0.2954 | 0.08897 |
| Ackley | raw | noisy_y | optuna | 36 | 62.33 | 0.7508 | 0.1243 |
| Ackley | norm | clean | random | 2 | 13 | 2.843 | 0.6475 |
| Ackley | norm | clean | tpe | 32 | 40.44 | 2.043 | 0.7313 |
| Ackley | norm | clean | tpe_w_smooth | 42 | 36.29 | 1.429 | 0.4699 |
| Ackley | norm | clean | tpe_w_smooth_inv | 30 | 39.07 | 2.073 | 0.7205 |
| Ackley | norm | clean | tpe_w_sign | 44 | 37.45 | 1.603 | 0.5353 |
| Ackley | norm | clean | tpe_w_sign_inv | 40 | 50.25 | 1.674 | 0.5648 |
| Ackley | norm | clean | tpe_refine | 76 | 31.05 | 0.7898 | 0.2999 |
| Ackley | norm | clean | tpe_gp | 52 | 40.92 | 1.278 | 0.4349 |
| Ackley | norm | clean | tpe_gp_w | 48 | 54.75 | 1.388 | 0.4701 |
| Ackley | norm | clean | tpe_gp_refine | 68 | 28.88 | 0.889 | 0.3163 |
| Ackley | norm | clean | optuna | 40 | 69.5 | 0.655 | 0.1112 |
| Ackley | norm | noisy_y | random | 2 | 13 | 2.844 | 0.657 |
| Ackley | norm | noisy_y | tpe | 44 | 40.23 | 1.812 | 0.6559 |
| Ackley | norm | noisy_y | tpe_w_smooth | 46 | 35.57 | 1.456 | 0.4717 |
| Ackley | norm | noisy_y | tpe_w_smooth_inv | 44 | 50.05 | 1.62 | 0.5333 |
| Ackley | norm | noisy_y | tpe_w_sign | 50 | 41.16 | 1.476 | 0.4761 |
| Ackley | norm | noisy_y | tpe_w_sign_inv | 40 | 48.85 | 1.533 | 0.5214 |
| Ackley | norm | noisy_y | tpe_refine | 66 | 28.3 | 1.065 | 0.4021 |
| Ackley | norm | noisy_y | tpe_gp | 56 | 40.68 | 1.27 | 0.431 |
| Ackley | norm | noisy_y | tpe_gp_w | 36 | 54.61 | 1.716 | 0.5701 |
| Ackley | norm | noisy_y | tpe_gp_refine | 66 | 33 | 0.9148 | 0.3317 |
| Ackley | norm | noisy_y | optuna | 36 | 62.33 | 0.7508 | 0.1243 |

## Полная таблица (все метрики, все ячейки)

| function | scale | data | algorithm | success_rate_% | steps_mean | steps_std | final_dist_y_mean | final_dist_y_std | final_dist_y_median | final_dist_x_mean | final_dist_x_std |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Sphere | raw | clean | random | 0 |  |  | 0.4018 | 0.4152 | 0.2598 | 0.5556 | 0.3051 |
| Sphere | raw | clean | tpe | 36 | 59.28 | 22.93 | 0.1392 | 0.2829 | 0.01457 | 0.2364 | 0.2887 |
| Sphere | raw | clean | tpe_w_smooth | 20 | 48.8 | 21.74 | 0.1765 | 0.3299 | 0.03297 | 0.2854 | 0.3084 |
| Sphere | raw | clean | tpe_w_smooth_inv | 46 | 56.52 | 23.64 | 0.09304 | 0.1731 | 0.003277 | 0.19 | 0.2386 |
| Sphere | raw | clean | tpe_w_sign | 28 | 61.79 | 26.3 | 0.1648 | 0.3993 | 0.01599 | 0.2486 | 0.3209 |
| Sphere | raw | clean | tpe_w_sign_inv | 48 | 59.71 | 23.62 | 0.0918 | 0.1901 | 0.002821 | 0.1792 | 0.2443 |
| Sphere | raw | clean | tpe_refine | 100 | 19.92 | 5.272 | 6.981e-07 | 1.634e-06 | 1.07e-07 | 0.0005607 | 0.0006195 |
| Sphere | raw | clean | tpe_gp | 84 | 45.9 | 21.98 | 0.003201 | 0.01286 | 4.836e-05 | 0.02371 | 0.05137 |
| Sphere | raw | clean | tpe_gp_w | 82 | 45.59 | 18.08 | 0.002107 | 0.008753 | 8.585e-05 | 0.02206 | 0.04025 |
| Sphere | raw | clean | tpe_gp_refine | 100 | 15.06 | 2.275 | 1.542e-06 | 4.428e-06 | 2.609e-07 | 0.0007865 | 0.0009609 |
| Sphere | raw | clean | optuna | 6 | 64 | 25.73 | 0.01705 | 0.01828 | 0.01214 | 0.1141 | 0.06343 |
| Sphere | raw | noisy_y | random | 0 |  |  | 0.4018 | 0.4152 | 0.2598 | 0.5556 | 0.3051 |
| Sphere | raw | noisy_y | tpe | 26 | 64.92 | 21.01 | 0.126 | 0.2748 | 0.009966 | 0.229 | 0.2712 |
| Sphere | raw | noisy_y | tpe_w_smooth | 16 | 61.88 | 27.4 | 0.1708 | 0.3343 | 0.02159 | 0.2826 | 0.3016 |
| Sphere | raw | noisy_y | tpe_w_smooth_inv | 24 | 60.58 | 23.67 | 0.09846 | 0.2019 | 0.006436 | 0.2027 | 0.2396 |
| Sphere | raw | noisy_y | tpe_w_sign | 22 | 67.45 | 19.04 | 0.1999 | 0.4695 | 0.01408 | 0.2726 | 0.3543 |
| Sphere | raw | noisy_y | tpe_w_sign_inv | 36 | 68.33 | 23.03 | 0.09839 | 0.2052 | 0.005151 | 0.1966 | 0.2444 |
| Sphere | raw | noisy_y | tpe_refine | 98 | 24.92 | 13.78 | 0.0006047 | 0.0008322 | 0.0003843 | 0.01943 | 0.01507 |
| Sphere | raw | noisy_y | tpe_gp | 58 | 46.55 | 24.42 | 0.004551 | 0.007789 | 0.002328 | 0.05501 | 0.03906 |
| Sphere | raw | noisy_y | tpe_gp_w | 56 | 45.86 | 15.54 | 0.005578 | 0.01099 | 0.002158 | 0.05767 | 0.04745 |
| Sphere | raw | noisy_y | tpe_gp_refine | 98 | 18.86 | 9.413 | 0.0007766 | 0.001039 | 0.000392 | 0.02245 | 0.01651 |
| Sphere | raw | noisy_y | optuna | 8 | 66 | 22.55 | 0.01714 | 0.01815 | 0.01334 | 0.1154 | 0.06175 |
| Sphere | norm | clean | random | 0 |  |  | 0.4018 | 0.4152 | 0.2598 | 0.5556 | 0.3051 |
| Sphere | norm | clean | tpe | 36 | 59.28 | 22.93 | 0.1392 | 0.2829 | 0.01457 | 0.2364 | 0.2887 |
| Sphere | norm | clean | tpe_w_smooth | 20 | 48.8 | 21.74 | 0.1765 | 0.3299 | 0.03297 | 0.2854 | 0.3084 |
| Sphere | norm | clean | tpe_w_smooth_inv | 46 | 56.52 | 23.64 | 0.09304 | 0.1731 | 0.003277 | 0.19 | 0.2386 |
| Sphere | norm | clean | tpe_w_sign | 28 | 61.79 | 26.3 | 0.1648 | 0.3993 | 0.01599 | 0.2486 | 0.3209 |
| Sphere | norm | clean | tpe_w_sign_inv | 48 | 59.71 | 23.62 | 0.0918 | 0.1901 | 0.002821 | 0.1792 | 0.2443 |
| Sphere | norm | clean | tpe_refine | 100 | 19.92 | 5.272 | 6.981e-07 | 1.634e-06 | 1.07e-07 | 0.0005607 | 0.0006195 |
| Sphere | norm | clean | tpe_gp | 46 | 54.48 | 22.02 | 0.08402 | 0.1609 | 0.002399 | 0.1776 | 0.2291 |
| Sphere | norm | clean | tpe_gp_w | 28 | 62.43 | 23.61 | 0.1011 | 0.1779 | 0.01158 | 0.211 | 0.2379 |
| Sphere | norm | clean | tpe_gp_refine | 100 | 18.92 | 4.354 | 4.024e-07 | 6.195e-07 | 1.431e-07 | 0.0004692 | 0.0004269 |
| Sphere | norm | clean | optuna | 6 | 64 | 25.73 | 0.01705 | 0.01828 | 0.01214 | 0.1141 | 0.06343 |
| Sphere | norm | noisy_y | random | 0 |  |  | 0.4018 | 0.4152 | 0.2598 | 0.5556 | 0.3051 |
| Sphere | norm | noisy_y | tpe | 26 | 64.92 | 21.01 | 0.126 | 0.2748 | 0.009966 | 0.229 | 0.2712 |
| Sphere | norm | noisy_y | tpe_w_smooth | 16 | 61.88 | 27.4 | 0.1708 | 0.3343 | 0.02159 | 0.2826 | 0.3016 |
| Sphere | norm | noisy_y | tpe_w_smooth_inv | 24 | 60.58 | 23.67 | 0.09846 | 0.2019 | 0.006436 | 0.2027 | 0.2396 |
| Sphere | norm | noisy_y | tpe_w_sign | 22 | 67.45 | 19.04 | 0.1999 | 0.4695 | 0.01408 | 0.2726 | 0.3543 |
| Sphere | norm | noisy_y | tpe_w_sign_inv | 36 | 68.33 | 23.03 | 0.09839 | 0.2052 | 0.005151 | 0.1966 | 0.2444 |
| Sphere | norm | noisy_y | tpe_refine | 98 | 24.92 | 13.78 | 0.0006047 | 0.0008322 | 0.0003843 | 0.01943 | 0.01507 |
| Sphere | norm | noisy_y | tpe_gp | 32 | 62.75 | 20.19 | 0.08345 | 0.1687 | 0.006436 | 0.1855 | 0.2214 |
| Sphere | norm | noisy_y | tpe_gp_w | 24 | 63.08 | 20.98 | 0.08862 | 0.1561 | 0.01582 | 0.2087 | 0.2123 |
| Sphere | norm | noisy_y | tpe_gp_refine | 96 | 24.12 | 14.38 | 0.00107 | 0.001232 | 0.0006578 | 0.02769 | 0.01741 |
| Sphere | norm | noisy_y | optuna | 8 | 66 | 22.55 | 0.01714 | 0.01815 | 0.01334 | 0.1154 | 0.06175 |
| Rosenbrock | raw | clean | random | 12 | 50.5 | 18.25 | 0.6699 | 0.6726 | 0.4125 | 0.8094 | 0.5436 |
| Rosenbrock | raw | clean | tpe | 8 | 20 | 2.915 | 1.533 | 1.804 | 0.5969 | 1.274 | 0.6918 |
| Rosenbrock | raw | clean | tpe_w_smooth | 14 | 25 | 7.982 | 1.379 | 1.742 | 0.5311 | 1.236 | 0.7338 |
| Rosenbrock | raw | clean | tpe_w_smooth_inv | 18 | 36.22 | 20.86 | 1.376 | 1.622 | 0.5575 | 1.248 | 0.68 |
| Rosenbrock | raw | clean | tpe_w_sign | 8 | 26.5 | 6.225 | 1.589 | 1.794 | 0.8557 | 1.322 | 0.7205 |
| Rosenbrock | raw | clean | tpe_w_sign_inv | 14 | 32.29 | 17.87 | 1.531 | 1.87 | 0.5575 | 1.292 | 0.7295 |
| Rosenbrock | raw | clean | tpe_refine | 24 | 38.5 | 27.35 | 0.3954 | 0.5708 | 0.2776 | 0.9035 | 0.6115 |
| Rosenbrock | raw | clean | tpe_gp | 34 | 28.88 | 17.39 | 0.4135 | 1.057 | 0.1122 | 0.7635 | 0.6618 |
| Rosenbrock | raw | clean | tpe_gp_w | 8 | 42 | 13.36 | 0.2954 | 0.2597 | 0.2073 | 0.8261 | 0.4406 |
| Rosenbrock | raw | clean | tpe_gp_refine | 14 | 32 | 23.84 | 0.2261 | 0.1639 | 0.2181 | 0.7095 | 0.4471 |
| Rosenbrock | raw | clean | optuna | 32 | 55.25 | 22.27 | 0.3045 | 0.848 | 0.1564 | 0.6479 | 0.4841 |
| Rosenbrock | raw | noisy_y | random | 12 | 50.5 | 18.25 | 0.6715 | 0.6731 | 0.4125 | 0.8068 | 0.5421 |
| Rosenbrock | raw | noisy_y | tpe | 10 | 21.6 | 4.128 | 1.593 | 1.825 | 0.5398 | 1.323 | 0.7066 |
| Rosenbrock | raw | noisy_y | tpe_w_smooth | 16 | 26.25 | 9.692 | 1.483 | 1.761 | 0.5073 | 1.253 | 0.7202 |
| Rosenbrock | raw | noisy_y | tpe_w_smooth_inv | 12 | 21.17 | 3.078 | 1.461 | 1.648 | 0.581 | 1.285 | 0.6764 |
| Rosenbrock | raw | noisy_y | tpe_w_sign | 12 | 28.33 | 6.368 | 1.651 | 1.833 | 0.7548 | 1.305 | 0.7307 |
| Rosenbrock | raw | noisy_y | tpe_w_sign_inv | 12 | 24.67 | 6.749 | 1.62 | 1.896 | 0.5812 | 1.301 | 0.7473 |
| Rosenbrock | raw | noisy_y | tpe_refine | 18 | 46.11 | 29.57 | 0.4284 | 0.5503 | 0.3267 | 1.017 | 0.6003 |
| Rosenbrock | raw | noisy_y | tpe_gp | 32 | 28.44 | 13.09 | 0.2657 | 0.3022 | 0.229 | 0.8299 | 0.5308 |
| Rosenbrock | raw | noisy_y | tpe_gp_w | 8 | 60 | 22.01 | 0.3183 | 0.2396 | 0.245 | 0.8663 | 0.4368 |
| Rosenbrock | raw | noisy_y | tpe_gp_refine | 12 | 20.67 | 13.1 | 0.23 | 0.1687 | 0.1987 | 0.6716 | 0.4387 |
| Rosenbrock | raw | noisy_y | optuna | 26 | 51.77 | 20.61 | 0.3558 | 0.8502 | 0.1872 | 0.6932 | 0.4851 |
| Rosenbrock | norm | clean | random | 12 | 50.5 | 18.25 | 0.6699 | 0.6726 | 0.4125 | 0.8094 | 0.5436 |
| Rosenbrock | norm | clean | tpe | 8 | 20 | 2.915 | 1.533 | 1.804 | 0.5969 | 1.274 | 0.6918 |
| Rosenbrock | norm | clean | tpe_w_smooth | 14 | 25 | 7.982 | 1.379 | 1.742 | 0.5311 | 1.236 | 0.7338 |
| Rosenbrock | norm | clean | tpe_w_smooth_inv | 18 | 36.22 | 20.86 | 1.376 | 1.622 | 0.5575 | 1.248 | 0.68 |
| Rosenbrock | norm | clean | tpe_w_sign | 8 | 26.5 | 6.225 | 1.589 | 1.794 | 0.8557 | 1.322 | 0.7205 |
| Rosenbrock | norm | clean | tpe_w_sign_inv | 14 | 32.29 | 17.87 | 1.531 | 1.87 | 0.5575 | 1.292 | 0.7295 |
| Rosenbrock | norm | clean | tpe_refine | 24 | 38.5 | 27.35 | 0.3954 | 0.5708 | 0.2776 | 0.9035 | 0.6115 |
| Rosenbrock | norm | clean | tpe_gp | 12 | 28.5 | 9.708 | 1.78 | 1.951 | 0.6913 | 1.307 | 0.709 |
| Rosenbrock | norm | clean | tpe_gp_w | 10 | 25.2 | 4.49 | 1.47 | 1.59 | 0.9947 | 1.298 | 0.635 |
| Rosenbrock | norm | clean | tpe_gp_refine | 26 | 28.46 | 20.74 | 0.5048 | 1.066 | 0.2376 | 0.8659 | 0.6653 |
| Rosenbrock | norm | clean | optuna | 32 | 55.25 | 22.27 | 0.3045 | 0.848 | 0.1564 | 0.6479 | 0.4841 |
| Rosenbrock | norm | noisy_y | random | 12 | 50.5 | 18.25 | 0.6715 | 0.6731 | 0.4125 | 0.8068 | 0.5421 |
| Rosenbrock | norm | noisy_y | tpe | 10 | 21.6 | 4.128 | 1.593 | 1.825 | 0.5398 | 1.323 | 0.7066 |
| Rosenbrock | norm | noisy_y | tpe_w_smooth | 16 | 26.25 | 9.692 | 1.483 | 1.761 | 0.5073 | 1.253 | 0.7202 |
| Rosenbrock | norm | noisy_y | tpe_w_smooth_inv | 12 | 21.17 | 3.078 | 1.461 | 1.648 | 0.581 | 1.285 | 0.6764 |
| Rosenbrock | norm | noisy_y | tpe_w_sign | 12 | 28.33 | 6.368 | 1.651 | 1.833 | 0.7548 | 1.305 | 0.7307 |
| Rosenbrock | norm | noisy_y | tpe_w_sign_inv | 12 | 24.67 | 6.749 | 1.62 | 1.896 | 0.5812 | 1.301 | 0.7473 |
| Rosenbrock | norm | noisy_y | tpe_refine | 18 | 46.11 | 29.57 | 0.4284 | 0.5503 | 0.3267 | 1.017 | 0.6003 |
| Rosenbrock | norm | noisy_y | tpe_gp | 12 | 32.5 | 13.15 | 1.865 | 1.931 | 0.9586 | 1.33 | 0.7003 |
| Rosenbrock | norm | noisy_y | tpe_gp_w | 10 | 23.2 | 3.311 | 1.455 | 1.528 | 0.9447 | 1.3 | 0.6123 |
| Rosenbrock | norm | noisy_y | tpe_gp_refine | 26 | 30.23 | 23.47 | 0.4575 | 0.9641 | 0.2682 | 0.8704 | 0.6204 |
| Rosenbrock | norm | noisy_y | optuna | 26 | 51.77 | 20.61 | 0.3558 | 0.8502 | 0.1872 | 0.6932 | 0.4851 |
| Rastrigin | raw | clean | random | 2 | 13 | 0 | 5.46 | 2.572 | 5.195 | 1.474 | 0.7244 |
| Rastrigin | raw | clean | tpe | 28 | 44.71 | 25.21 | 2.775 | 3.333 | 1.263 | 1.328 | 0.9755 |
| Rastrigin | raw | clean | tpe_w_smooth | 8 | 38.5 | 22.61 | 3.43 | 3.367 | 2.165 | 1.445 | 0.818 |
| Rastrigin | raw | clean | tpe_w_smooth_inv | 36 | 51.94 | 27.31 | 2.721 | 3.29 | 1.027 | 1.32 | 0.9556 |
| Rastrigin | raw | clean | tpe_w_sign | 8 | 49.5 | 28.78 | 3.915 | 3.462 | 3.082 | 1.559 | 0.83 |
| Rastrigin | raw | clean | tpe_w_sign_inv | 26 | 43.69 | 26.02 | 2.553 | 2.781 | 1.023 | 1.307 | 0.8647 |
| Rastrigin | raw | clean | tpe_refine | 76 | 29.66 | 19.62 | 1.136 | 1.314 | 0.9951 | 0.8131 | 0.6717 |
| Rastrigin | raw | clean | tpe_gp | 8 | 59.5 | 29.21 | 3.599 | 3.157 | 2.289 | 1.456 | 0.8172 |
| Rastrigin | raw | clean | tpe_gp_w | 20 | 80.5 | 11.16 | 2.127 | 1.347 | 1.895 | 1.096 | 0.6049 |
| Rastrigin | raw | clean | tpe_gp_refine | 58 | 38.86 | 24.7 | 1.226 | 1.168 | 0.9964 | 0.8937 | 0.5878 |
| Rastrigin | raw | clean | optuna | 10 | 70.6 | 26.59 | 2.58 | 1.439 | 2.384 | 1.026 | 0.6194 |
| Rastrigin | raw | noisy_y | random | 2 | 13 | 0 | 5.465 | 2.57 | 5.195 | 1.493 | 0.7171 |
| Rastrigin | raw | noisy_y | tpe | 16 | 28.5 | 10.54 | 3.453 | 3.628 | 2.03 | 1.46 | 0.9404 |
| Rastrigin | raw | noisy_y | tpe_w_smooth | 8 | 49 | 27 | 3.435 | 3.284 | 2.197 | 1.426 | 0.8133 |
| Rastrigin | raw | noisy_y | tpe_w_smooth_inv | 24 | 41.75 | 19.79 | 2.914 | 3.043 | 2.039 | 1.414 | 0.861 |
| Rastrigin | raw | noisy_y | tpe_w_sign | 4 | 31.5 | 17.5 | 3.769 | 3.067 | 2.96 | 1.527 | 0.7789 |
| Rastrigin | raw | noisy_y | tpe_w_sign_inv | 20 | 35.9 | 22.16 | 2.701 | 2.645 | 2.032 | 1.312 | 0.8438 |
| Rastrigin | raw | noisy_y | tpe_refine | 52 | 28.12 | 19.5 | 1.189 | 1.196 | 1.01 | 0.8913 | 0.5933 |
| Rastrigin | raw | noisy_y | tpe_gp | 12 | 38.5 | 15.28 | 3.456 | 2.462 | 3.064 | 1.491 | 0.7547 |
| Rastrigin | raw | noisy_y | tpe_gp_w | 18 | 72.89 | 17.67 | 2.2 | 1.628 | 1.678 | 1.092 | 0.6221 |
| Rastrigin | raw | noisy_y | tpe_gp_refine | 44 | 37.55 | 22.18 | 1.521 | 1.749 | 1.064 | 0.8836 | 0.7493 |
| Rastrigin | raw | noisy_y | optuna | 12 | 60 | 28.65 | 2.523 | 1.555 | 2.144 | 1.003 | 0.5555 |
| Rastrigin | norm | clean | random | 2 | 13 | 0 | 5.46 | 2.572 | 5.195 | 1.474 | 0.7244 |
| Rastrigin | norm | clean | tpe | 28 | 44.71 | 25.21 | 2.775 | 3.333 | 1.263 | 1.328 | 0.9755 |
| Rastrigin | norm | clean | tpe_w_smooth | 8 | 38.5 | 22.61 | 3.43 | 3.367 | 2.165 | 1.445 | 0.818 |
| Rastrigin | norm | clean | tpe_w_smooth_inv | 36 | 51.94 | 27.31 | 2.721 | 3.29 | 1.027 | 1.32 | 0.9556 |
| Rastrigin | norm | clean | tpe_w_sign | 8 | 49.5 | 28.78 | 3.915 | 3.462 | 3.082 | 1.559 | 0.83 |
| Rastrigin | norm | clean | tpe_w_sign_inv | 26 | 43.69 | 26.02 | 2.553 | 2.781 | 1.023 | 1.307 | 0.8647 |
| Rastrigin | norm | clean | tpe_refine | 76 | 29.66 | 19.62 | 1.136 | 1.314 | 0.9951 | 0.8131 | 0.6717 |
| Rastrigin | norm | clean | tpe_gp | 24 | 46 | 26.15 | 2.436 | 1.981 | 2.002 | 1.283 | 0.7334 |
| Rastrigin | norm | clean | tpe_gp_w | 18 | 37 | 16.1 | 2.674 | 2.156 | 2.012 | 1.341 | 0.7151 |
| Rastrigin | norm | clean | tpe_gp_refine | 64 | 31.31 | 18.09 | 1.043 | 1.034 | 0.9953 | 0.7949 | 0.5959 |
| Rastrigin | norm | clean | optuna | 10 | 70.6 | 26.59 | 2.58 | 1.439 | 2.384 | 1.026 | 0.6194 |
| Rastrigin | norm | noisy_y | random | 2 | 13 | 0 | 5.465 | 2.57 | 5.195 | 1.493 | 0.7171 |
| Rastrigin | norm | noisy_y | tpe | 16 | 28.5 | 10.54 | 3.453 | 3.628 | 2.03 | 1.46 | 0.9404 |
| Rastrigin | norm | noisy_y | tpe_w_smooth | 8 | 49 | 27 | 3.435 | 3.284 | 2.197 | 1.426 | 0.8133 |
| Rastrigin | norm | noisy_y | tpe_w_smooth_inv | 24 | 41.75 | 19.79 | 2.914 | 3.043 | 2.039 | 1.414 | 0.861 |
| Rastrigin | norm | noisy_y | tpe_w_sign | 4 | 31.5 | 17.5 | 3.769 | 3.067 | 2.96 | 1.527 | 0.7789 |
| Rastrigin | norm | noisy_y | tpe_w_sign_inv | 20 | 35.9 | 22.16 | 2.701 | 2.645 | 2.032 | 1.312 | 0.8438 |
| Rastrigin | norm | noisy_y | tpe_refine | 52 | 28.12 | 19.5 | 1.189 | 1.196 | 1.01 | 0.8913 | 0.5933 |
| Rastrigin | norm | noisy_y | tpe_gp | 18 | 54.89 | 24.84 | 3.168 | 2.645 | 2.223 | 1.428 | 0.7756 |
| Rastrigin | norm | noisy_y | tpe_gp_w | 12 | 36.67 | 15.98 | 2.951 | 2.147 | 2.179 | 1.389 | 0.701 |
| Rastrigin | norm | noisy_y | tpe_gp_refine | 48 | 38.46 | 25.59 | 1.248 | 1.116 | 1.044 | 0.911 | 0.5825 |
| Rastrigin | norm | noisy_y | optuna | 12 | 60 | 28.65 | 2.523 | 1.555 | 2.144 | 1.003 | 0.5555 |
| Ackley | raw | clean | random | 2 | 13 | 0 | 2.843 | 1.059 | 3.014 | 0.6475 | 0.3763 |
| Ackley | raw | clean | tpe | 32 | 40.44 | 24.36 | 2.043 | 1.582 | 2.581 | 0.7313 | 0.6348 |
| Ackley | raw | clean | tpe_w_smooth | 42 | 36.29 | 22.5 | 1.429 | 1.328 | 0.8558 | 0.4699 | 0.5021 |
| Ackley | raw | clean | tpe_w_smooth_inv | 30 | 39.07 | 24.14 | 2.073 | 1.437 | 2.58 | 0.7205 | 0.5477 |
| Ackley | raw | clean | tpe_w_sign | 44 | 37.45 | 20.53 | 1.603 | 1.405 | 0.9792 | 0.5353 | 0.5215 |
| Ackley | raw | clean | tpe_w_sign_inv | 40 | 50.25 | 25.31 | 1.674 | 1.568 | 1.971 | 0.5648 | 0.6111 |
| Ackley | raw | clean | tpe_refine | 76 | 31.05 | 24.14 | 0.7898 | 1.475 | 0.003264 | 0.2999 | 0.5685 |
| Ackley | raw | clean | tpe_gp | 86 | 39.23 | 20.19 | 0.4545 | 0.9426 | 0.04672 | 0.159 | 0.3465 |
| Ackley | raw | clean | tpe_gp_w | 90 | 44.33 | 22.11 | 0.3911 | 1.135 | 0.05787 | 0.1296 | 0.4672 |
| Ackley | raw | clean | tpe_gp_refine | 84 | 18.95 | 13.29 | 0.4359 | 0.999 | 0.003501 | 0.1614 | 0.371 |
| Ackley | raw | clean | optuna | 40 | 69.5 | 22.74 | 0.655 | 0.4328 | 0.6066 | 0.1112 | 0.05658 |
| Ackley | raw | noisy_y | random | 2 | 13 | 0 | 2.844 | 1.06 | 3.014 | 0.657 | 0.3866 |
| Ackley | raw | noisy_y | tpe | 44 | 40.23 | 18.18 | 1.812 | 1.651 | 2.58 | 0.6559 | 0.6475 |
| Ackley | raw | noisy_y | tpe_w_smooth | 46 | 35.57 | 20.24 | 1.456 | 1.498 | 0.5668 | 0.4717 | 0.5626 |
| Ackley | raw | noisy_y | tpe_w_smooth_inv | 44 | 50.05 | 27.24 | 1.62 | 1.623 | 1.232 | 0.5333 | 0.6326 |
| Ackley | raw | noisy_y | tpe_w_sign | 50 | 41.16 | 23.07 | 1.476 | 1.486 | 0.5179 | 0.4761 | 0.5665 |
| Ackley | raw | noisy_y | tpe_w_sign_inv | 40 | 48.85 | 22.23 | 1.533 | 1.499 | 0.9373 | 0.5214 | 0.5982 |
| Ackley | raw | noisy_y | tpe_refine | 66 | 28.3 | 21.25 | 1.065 | 1.552 | 0.03327 | 0.4021 | 0.5994 |
| Ackley | raw | noisy_y | tpe_gp | 88 | 39.52 | 18.08 | 0.4187 | 0.857 | 0.08421 | 0.1347 | 0.3121 |
| Ackley | raw | noisy_y | tpe_gp_w | 84 | 42.69 | 19.49 | 0.4513 | 0.8581 | 0.07004 | 0.1448 | 0.3068 |
| Ackley | raw | noisy_y | tpe_gp_refine | 90 | 22.18 | 21.64 | 0.2954 | 0.8152 | 0.02178 | 0.08897 | 0.254 |
| Ackley | raw | noisy_y | optuna | 36 | 62.33 | 23.32 | 0.7508 | 0.4398 | 0.6825 | 0.1243 | 0.05549 |
| Ackley | norm | clean | random | 2 | 13 | 0 | 2.843 | 1.059 | 3.014 | 0.6475 | 0.3763 |
| Ackley | norm | clean | tpe | 32 | 40.44 | 24.36 | 2.043 | 1.582 | 2.581 | 0.7313 | 0.6348 |
| Ackley | norm | clean | tpe_w_smooth | 42 | 36.29 | 22.5 | 1.429 | 1.328 | 0.8558 | 0.4699 | 0.5021 |
| Ackley | norm | clean | tpe_w_smooth_inv | 30 | 39.07 | 24.14 | 2.073 | 1.437 | 2.58 | 0.7205 | 0.5477 |
| Ackley | norm | clean | tpe_w_sign | 44 | 37.45 | 20.53 | 1.603 | 1.405 | 0.9792 | 0.5353 | 0.5215 |
| Ackley | norm | clean | tpe_w_sign_inv | 40 | 50.25 | 25.31 | 1.674 | 1.568 | 1.971 | 0.5648 | 0.6111 |
| Ackley | norm | clean | tpe_refine | 76 | 31.05 | 24.14 | 0.7898 | 1.475 | 0.003264 | 0.2999 | 0.5685 |
| Ackley | norm | clean | tpe_gp | 52 | 40.92 | 23.09 | 1.278 | 1.393 | 0.3173 | 0.4349 | 0.4987 |
| Ackley | norm | clean | tpe_gp_w | 48 | 54.75 | 22.88 | 1.388 | 1.345 | 0.6893 | 0.4701 | 0.5038 |
| Ackley | norm | clean | tpe_gp_refine | 68 | 28.88 | 22.62 | 0.889 | 1.318 | 0.005807 | 0.3163 | 0.4854 |
| Ackley | norm | clean | optuna | 40 | 69.5 | 22.74 | 0.655 | 0.4328 | 0.6066 | 0.1112 | 0.05658 |
| Ackley | norm | noisy_y | random | 2 | 13 | 0 | 2.844 | 1.06 | 3.014 | 0.657 | 0.3866 |
| Ackley | norm | noisy_y | tpe | 44 | 40.23 | 18.18 | 1.812 | 1.651 | 2.58 | 0.6559 | 0.6475 |
| Ackley | norm | noisy_y | tpe_w_smooth | 46 | 35.57 | 20.24 | 1.456 | 1.498 | 0.5668 | 0.4717 | 0.5626 |
| Ackley | norm | noisy_y | tpe_w_smooth_inv | 44 | 50.05 | 27.24 | 1.62 | 1.623 | 1.232 | 0.5333 | 0.6326 |
| Ackley | norm | noisy_y | tpe_w_sign | 50 | 41.16 | 23.07 | 1.476 | 1.486 | 0.5179 | 0.4761 | 0.5665 |
| Ackley | norm | noisy_y | tpe_w_sign_inv | 40 | 48.85 | 22.23 | 1.533 | 1.499 | 0.9373 | 0.5214 | 0.5982 |
| Ackley | norm | noisy_y | tpe_refine | 66 | 28.3 | 21.25 | 1.065 | 1.552 | 0.03327 | 0.4021 | 0.5994 |
| Ackley | norm | noisy_y | tpe_gp | 56 | 40.68 | 23.67 | 1.27 | 1.533 | 0.2775 | 0.431 | 0.5724 |
| Ackley | norm | noisy_y | tpe_gp_w | 36 | 54.61 | 26.1 | 1.716 | 1.498 | 1.481 | 0.5701 | 0.5759 |
| Ackley | norm | noisy_y | tpe_gp_refine | 66 | 33 | 26.32 | 0.9148 | 1.322 | 0.02827 | 0.3317 | 0.4906 |
| Ackley | norm | noisy_y | optuna | 36 | 62.33 | 23.32 | 0.7508 | 0.4398 | 0.6825 | 0.1243 | 0.05549 |

## Выводы (строго по числам прогона)

1. **Базовый `tpe` осмыслен:** средний success 25.0% против random 4.0% и optuna 21.2% (порог success строгий, поэтому смотрите и на final_dist_y).
2. **Нормализация цели инвариантна** для `tpe`, всех форм w(x) и `tpe_refine` (gap=0), и **важна только для GP-методов** (gap 1.4): GP мешает y-единицы с лог-плотностью.
3. **Класс black-box: GP-переранжирование помогает** — `tpe_gp` (градиент НЕ использует) даёт 6 значимых улучшений над `tpe`, не уступая `optuna` (6).
4. **Класс white-box (мягкий вес по ∇f): не помогает** — ни одна из 4 форм w(x) не даёт значимого улучшения (`tpe_w_*`: всего 0 значимых), хотя по средним отдельные формы «выигрывают» в части ячеек. Причина: w∈[0.8,1.2] слишком слаб, чтобы менять argmax l/g.
5. **Класс white-box (refinement = градиентный спуск): доминирует, но тривиально** — `tpe_refine` 12 и `tpe_gp_refine` 12 значимых улучшений. Это ожидаемо: refinement — обычный градиентный спуск по ТОЧНОМУ ∇f, т.е. ВЕРХНЯЯ ГРАНИЦА «что даёт точный градиент», а не доказательство пользы для самого TPE.

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
