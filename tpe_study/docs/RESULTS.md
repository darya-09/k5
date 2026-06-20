# RESULTS — табличные результаты и графики

> Сгенерировано автоматически из `results/tables/*.csv` (реальный прогон `run.py`).

## Конфигурация прогона

```json
{
  "seeds": 20,
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
| optuna | 14.4 |
| random | 6.2 |
| tpe | 33.8 |
| tpe_gp | 42.8 |
| tpe_gradw | 31.2 |
| tpe_gradw_gp | 34.1 |

## Авто-выводы (из чисел этого прогона)

- **Инвариантность нормализации для чистого rank-based `tpe`** (clean): максимальный |raw − norm| по final_dist_y = **0** → при ~0 это строго подтверждает: монотонно-аффинное масштабирование цели НЕ влияет на ранговый TPE.
- **Модификации масштабо-зависимы:** тот же разрыв для `tpe_gradw` = 0.923, для `tpe_gp` = 1.52. Причина: градиентный вес зависит от масштаба ∇, а GP-член `−μ+βσ` в y-единицах конкурирует с лог-плотностью → нормализация меняет баланс. Вывод: нормализация нужна именно для grad/GP-вариантов, а для базового TPE бесполезна.
- **Как часто модификация бьёт baseline `tpe`** (доля ячеек, % по final_dist_y):
  - `optuna`: 50.0%
  - `random`: 25.0%
  - `tpe_gp`: 68.8%
  - `tpe_gradw`: 56.2%
  - `tpe_gradw_gp`: 62.5%

## Ablation: каждая модификация против baseline `tpe`

Δ = algo − tpe по final_dist_y (меньше нуля → модификация лучше).

| function | scale | data | algorithm | tpe_final_dist_y | algo_final_dist_y | delta_dist_y(algo-tpe) | better_than_tpe | tpe_success_% | algo_success_% |
|---|---|---|---|---|---|---|---|---|---|
| Ackley | norm | clean | tpe_gradw | 1.021 | 1.112 | 0.09089 | False | 65 | 60 |
| Ackley | norm | clean | tpe_gp | 1.021 | 1.083 | 0.06212 | False | 65 | 60 |
| Ackley | norm | clean | tpe_gradw_gp | 1.021 | 1.052 | 0.03139 | False | 65 | 60 |
| Ackley | norm | clean | optuna | 1.021 | 1.119 | 0.09812 | False | 65 | 15 |
| Ackley | norm | clean | random | 1.021 | 2.677 | 1.657 | False | 65 | 5 |
| Ackley | norm | noisy_y | tpe_gradw | 0.9444 | 0.9383 | -0.006108 | True | 70 | 75 |
| Ackley | norm | noisy_y | tpe_gp | 0.9444 | 1.123 | 0.1789 | False | 70 | 60 |
| Ackley | norm | noisy_y | tpe_gradw_gp | 0.9444 | 0.9854 | 0.04101 | False | 70 | 60 |
| Ackley | norm | noisy_y | optuna | 0.9444 | 1.05 | 0.1055 | False | 70 | 20 |
| Ackley | norm | noisy_y | random | 0.9444 | 2.677 | 1.733 | False | 70 | 5 |
| Ackley | raw | clean | tpe_gradw | 1.021 | 0.5245 | -0.4963 | True | 65 | 80 |
| Ackley | raw | clean | tpe_gp | 1.021 | 0.4342 | -0.5865 | True | 65 | 80 |
| Ackley | raw | clean | tpe_gradw_gp | 1.021 | 0.2109 | -0.8099 | True | 65 | 90 |
| Ackley | raw | clean | optuna | 1.021 | 1.119 | 0.09812 | False | 65 | 15 |
| Ackley | raw | clean | random | 1.021 | 2.677 | 1.657 | False | 65 | 5 |
| Ackley | raw | noisy_y | tpe_gradw | 0.9444 | 0.8732 | -0.07121 | True | 70 | 65 |
| Ackley | raw | noisy_y | tpe_gp | 0.9444 | 0.2687 | -0.6757 | True | 70 | 85 |
| Ackley | raw | noisy_y | tpe_gradw_gp | 0.9444 | 0.5711 | -0.3733 | True | 70 | 85 |
| Ackley | raw | noisy_y | optuna | 0.9444 | 1.05 | 0.1055 | False | 70 | 20 |
| Ackley | raw | noisy_y | random | 0.9444 | 2.677 | 1.733 | False | 70 | 5 |
| Rastrigin | norm | clean | tpe_gradw | 2.37 | 2.875 | 0.5045 | False | 30 | 35 |
| Rastrigin | norm | clean | tpe_gp | 2.37 | 1.913 | -0.4569 | True | 30 | 15 |
| Rastrigin | norm | clean | tpe_gradw_gp | 2.37 | 3.552 | 1.182 | False | 30 | 0 |
| Rastrigin | norm | clean | optuna | 2.37 | 2.893 | 0.5227 | False | 30 | 10 |
| Rastrigin | norm | clean | random | 2.37 | 6.032 | 3.662 | False | 30 | 5 |
| Rastrigin | norm | noisy_y | tpe_gradw | 2.478 | 2.621 | 0.1436 | False | 20 | 30 |
| Rastrigin | norm | noisy_y | tpe_gp | 2.478 | 2.491 | 0.01372 | False | 20 | 10 |
| Rastrigin | norm | noisy_y | tpe_gradw_gp | 2.478 | 4.133 | 1.656 | False | 20 | 5 |
| Rastrigin | norm | noisy_y | optuna | 2.478 | 2.564 | 0.08585 | False | 20 | 15 |
| Rastrigin | norm | noisy_y | random | 2.478 | 6.04 | 3.563 | False | 20 | 5 |
| Rastrigin | raw | clean | tpe_gradw | 2.37 | 3.24 | 0.8701 | False | 30 | 5 |
| Rastrigin | raw | clean | tpe_gp | 2.37 | 3.432 | 1.062 | False | 30 | 5 |
| Rastrigin | raw | clean | tpe_gradw_gp | 2.37 | 2.897 | 0.5268 | False | 30 | 10 |
| Rastrigin | raw | clean | optuna | 2.37 | 2.893 | 0.5227 | False | 30 | 10 |
| Rastrigin | raw | clean | random | 2.37 | 6.032 | 3.662 | False | 30 | 5 |
| Rastrigin | raw | noisy_y | tpe_gradw | 2.478 | 3.271 | 0.7934 | False | 20 | 5 |
| Rastrigin | raw | noisy_y | tpe_gp | 2.478 | 3.44 | 0.9619 | False | 20 | 10 |
| Rastrigin | raw | noisy_y | tpe_gradw_gp | 2.478 | 3.085 | 0.6076 | False | 20 | 15 |
| Rastrigin | raw | noisy_y | optuna | 2.478 | 2.564 | 0.08585 | False | 20 | 15 |
| Rastrigin | raw | noisy_y | random | 2.478 | 6.04 | 3.563 | False | 20 | 5 |
| Rosenbrock | norm | clean | tpe_gradw | 1.902 | 1.949 | 0.04745 | False | 10 | 0 |
| Rosenbrock | norm | clean | tpe_gp | 1.902 | 1.563 | -0.3388 | True | 10 | 20 |
| Rosenbrock | norm | clean | tpe_gradw_gp | 1.902 | 1.201 | -0.7006 | True | 10 | 0 |
| Rosenbrock | norm | clean | optuna | 1.902 | 0.2044 | -1.697 | True | 10 | 30 |
| Rosenbrock | norm | clean | random | 1.902 | 0.7622 | -1.14 | True | 10 | 15 |
| Rosenbrock | norm | noisy_y | tpe_gradw | 2.002 | 2.057 | 0.055 | False | 5 | 0 |
| Rosenbrock | norm | noisy_y | tpe_gp | 2.002 | 1.609 | -0.3935 | True | 5 | 20 |
| Rosenbrock | norm | noisy_y | tpe_gradw_gp | 2.002 | 1.266 | -0.7362 | True | 5 | 0 |
| Rosenbrock | norm | noisy_y | optuna | 2.002 | 0.2359 | -1.766 | True | 5 | 25 |
| Rosenbrock | norm | noisy_y | random | 2.002 | 0.7622 | -1.24 | True | 5 | 15 |
| Rosenbrock | raw | clean | tpe_gradw | 1.902 | 1.027 | -0.8753 | True | 10 | 0 |
| Rosenbrock | raw | clean | tpe_gp | 1.902 | 0.5431 | -1.359 | True | 10 | 40 |
| Rosenbrock | raw | clean | tpe_gradw_gp | 1.902 | 0.221 | -1.681 | True | 10 | 10 |
| Rosenbrock | raw | clean | optuna | 1.902 | 0.2044 | -1.697 | True | 10 | 30 |
| Rosenbrock | raw | clean | random | 1.902 | 0.7622 | -1.14 | True | 10 | 15 |
| Rosenbrock | raw | noisy_y | tpe_gradw | 2.002 | 1.021 | -0.981 | True | 5 | 0 |
| Rosenbrock | raw | noisy_y | tpe_gp | 2.002 | 0.5337 | -1.469 | True | 5 | 35 |
| Rosenbrock | raw | noisy_y | tpe_gradw_gp | 2.002 | 0.2347 | -1.768 | True | 5 | 15 |
| Rosenbrock | raw | noisy_y | optuna | 2.002 | 0.2359 | -1.766 | True | 5 | 25 |
| Rosenbrock | raw | noisy_y | random | 2.002 | 0.7622 | -1.24 | True | 5 | 15 |
| Sphere | norm | clean | tpe_gradw | 0.1116 | 0.1028 | -0.008802 | True | 40 | 40 |
| Sphere | norm | clean | tpe_gp | 0.1116 | 0.02784 | -0.08372 | True | 40 | 40 |
| Sphere | norm | clean | tpe_gradw_gp | 0.1116 | 0.07395 | -0.03761 | True | 40 | 45 |
| Sphere | norm | clean | optuna | 0.1116 | 0.02484 | -0.08673 | True | 40 | 0 |
| Sphere | norm | clean | random | 0.1116 | 0.3472 | 0.2356 | False | 40 | 0 |
| Sphere | norm | noisy_y | tpe_gradw | 0.1093 | 0.09458 | -0.01477 | True | 30 | 30 |
| Sphere | norm | noisy_y | tpe_gp | 0.1093 | 0.0272 | -0.08214 | True | 30 | 35 |
| Sphere | norm | noisy_y | tpe_gradw_gp | 0.1093 | 0.06477 | -0.04458 | True | 30 | 15 |
| Sphere | norm | noisy_y | optuna | 0.1093 | 0.02717 | -0.08218 | True | 30 | 0 |
| Sphere | norm | noisy_y | random | 0.1093 | 0.3472 | 0.2378 | False | 30 | 0 |
| Sphere | raw | clean | tpe_gradw | 0.1116 | 0.04789 | -0.06367 | True | 40 | 40 |
| Sphere | raw | clean | tpe_gp | 0.1116 | 0.0001577 | -0.1114 | True | 40 | 95 |
| Sphere | raw | clean | tpe_gradw_gp | 0.1116 | 0.0003189 | -0.1112 | True | 40 | 90 |
| Sphere | raw | clean | optuna | 0.1116 | 0.02484 | -0.08673 | True | 40 | 0 |
| Sphere | raw | clean | random | 0.1116 | 0.3472 | 0.2356 | False | 40 | 0 |
| Sphere | raw | noisy_y | tpe_gradw | 0.1093 | 0.07767 | -0.03167 | True | 30 | 35 |
| Sphere | raw | noisy_y | tpe_gp | 0.1093 | 0.001454 | -0.1079 | True | 30 | 75 |
| Sphere | raw | noisy_y | tpe_gradw_gp | 0.1093 | 0.001926 | -0.1074 | True | 30 | 45 |
| Sphere | raw | noisy_y | optuna | 0.1093 | 0.02717 | -0.08218 | True | 30 | 0 |
| Sphere | raw | noisy_y | random | 0.1093 | 0.3472 | 0.2378 | False | 30 | 0 |

## Ключевые метрики (все ячейки)

| function | scale | data | algorithm | success_rate_% | steps_mean | final_dist_y_mean | final_dist_x_mean |
|---|---|---|---|---|---|---|---|
| Sphere | raw | clean | random | 0 |  | 0.3472 | 0.5042 |
| Sphere | raw | clean | tpe | 40 | 47.5 | 0.1116 | 0.182 |
| Sphere | raw | clean | tpe_gradw | 40 | 34.12 | 0.04789 | 0.1276 |
| Sphere | raw | clean | tpe_gp | 95 | 39 | 0.0001577 | 0.01006 |
| Sphere | raw | clean | tpe_gradw_gp | 90 | 33.83 | 0.0003189 | 0.01233 |
| Sphere | raw | clean | optuna | 0 |  | 0.02484 | 0.1467 |
| Sphere | raw | noisy_y | random | 0 |  | 0.3472 | 0.5042 |
| Sphere | raw | noisy_y | tpe | 30 | 45.17 | 0.1093 | 0.1998 |
| Sphere | raw | noisy_y | tpe_gradw | 35 | 43.43 | 0.07767 | 0.1715 |
| Sphere | raw | noisy_y | tpe_gp | 75 | 40.33 | 0.001454 | 0.03475 |
| Sphere | raw | noisy_y | tpe_gradw_gp | 45 | 33.44 | 0.001926 | 0.04039 |
| Sphere | raw | noisy_y | optuna | 0 |  | 0.02717 | 0.1542 |
| Sphere | norm | clean | random | 0 |  | 0.3472 | 0.5042 |
| Sphere | norm | clean | tpe | 40 | 47.5 | 0.1116 | 0.182 |
| Sphere | norm | clean | tpe_gradw | 40 | 52 | 0.1028 | 0.1891 |
| Sphere | norm | clean | tpe_gp | 40 | 53.12 | 0.02784 | 0.1072 |
| Sphere | norm | clean | tpe_gradw_gp | 45 | 47.44 | 0.07395 | 0.1527 |
| Sphere | norm | clean | optuna | 0 |  | 0.02484 | 0.1467 |
| Sphere | norm | noisy_y | random | 0 |  | 0.3472 | 0.5042 |
| Sphere | norm | noisy_y | tpe | 30 | 45.17 | 0.1093 | 0.1998 |
| Sphere | norm | noisy_y | tpe_gradw | 30 | 56.67 | 0.09458 | 0.2069 |
| Sphere | norm | noisy_y | tpe_gp | 35 | 54.29 | 0.0272 | 0.1014 |
| Sphere | norm | noisy_y | tpe_gradw_gp | 15 | 30 | 0.06477 | 0.1732 |
| Sphere | norm | noisy_y | optuna | 0 |  | 0.02717 | 0.1542 |
| Rosenbrock | raw | clean | random | 15 | 49 | 0.7622 | 0.7928 |
| Rosenbrock | raw | clean | tpe | 10 | 47 | 1.902 | 1.444 |
| Rosenbrock | raw | clean | tpe_gradw | 0 |  | 1.027 | 0.9796 |
| Rosenbrock | raw | clean | tpe_gp | 40 | 25.75 | 0.5431 | 0.7514 |
| Rosenbrock | raw | clean | tpe_gradw_gp | 10 | 56 | 0.221 | 0.7029 |
| Rosenbrock | raw | clean | optuna | 30 | 45.83 | 0.2044 | 0.696 |
| Rosenbrock | raw | noisy_y | random | 15 | 49 | 0.7622 | 0.7928 |
| Rosenbrock | raw | noisy_y | tpe | 5 | 15 | 2.002 | 1.501 |
| Rosenbrock | raw | noisy_y | tpe_gradw | 0 |  | 1.021 | 1.075 |
| Rosenbrock | raw | noisy_y | tpe_gp | 35 | 22 | 0.5337 | 0.8095 |
| Rosenbrock | raw | noisy_y | tpe_gradw_gp | 15 | 60.67 | 0.2347 | 0.7361 |
| Rosenbrock | raw | noisy_y | optuna | 25 | 46 | 0.2359 | 0.7533 |
| Rosenbrock | norm | clean | random | 15 | 49 | 0.7622 | 0.7928 |
| Rosenbrock | norm | clean | tpe | 10 | 47 | 1.902 | 1.444 |
| Rosenbrock | norm | clean | tpe_gradw | 0 |  | 1.949 | 1.577 |
| Rosenbrock | norm | clean | tpe_gp | 20 | 35.25 | 1.563 | 1.275 |
| Rosenbrock | norm | clean | tpe_gradw_gp | 0 |  | 1.201 | 1.375 |
| Rosenbrock | norm | clean | optuna | 30 | 45.83 | 0.2044 | 0.696 |
| Rosenbrock | norm | noisy_y | random | 15 | 49 | 0.7622 | 0.7928 |
| Rosenbrock | norm | noisy_y | tpe | 5 | 15 | 2.002 | 1.501 |
| Rosenbrock | norm | noisy_y | tpe_gradw | 0 |  | 2.057 | 1.6 |
| Rosenbrock | norm | noisy_y | tpe_gp | 20 | 33.25 | 1.609 | 1.312 |
| Rosenbrock | norm | noisy_y | tpe_gradw_gp | 0 |  | 1.266 | 1.405 |
| Rosenbrock | norm | noisy_y | optuna | 25 | 46 | 0.2359 | 0.7533 |
| Rastrigin | raw | clean | random | 5 | 13 | 6.032 | 1.317 |
| Rastrigin | raw | clean | tpe | 30 | 53.17 | 2.37 | 1.342 |
| Rastrigin | raw | clean | tpe_gradw | 5 | 50 | 3.24 | 1.141 |
| Rastrigin | raw | clean | tpe_gp | 5 | 44 | 3.432 | 1.516 |
| Rastrigin | raw | clean | tpe_gradw_gp | 10 | 64 | 2.897 | 1.073 |
| Rastrigin | raw | clean | optuna | 10 | 45 | 2.893 | 1.181 |
| Rastrigin | raw | noisy_y | random | 5 | 13 | 6.04 | 1.406 |
| Rastrigin | raw | noisy_y | tpe | 20 | 41.75 | 2.478 | 1.284 |
| Rastrigin | raw | noisy_y | tpe_gradw | 5 | 71 | 3.271 | 1.061 |
| Rastrigin | raw | noisy_y | tpe_gp | 10 | 47 | 3.44 | 1.449 |
| Rastrigin | raw | noisy_y | tpe_gradw_gp | 15 | 53.67 | 3.085 | 1.085 |
| Rastrigin | raw | noisy_y | optuna | 15 | 41 | 2.564 | 1.084 |
| Rastrigin | norm | clean | random | 5 | 13 | 6.032 | 1.317 |
| Rastrigin | norm | clean | tpe | 30 | 53.17 | 2.37 | 1.342 |
| Rastrigin | norm | clean | tpe_gradw | 35 | 43.14 | 2.875 | 1.264 |
| Rastrigin | norm | clean | tpe_gp | 15 | 41 | 1.913 | 1.159 |
| Rastrigin | norm | clean | tpe_gradw_gp | 0 |  | 3.552 | 1.577 |
| Rastrigin | norm | clean | optuna | 10 | 45 | 2.893 | 1.181 |
| Rastrigin | norm | noisy_y | random | 5 | 13 | 6.04 | 1.406 |
| Rastrigin | norm | noisy_y | tpe | 20 | 41.75 | 2.478 | 1.284 |
| Rastrigin | norm | noisy_y | tpe_gradw | 30 | 43.17 | 2.621 | 1.218 |
| Rastrigin | norm | noisy_y | tpe_gp | 10 | 48 | 2.491 | 1.243 |
| Rastrigin | norm | noisy_y | tpe_gradw_gp | 5 | 46 | 4.133 | 1.713 |
| Rastrigin | norm | noisy_y | optuna | 15 | 41 | 2.564 | 1.084 |
| Ackley | raw | clean | random | 5 | 13 | 2.677 | 0.5621 |
| Ackley | raw | clean | tpe | 65 | 42.23 | 1.021 | 0.3323 |
| Ackley | raw | clean | tpe_gradw | 80 | 48.56 | 0.5245 | 0.1569 |
| Ackley | raw | clean | tpe_gp | 80 | 28.75 | 0.4342 | 0.1292 |
| Ackley | raw | clean | tpe_gradw_gp | 90 | 34.39 | 0.2109 | 0.06836 |
| Ackley | raw | clean | optuna | 15 | 50.67 | 1.119 | 0.1685 |
| Ackley | raw | noisy_y | random | 5 | 13 | 2.677 | 0.5621 |
| Ackley | raw | noisy_y | tpe | 70 | 39.36 | 0.9444 | 0.3276 |
| Ackley | raw | noisy_y | tpe_gradw | 65 | 42.15 | 0.8732 | 0.2381 |
| Ackley | raw | noisy_y | tpe_gp | 85 | 30.88 | 0.2687 | 0.07847 |
| Ackley | raw | noisy_y | tpe_gradw_gp | 85 | 35.53 | 0.5711 | 0.217 |
| Ackley | raw | noisy_y | optuna | 20 | 53.75 | 1.05 | 0.1624 |
| Ackley | norm | clean | random | 5 | 13 | 2.677 | 0.5621 |
| Ackley | norm | clean | tpe | 65 | 42.23 | 1.021 | 0.3323 |
| Ackley | norm | clean | tpe_gradw | 60 | 36.25 | 1.112 | 0.3602 |
| Ackley | norm | clean | tpe_gp | 60 | 35.25 | 1.083 | 0.3626 |
| Ackley | norm | clean | tpe_gradw_gp | 60 | 33.67 | 1.052 | 0.3389 |
| Ackley | norm | clean | optuna | 15 | 50.67 | 1.119 | 0.1685 |
| Ackley | norm | noisy_y | random | 5 | 13 | 2.677 | 0.5621 |
| Ackley | norm | noisy_y | tpe | 70 | 39.36 | 0.9444 | 0.3276 |
| Ackley | norm | noisy_y | tpe_gradw | 75 | 38.4 | 0.9383 | 0.343 |
| Ackley | norm | noisy_y | tpe_gp | 60 | 33.75 | 1.123 | 0.3676 |
| Ackley | norm | noisy_y | tpe_gradw_gp | 60 | 34.75 | 0.9854 | 0.3107 |
| Ackley | norm | noisy_y | optuna | 20 | 53.75 | 1.05 | 0.1624 |

## Полная таблица (все метрики, все ячейки)

| function | scale | data | algorithm | success_rate_% | steps_mean | steps_std | final_dist_y_mean | final_dist_y_std | final_dist_y_median | final_dist_x_mean | final_dist_x_std |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Sphere | raw | clean | random | 0 |  |  | 0.3472 | 0.4396 | 0.2396 | 0.5042 | 0.305 |
| Sphere | raw | clean | tpe | 40 | 47.5 | 15.07 | 0.1116 | 0.3133 | 0.002749 | 0.182 | 0.2801 |
| Sphere | raw | clean | tpe_gradw | 40 | 34.12 | 11.73 | 0.04789 | 0.1072 | 0.002139 | 0.1276 | 0.1778 |
| Sphere | raw | clean | tpe_gp | 95 | 39 | 15.18 | 0.0001577 | 0.0002564 | 6.561e-05 | 0.01006 | 0.007522 |
| Sphere | raw | clean | tpe_gradw_gp | 90 | 33.83 | 12.51 | 0.0003189 | 0.0007331 | 4.842e-05 | 0.01233 | 0.01291 |
| Sphere | raw | clean | optuna | 0 |  |  | 0.02484 | 0.01712 | 0.01806 | 0.1467 | 0.05748 |
| Sphere | raw | noisy_y | random | 0 |  |  | 0.3472 | 0.4396 | 0.2396 | 0.5042 | 0.305 |
| Sphere | raw | noisy_y | tpe | 30 | 45.17 | 17.43 | 0.1093 | 0.2688 | 0.00499 | 0.1998 | 0.2635 |
| Sphere | raw | noisy_y | tpe_gradw | 35 | 43.43 | 23.6 | 0.07767 | 0.1555 | 0.00677 | 0.1715 | 0.2197 |
| Sphere | raw | noisy_y | tpe_gp | 75 | 40.33 | 18.11 | 0.001454 | 0.001291 | 0.0009559 | 0.03475 | 0.0157 |
| Sphere | raw | noisy_y | tpe_gradw_gp | 45 | 33.44 | 15.29 | 0.001926 | 0.001384 | 0.001698 | 0.04039 | 0.01717 |
| Sphere | raw | noisy_y | optuna | 0 |  |  | 0.02717 | 0.01953 | 0.01811 | 0.1542 | 0.05814 |
| Sphere | norm | clean | random | 0 |  |  | 0.3472 | 0.4396 | 0.2396 | 0.5042 | 0.305 |
| Sphere | norm | clean | tpe | 40 | 47.5 | 15.07 | 0.1116 | 0.3133 | 0.002749 | 0.182 | 0.2801 |
| Sphere | norm | clean | tpe_gradw | 40 | 52 | 12.73 | 0.1028 | 0.1863 | 0.002389 | 0.1891 | 0.2589 |
| Sphere | norm | clean | tpe_gp | 40 | 53.12 | 15.89 | 0.02784 | 0.05464 | 0.004212 | 0.1072 | 0.1279 |
| Sphere | norm | clean | tpe_gradw_gp | 45 | 47.44 | 17.1 | 0.07395 | 0.1469 | 0.001689 | 0.1527 | 0.225 |
| Sphere | norm | clean | optuna | 0 |  |  | 0.02484 | 0.01712 | 0.01806 | 0.1467 | 0.05748 |
| Sphere | norm | noisy_y | random | 0 |  |  | 0.3472 | 0.4396 | 0.2396 | 0.5042 | 0.305 |
| Sphere | norm | noisy_y | tpe | 30 | 45.17 | 17.43 | 0.1093 | 0.2688 | 0.00499 | 0.1998 | 0.2635 |
| Sphere | norm | noisy_y | tpe_gradw | 30 | 56.67 | 10.24 | 0.09458 | 0.1663 | 0.008718 | 0.2069 | 0.2275 |
| Sphere | norm | noisy_y | tpe_gp | 35 | 54.29 | 17.22 | 0.0272 | 0.0708 | 0.004054 | 0.1014 | 0.1301 |
| Sphere | norm | noisy_y | tpe_gradw_gp | 15 | 30 | 9.626 | 0.06477 | 0.1186 | 0.008081 | 0.1732 | 0.1865 |
| Sphere | norm | noisy_y | optuna | 0 |  |  | 0.02717 | 0.01953 | 0.01811 | 0.1542 | 0.05814 |
| Rosenbrock | raw | clean | random | 15 | 49 | 9.416 | 0.7622 | 0.821 | 0.4 | 0.7928 | 0.5809 |
| Rosenbrock | raw | clean | tpe | 10 | 47 | 32 | 1.902 | 2.144 | 0.5618 | 1.444 | 0.7191 |
| Rosenbrock | raw | clean | tpe_gradw | 0 |  |  | 1.027 | 1.783 | 0.4297 | 0.9796 | 0.4901 |
| Rosenbrock | raw | clean | tpe_gp | 40 | 25.75 | 8.969 | 0.5431 | 1.532 | 0.1131 | 0.7514 | 0.8241 |
| Rosenbrock | raw | clean | tpe_gradw_gp | 10 | 56 | 8 | 0.221 | 0.1802 | 0.1769 | 0.7029 | 0.4744 |
| Rosenbrock | raw | clean | optuna | 30 | 45.83 | 13.41 | 0.2044 | 0.1617 | 0.1784 | 0.696 | 0.3571 |
| Rosenbrock | raw | noisy_y | random | 15 | 49 | 9.416 | 0.7622 | 0.821 | 0.4 | 0.7928 | 0.5809 |
| Rosenbrock | raw | noisy_y | tpe | 5 | 15 | 0 | 2.002 | 2.099 | 0.78 | 1.501 | 0.6896 |
| Rosenbrock | raw | noisy_y | tpe_gradw | 0 |  |  | 1.021 | 1.776 | 0.4472 | 1.075 | 0.5066 |
| Rosenbrock | raw | noisy_y | tpe_gp | 35 | 22 | 3.295 | 0.5337 | 1.492 | 0.1767 | 0.8095 | 0.717 |
| Rosenbrock | raw | noisy_y | tpe_gradw_gp | 15 | 60.67 | 11.09 | 0.2347 | 0.1804 | 0.1753 | 0.7361 | 0.5157 |
| Rosenbrock | raw | noisy_y | optuna | 25 | 46 | 14.68 | 0.2359 | 0.1598 | 0.2005 | 0.7533 | 0.4417 |
| Rosenbrock | norm | clean | random | 15 | 49 | 9.416 | 0.7622 | 0.821 | 0.4 | 0.7928 | 0.5809 |
| Rosenbrock | norm | clean | tpe | 10 | 47 | 32 | 1.902 | 2.144 | 0.5618 | 1.444 | 0.7191 |
| Rosenbrock | norm | clean | tpe_gradw | 0 |  |  | 1.949 | 1.975 | 1.088 | 1.577 | 0.6776 |
| Rosenbrock | norm | clean | tpe_gp | 20 | 35.25 | 14.91 | 1.563 | 2.095 | 0.3703 | 1.275 | 0.8493 |
| Rosenbrock | norm | clean | tpe_gradw_gp | 0 |  |  | 1.201 | 1.435 | 0.568 | 1.375 | 0.5026 |
| Rosenbrock | norm | clean | optuna | 30 | 45.83 | 13.41 | 0.2044 | 0.1617 | 0.1784 | 0.696 | 0.3571 |
| Rosenbrock | norm | noisy_y | random | 15 | 49 | 9.416 | 0.7622 | 0.821 | 0.4 | 0.7928 | 0.5809 |
| Rosenbrock | norm | noisy_y | tpe | 5 | 15 | 0 | 2.002 | 2.099 | 0.78 | 1.501 | 0.6896 |
| Rosenbrock | norm | noisy_y | tpe_gradw | 0 |  |  | 2.057 | 2.001 | 1.25 | 1.6 | 0.6791 |
| Rosenbrock | norm | noisy_y | tpe_gp | 20 | 33.25 | 12.13 | 1.609 | 2.1 | 0.4582 | 1.312 | 0.8445 |
| Rosenbrock | norm | noisy_y | tpe_gradw_gp | 0 |  |  | 1.266 | 1.44 | 0.6188 | 1.405 | 0.5067 |
| Rosenbrock | norm | noisy_y | optuna | 25 | 46 | 14.68 | 0.2359 | 0.1598 | 0.2005 | 0.7533 | 0.4417 |
| Rastrigin | raw | clean | random | 5 | 13 | 0 | 6.032 | 2.743 | 5.9 | 1.317 | 0.7139 |
| Rastrigin | raw | clean | tpe | 30 | 53.17 | 20.05 | 2.37 | 2.046 | 1.63 | 1.342 | 0.695 |
| Rastrigin | raw | clean | tpe_gradw | 5 | 50 | 0 | 3.24 | 2.143 | 2.726 | 1.141 | 0.4123 |
| Rastrigin | raw | clean | tpe_gp | 5 | 44 | 0 | 3.432 | 3.145 | 2.059 | 1.516 | 0.7439 |
| Rastrigin | raw | clean | tpe_gradw_gp | 10 | 64 | 13 | 2.897 | 1.955 | 2.304 | 1.073 | 0.6498 |
| Rastrigin | raw | clean | optuna | 10 | 45 | 17 | 2.893 | 1.586 | 2.485 | 1.181 | 0.6358 |
| Rastrigin | raw | noisy_y | random | 5 | 13 | 0 | 6.04 | 2.733 | 5.9 | 1.406 | 0.6685 |
| Rastrigin | raw | noisy_y | tpe | 20 | 41.75 | 13.63 | 2.478 | 2.084 | 1.633 | 1.284 | 0.74 |
| Rastrigin | raw | noisy_y | tpe_gradw | 5 | 71 | 0 | 3.271 | 2.263 | 2.611 | 1.061 | 0.4309 |
| Rastrigin | raw | noisy_y | tpe_gp | 10 | 47 | 1 | 3.44 | 2.764 | 2.25 | 1.449 | 0.7931 |
| Rastrigin | raw | noisy_y | tpe_gradw_gp | 15 | 53.67 | 11.03 | 3.085 | 1.79 | 2.928 | 1.085 | 0.644 |
| Rastrigin | raw | noisy_y | optuna | 15 | 41 | 16.31 | 2.564 | 1.55 | 2.226 | 1.084 | 0.5573 |
| Rastrigin | norm | clean | random | 5 | 13 | 0 | 6.032 | 2.743 | 5.9 | 1.317 | 0.7139 |
| Rastrigin | norm | clean | tpe | 30 | 53.17 | 20.05 | 2.37 | 2.046 | 1.63 | 1.342 | 0.695 |
| Rastrigin | norm | clean | tpe_gradw | 35 | 43.14 | 11.52 | 2.875 | 3.651 | 1.039 | 1.264 | 1.108 |
| Rastrigin | norm | clean | tpe_gp | 15 | 41 | 4.082 | 1.913 | 1.82 | 1.178 | 1.159 | 0.6713 |
| Rastrigin | norm | clean | tpe_gradw_gp | 0 |  |  | 3.552 | 2.647 | 2.36 | 1.577 | 0.6753 |
| Rastrigin | norm | clean | optuna | 10 | 45 | 17 | 2.893 | 1.586 | 2.485 | 1.181 | 0.6358 |
| Rastrigin | norm | noisy_y | random | 5 | 13 | 0 | 6.04 | 2.733 | 5.9 | 1.406 | 0.6685 |
| Rastrigin | norm | noisy_y | tpe | 20 | 41.75 | 13.63 | 2.478 | 2.084 | 1.633 | 1.284 | 0.74 |
| Rastrigin | norm | noisy_y | tpe_gradw | 30 | 43.17 | 13.2 | 2.621 | 2.71 | 1.661 | 1.218 | 0.9547 |
| Rastrigin | norm | noisy_y | tpe_gp | 10 | 48 | 3 | 2.491 | 2.08 | 1.577 | 1.243 | 0.7313 |
| Rastrigin | norm | noisy_y | tpe_gradw_gp | 5 | 46 | 0 | 4.133 | 3.172 | 4.508 | 1.713 | 0.8528 |
| Rastrigin | norm | noisy_y | optuna | 15 | 41 | 16.31 | 2.564 | 1.55 | 2.226 | 1.084 | 0.5573 |
| Ackley | raw | clean | random | 5 | 13 | 0 | 2.677 | 1.109 | 3.072 | 0.5621 | 0.4121 |
| Ackley | raw | clean | tpe | 65 | 42.23 | 19.14 | 1.021 | 1.314 | 0.3112 | 0.3323 | 0.453 |
| Ackley | raw | clean | tpe_gradw | 80 | 48.56 | 17.2 | 0.5245 | 0.9794 | 0.06523 | 0.1569 | 0.3475 |
| Ackley | raw | clean | tpe_gp | 80 | 28.75 | 5.54 | 0.4342 | 0.8017 | 0.07689 | 0.1292 | 0.2798 |
| Ackley | raw | clean | tpe_gradw_gp | 90 | 34.39 | 9.013 | 0.2109 | 0.5604 | 0.05084 | 0.06836 | 0.2057 |
| Ackley | raw | clean | optuna | 15 | 50.67 | 13.91 | 1.119 | 0.5383 | 1.014 | 0.1685 | 0.06351 |
| Ackley | raw | noisy_y | random | 5 | 13 | 0 | 2.677 | 1.109 | 3.072 | 0.5621 | 0.4121 |
| Ackley | raw | noisy_y | tpe | 70 | 39.36 | 13.69 | 0.9444 | 1.382 | 0.1913 | 0.3276 | 0.5394 |
| Ackley | raw | noisy_y | tpe_gradw | 65 | 42.15 | 12.04 | 0.8732 | 1.171 | 0.138 | 0.2381 | 0.3942 |
| Ackley | raw | noisy_y | tpe_gp | 85 | 30.88 | 9.164 | 0.2687 | 0.5565 | 0.09146 | 0.07847 | 0.197 |
| Ackley | raw | noisy_y | tpe_gradw_gp | 85 | 35.53 | 9.089 | 0.5711 | 1.566 | 0.06444 | 0.217 | 0.654 |
| Ackley | raw | noisy_y | optuna | 20 | 53.75 | 14.89 | 1.05 | 0.5573 | 0.8891 | 0.1624 | 0.06901 |
| Ackley | norm | clean | random | 5 | 13 | 0 | 2.677 | 1.109 | 3.072 | 0.5621 | 0.4121 |
| Ackley | norm | clean | tpe | 65 | 42.23 | 19.14 | 1.021 | 1.314 | 0.3112 | 0.3323 | 0.453 |
| Ackley | norm | clean | tpe_gradw | 60 | 36.25 | 16.6 | 1.112 | 1.486 | 0.195 | 0.3602 | 0.55 |
| Ackley | norm | clean | tpe_gp | 60 | 35.25 | 13.71 | 1.083 | 1.294 | 0.1017 | 0.3626 | 0.4533 |
| Ackley | norm | clean | tpe_gradw_gp | 60 | 33.67 | 12.42 | 1.052 | 1.527 | 0.04215 | 0.3389 | 0.56 |
| Ackley | norm | clean | optuna | 15 | 50.67 | 13.91 | 1.119 | 0.5383 | 1.014 | 0.1685 | 0.06351 |
| Ackley | norm | noisy_y | random | 5 | 13 | 0 | 2.677 | 1.109 | 3.072 | 0.5621 | 0.4121 |
| Ackley | norm | noisy_y | tpe | 70 | 39.36 | 13.69 | 0.9444 | 1.382 | 0.1913 | 0.3276 | 0.5394 |
| Ackley | norm | noisy_y | tpe_gradw | 75 | 38.4 | 15.09 | 0.9383 | 1.635 | 0.1608 | 0.343 | 0.6418 |
| Ackley | norm | noisy_y | tpe_gp | 60 | 33.75 | 15.61 | 1.123 | 1.371 | 0.1889 | 0.3676 | 0.4947 |
| Ackley | norm | noisy_y | tpe_gradw_gp | 60 | 34.75 | 18.63 | 0.9854 | 1.184 | 0.2661 | 0.3107 | 0.4378 |
| Ackley | norm | noisy_y | optuna | 20 | 53.75 | 14.89 | 1.05 | 0.5573 | 0.8891 | 0.1624 | 0.06901 |

## Выводы (строго по числам прогона)

1. **Базовый `tpe` осмыслен:** средний success 33.8% против random 6.2% и optuna 14.4% (порог success строгий, поэтому смотрите и на final_dist_y).
2. **Нормализация цели для рангового TPE не влияет** (gap=0), но **важна для grad/GP-вариантов** (gap 0.92/1.5). Для базового TPE это no-op.
3. **GP-переранжирование (`tpe_gp`) — самая полезная модификация:** выше всех средний success (42.8%) и бьёт baseline в 68.8% ячеек; особенно сильно на гладких функциях.
4. **Градиентное взвешивание (`tpe_gradw`)** даёт умеренный эффект (лучше baseline в 56.2% ячеек), сильнее помогает по dist_x на многоэкстремальных.
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
