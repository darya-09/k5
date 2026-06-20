# РЕЗУЛЬТАТЫ ПО ВСЕМ ЭКСПЕРИМЕНТАМ (факты, без интерпретаций)

Источник: прогон `run.py`, конфиг: seeds=50, n_init=10, gamma=0.2, n_candidates=24, max_evals=100, PYTHONHASHSEED=0. Функции: Sphere, Rosenbrock, Rastrigin, Ackley. Шкалы: ['raw', 'norm']. Данные: ['clean', 'noisy_y']. Оценка качества — по raw clean функции.

Метрики: success_rate_% (доля из 50 запусков, достигших порога по dist_y); final_dist_y = |f(x_best) − f*|; final_dist_x = ||x_best − x*||. Колонка `uses_gradient`: использует ли метод точный аналитический градиент.

## 1. Средние по 16 ячейкам (функция×scale×data), по алгоритмам
| algorithm | success_rate_% | final_dist_y_mean | final_dist_x_mean | family | uses_gradient |
|---|---|---|---|---|---|
| tpe_refine | 63.75 | 0.626 | 0.543 | white-box(∇f-descent) | True |
| tpe_gp_refine | 62.12 | 0.562 | 0.472 | white-box(∇f-descent) | True |
| tpe_gp | 40.88 | 1.286 | 0.718 | black-box | False |
| tpe_gp_w | 34.5 | 1.102 | 0.689 | white-box(∇f) | True |
| tpe_w_sign_inv | 29.5 | 1.475 | 0.834 | white-box(∇f) | True |
| tpe_w_smooth_inv | 29.25 | 1.545 | 0.864 | white-box(∇f) | True |
| tpe | 25 | 1.684 | 0.905 | black-box | False |
| tpe_w_sign | 22 | 1.796 | 0.906 | white-box(∇f) | True |
| optuna | 21.25 | 0.9 | 0.479 | black-box | False |
| tpe_w_smooth | 21.25 | 1.62 | 0.859 | white-box(∇f) | True |
| random | 4 | 2.345 | 0.875 | black-box | False |

## 2. Доля ячеек, где метод лучше baseline `tpe` по final_dist_y (из 16)
| algorithm | cells_better_than_tpe_% |
|---|---|
| optuna | 100 |
| tpe_gp_refine | 100 |
| tpe_refine | 100 |
| tpe_gp_w | 100 |
| tpe_w_smooth_inv | 87.5 |
| tpe_w_sign_inv | 87.5 |
| tpe_gp | 75 |
| tpe_w_smooth | 62.5 |
| random | 25 |
| tpe_w_sign | 25 |

## 3. Статистическая значимость vs `tpe` (парный Уилкоксон + поправка Холма, α=0.05)
Всего сравнений: 160. Значимых: 48 (улучшений: 42, ухудшений: 6).
| algorithm | significant_improvements(of 16) | uses_gradient |
|---|---|---|
| optuna | 6 | False |
| random | 0 | False |
| tpe_gp | 6 | False |
| tpe_gp_refine | 12 | True |
| tpe_gp_w | 6 | True |
| tpe_refine | 12 | True |
| tpe_w_sign | 0 | True |
| tpe_w_sign_inv | 0 | True |
| tpe_w_smooth | 0 | True |
| tpe_w_smooth_inv | 0 | True |

### 3a. Ячейки со значимым УЛУЧШЕНИЕМ над `tpe`
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

### 3b. Ячейки со значимым УХУДШЕНИЕМ относительно `tpe`
| function | scale | data | algorithm | median_delta | p_holm |
|---|---|---|---|---|---|
| Rastrigin | norm | clean | random | 3.182 | 0.004012 |
| Rastrigin | raw | clean | random | 3.182 | 0.004012 |
| Sphere | norm | clean | random | 0.2213 | 0.001962 |
| Sphere | norm | noisy_y | random | 0.2189 | 0.0006512 |
| Sphere | raw | clean | random | 0.2213 | 0.001962 |
| Sphere | raw | noisy_y | random | 0.2189 | 0.0006512 |

## 4. Инвариантность к нормализации (сколько из 8 ячеек raw≡norm точно)
| algorithm | cells_raw==norm(of 8) |
|---|---|
| optuna | 8 |
| random | 8 |
| tpe | 8 |
| tpe_gp | 0 |
| tpe_gp_refine | 0 |
| tpe_gp_w | 0 |
| tpe_refine | 8 |
| tpe_w_sign | 8 |
| tpe_w_sign_inv | 8 |
| tpe_w_smooth | 8 |
| tpe_w_smooth_inv | 8 |

## 5. Робастность: число значимых улучшений vs `tpe` (метрика final_dist_y) при разных тестах×поправках
Тесты: wilcoxon, ttest (парный), sign, perm (перестановочный). Поправки: raw/holm/bh(FDR).
| algorithm | wilcoxon/raw | wilcoxon/holm | wilcoxon/bh | ttest/raw | ttest/holm | ttest/bh | sign/raw | sign/holm | sign/bh | perm/raw | perm/holm | perm/bh |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| optuna | 10 | 6 | 8 | 10 | 8 | 10 | 6 | 2 | 6 | 10 | 10 | 10 |
| random | 4 | 0 | 4 | 4 | 0 | 4 | 0 | 0 | 0 | 4 | 0 | 4 |
| tpe_gp | 8 | 6 | 8 | 8 | 4 | 8 | 7 | 5 | 7 | 8 | 6 | 8 |
| tpe_gp_refine | 16 | 12 | 16 | 16 | 8 | 16 | 16 | 9 | 16 | 16 | 12 | 16 |
| tpe_gp_w | 7 | 6 | 7 | 8 | 4 | 7 | 4 | 3 | 4 | 8 | 6 | 7 |
| tpe_refine | 16 | 12 | 16 | 16 | 8 | 16 | 16 | 8 | 12 | 16 | 12 | 16 |
| tpe_w_sign | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| tpe_w_sign_inv | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| tpe_w_smooth | 2 | 0 | 2 | 2 | 0 | 2 | 0 | 0 | 0 | 2 | 0 | 2 |
| tpe_w_smooth_inv | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## 6. Полная таблица ключевых метрик (все 176 строк)
| function | scale | data | algorithm | success_rate_% | steps_mean | final_dist_y_mean | final_dist_y_std | final_dist_x_mean | final_dist_x_std |
|---|---|---|---|---|---|---|---|---|---|
| Ackley | norm | clean | optuna | 40 | 69.5 | 0.655 | 0.4328 | 0.1112 | 0.05658 |
| Ackley | norm | clean | random | 2 | 13 | 2.843 | 1.059 | 0.6475 | 0.3763 |
| Ackley | norm | clean | tpe | 32 | 40.44 | 2.043 | 1.582 | 0.7313 | 0.6348 |
| Ackley | norm | clean | tpe_gp | 52 | 40.92 | 1.278 | 1.393 | 0.4349 | 0.4987 |
| Ackley | norm | clean | tpe_gp_refine | 68 | 28.88 | 0.889 | 1.318 | 0.3163 | 0.4854 |
| Ackley | norm | clean | tpe_gp_w | 48 | 54.75 | 1.388 | 1.345 | 0.4701 | 0.5038 |
| Ackley | norm | clean | tpe_refine | 76 | 31.05 | 0.7898 | 1.475 | 0.2999 | 0.5685 |
| Ackley | norm | clean | tpe_w_sign | 44 | 37.45 | 1.603 | 1.405 | 0.5353 | 0.5215 |
| Ackley | norm | clean | tpe_w_sign_inv | 40 | 50.25 | 1.674 | 1.568 | 0.5648 | 0.6111 |
| Ackley | norm | clean | tpe_w_smooth | 42 | 36.29 | 1.429 | 1.328 | 0.4699 | 0.5021 |
| Ackley | norm | clean | tpe_w_smooth_inv | 30 | 39.07 | 2.073 | 1.437 | 0.7205 | 0.5477 |
| Ackley | norm | noisy_y | optuna | 36 | 62.33 | 0.7508 | 0.4398 | 0.1243 | 0.05549 |
| Ackley | norm | noisy_y | random | 2 | 13 | 2.844 | 1.06 | 0.657 | 0.3866 |
| Ackley | norm | noisy_y | tpe | 44 | 40.23 | 1.812 | 1.651 | 0.6559 | 0.6475 |
| Ackley | norm | noisy_y | tpe_gp | 56 | 40.68 | 1.27 | 1.533 | 0.431 | 0.5724 |
| Ackley | norm | noisy_y | tpe_gp_refine | 66 | 33 | 0.9148 | 1.322 | 0.3317 | 0.4906 |
| Ackley | norm | noisy_y | tpe_gp_w | 36 | 54.61 | 1.716 | 1.498 | 0.5701 | 0.5759 |
| Ackley | norm | noisy_y | tpe_refine | 66 | 28.3 | 1.065 | 1.552 | 0.4021 | 0.5994 |
| Ackley | norm | noisy_y | tpe_w_sign | 50 | 41.16 | 1.476 | 1.486 | 0.4761 | 0.5665 |
| Ackley | norm | noisy_y | tpe_w_sign_inv | 40 | 48.85 | 1.533 | 1.499 | 0.5214 | 0.5982 |
| Ackley | norm | noisy_y | tpe_w_smooth | 46 | 35.57 | 1.456 | 1.498 | 0.4717 | 0.5626 |
| Ackley | norm | noisy_y | tpe_w_smooth_inv | 44 | 50.05 | 1.62 | 1.623 | 0.5333 | 0.6326 |
| Ackley | raw | clean | optuna | 40 | 69.5 | 0.655 | 0.4328 | 0.1112 | 0.05658 |
| Ackley | raw | clean | random | 2 | 13 | 2.843 | 1.059 | 0.6475 | 0.3763 |
| Ackley | raw | clean | tpe | 32 | 40.44 | 2.043 | 1.582 | 0.7313 | 0.6348 |
| Ackley | raw | clean | tpe_gp | 86 | 39.23 | 0.4545 | 0.9426 | 0.159 | 0.3465 |
| Ackley | raw | clean | tpe_gp_refine | 84 | 18.95 | 0.4359 | 0.999 | 0.1614 | 0.371 |
| Ackley | raw | clean | tpe_gp_w | 90 | 44.33 | 0.3911 | 1.135 | 0.1296 | 0.4672 |
| Ackley | raw | clean | tpe_refine | 76 | 31.05 | 0.7898 | 1.475 | 0.2999 | 0.5685 |
| Ackley | raw | clean | tpe_w_sign | 44 | 37.45 | 1.603 | 1.405 | 0.5353 | 0.5215 |
| Ackley | raw | clean | tpe_w_sign_inv | 40 | 50.25 | 1.674 | 1.568 | 0.5648 | 0.6111 |
| Ackley | raw | clean | tpe_w_smooth | 42 | 36.29 | 1.429 | 1.328 | 0.4699 | 0.5021 |
| Ackley | raw | clean | tpe_w_smooth_inv | 30 | 39.07 | 2.073 | 1.437 | 0.7205 | 0.5477 |
| Ackley | raw | noisy_y | optuna | 36 | 62.33 | 0.7508 | 0.4398 | 0.1243 | 0.05549 |
| Ackley | raw | noisy_y | random | 2 | 13 | 2.844 | 1.06 | 0.657 | 0.3866 |
| Ackley | raw | noisy_y | tpe | 44 | 40.23 | 1.812 | 1.651 | 0.6559 | 0.6475 |
| Ackley | raw | noisy_y | tpe_gp | 88 | 39.52 | 0.4187 | 0.857 | 0.1347 | 0.3121 |
| Ackley | raw | noisy_y | tpe_gp_refine | 90 | 22.18 | 0.2954 | 0.8152 | 0.08897 | 0.254 |
| Ackley | raw | noisy_y | tpe_gp_w | 84 | 42.69 | 0.4513 | 0.8581 | 0.1448 | 0.3068 |
| Ackley | raw | noisy_y | tpe_refine | 66 | 28.3 | 1.065 | 1.552 | 0.4021 | 0.5994 |
| Ackley | raw | noisy_y | tpe_w_sign | 50 | 41.16 | 1.476 | 1.486 | 0.4761 | 0.5665 |
| Ackley | raw | noisy_y | tpe_w_sign_inv | 40 | 48.85 | 1.533 | 1.499 | 0.5214 | 0.5982 |
| Ackley | raw | noisy_y | tpe_w_smooth | 46 | 35.57 | 1.456 | 1.498 | 0.4717 | 0.5626 |
| Ackley | raw | noisy_y | tpe_w_smooth_inv | 44 | 50.05 | 1.62 | 1.623 | 0.5333 | 0.6326 |
| Rastrigin | norm | clean | optuna | 10 | 70.6 | 2.58 | 1.439 | 1.026 | 0.6194 |
| Rastrigin | norm | clean | random | 2 | 13 | 5.46 | 2.572 | 1.474 | 0.7244 |
| Rastrigin | norm | clean | tpe | 28 | 44.71 | 2.775 | 3.333 | 1.328 | 0.9755 |
| Rastrigin | norm | clean | tpe_gp | 24 | 46 | 2.436 | 1.981 | 1.283 | 0.7334 |
| Rastrigin | norm | clean | tpe_gp_refine | 64 | 31.31 | 1.043 | 1.034 | 0.7949 | 0.5959 |
| Rastrigin | norm | clean | tpe_gp_w | 18 | 37 | 2.674 | 2.156 | 1.341 | 0.7151 |
| Rastrigin | norm | clean | tpe_refine | 76 | 29.66 | 1.136 | 1.314 | 0.8131 | 0.6717 |
| Rastrigin | norm | clean | tpe_w_sign | 8 | 49.5 | 3.915 | 3.462 | 1.559 | 0.83 |
| Rastrigin | norm | clean | tpe_w_sign_inv | 26 | 43.69 | 2.553 | 2.781 | 1.307 | 0.8647 |
| Rastrigin | norm | clean | tpe_w_smooth | 8 | 38.5 | 3.43 | 3.367 | 1.445 | 0.818 |
| Rastrigin | norm | clean | tpe_w_smooth_inv | 36 | 51.94 | 2.721 | 3.29 | 1.32 | 0.9556 |
| Rastrigin | norm | noisy_y | optuna | 12 | 60 | 2.523 | 1.555 | 1.003 | 0.5555 |
| Rastrigin | norm | noisy_y | random | 2 | 13 | 5.465 | 2.57 | 1.493 | 0.7171 |
| Rastrigin | norm | noisy_y | tpe | 16 | 28.5 | 3.453 | 3.628 | 1.46 | 0.9404 |
| Rastrigin | norm | noisy_y | tpe_gp | 18 | 54.89 | 3.168 | 2.645 | 1.428 | 0.7756 |
| Rastrigin | norm | noisy_y | tpe_gp_refine | 48 | 38.46 | 1.248 | 1.116 | 0.911 | 0.5825 |
| Rastrigin | norm | noisy_y | tpe_gp_w | 12 | 36.67 | 2.951 | 2.147 | 1.389 | 0.701 |
| Rastrigin | norm | noisy_y | tpe_refine | 52 | 28.12 | 1.189 | 1.196 | 0.8913 | 0.5933 |
| Rastrigin | norm | noisy_y | tpe_w_sign | 4 | 31.5 | 3.769 | 3.067 | 1.527 | 0.7789 |
| Rastrigin | norm | noisy_y | tpe_w_sign_inv | 20 | 35.9 | 2.701 | 2.645 | 1.312 | 0.8438 |
| Rastrigin | norm | noisy_y | tpe_w_smooth | 8 | 49 | 3.435 | 3.284 | 1.426 | 0.8133 |
| Rastrigin | norm | noisy_y | tpe_w_smooth_inv | 24 | 41.75 | 2.914 | 3.043 | 1.414 | 0.861 |
| Rastrigin | raw | clean | optuna | 10 | 70.6 | 2.58 | 1.439 | 1.026 | 0.6194 |
| Rastrigin | raw | clean | random | 2 | 13 | 5.46 | 2.572 | 1.474 | 0.7244 |
| Rastrigin | raw | clean | tpe | 28 | 44.71 | 2.775 | 3.333 | 1.328 | 0.9755 |
| Rastrigin | raw | clean | tpe_gp | 8 | 59.5 | 3.599 | 3.157 | 1.456 | 0.8172 |
| Rastrigin | raw | clean | tpe_gp_refine | 58 | 38.86 | 1.226 | 1.168 | 0.8937 | 0.5878 |
| Rastrigin | raw | clean | tpe_gp_w | 20 | 80.5 | 2.127 | 1.347 | 1.096 | 0.6049 |
| Rastrigin | raw | clean | tpe_refine | 76 | 29.66 | 1.136 | 1.314 | 0.8131 | 0.6717 |
| Rastrigin | raw | clean | tpe_w_sign | 8 | 49.5 | 3.915 | 3.462 | 1.559 | 0.83 |
| Rastrigin | raw | clean | tpe_w_sign_inv | 26 | 43.69 | 2.553 | 2.781 | 1.307 | 0.8647 |
| Rastrigin | raw | clean | tpe_w_smooth | 8 | 38.5 | 3.43 | 3.367 | 1.445 | 0.818 |
| Rastrigin | raw | clean | tpe_w_smooth_inv | 36 | 51.94 | 2.721 | 3.29 | 1.32 | 0.9556 |
| Rastrigin | raw | noisy_y | optuna | 12 | 60 | 2.523 | 1.555 | 1.003 | 0.5555 |
| Rastrigin | raw | noisy_y | random | 2 | 13 | 5.465 | 2.57 | 1.493 | 0.7171 |
| Rastrigin | raw | noisy_y | tpe | 16 | 28.5 | 3.453 | 3.628 | 1.46 | 0.9404 |
| Rastrigin | raw | noisy_y | tpe_gp | 12 | 38.5 | 3.456 | 2.462 | 1.491 | 0.7547 |
| Rastrigin | raw | noisy_y | tpe_gp_refine | 44 | 37.55 | 1.521 | 1.749 | 0.8836 | 0.7493 |
| Rastrigin | raw | noisy_y | tpe_gp_w | 18 | 72.89 | 2.2 | 1.628 | 1.092 | 0.6221 |
| Rastrigin | raw | noisy_y | tpe_refine | 52 | 28.12 | 1.189 | 1.196 | 0.8913 | 0.5933 |
| Rastrigin | raw | noisy_y | tpe_w_sign | 4 | 31.5 | 3.769 | 3.067 | 1.527 | 0.7789 |
| Rastrigin | raw | noisy_y | tpe_w_sign_inv | 20 | 35.9 | 2.701 | 2.645 | 1.312 | 0.8438 |
| Rastrigin | raw | noisy_y | tpe_w_smooth | 8 | 49 | 3.435 | 3.284 | 1.426 | 0.8133 |
| Rastrigin | raw | noisy_y | tpe_w_smooth_inv | 24 | 41.75 | 2.914 | 3.043 | 1.414 | 0.861 |
| Rosenbrock | norm | clean | optuna | 32 | 55.25 | 0.3045 | 0.848 | 0.6479 | 0.4841 |
| Rosenbrock | norm | clean | random | 12 | 50.5 | 0.6699 | 0.6726 | 0.8094 | 0.5436 |
| Rosenbrock | norm | clean | tpe | 8 | 20 | 1.533 | 1.804 | 1.274 | 0.6918 |
| Rosenbrock | norm | clean | tpe_gp | 12 | 28.5 | 1.78 | 1.951 | 1.307 | 0.709 |
| Rosenbrock | norm | clean | tpe_gp_refine | 26 | 28.46 | 0.5048 | 1.066 | 0.8659 | 0.6653 |
| Rosenbrock | norm | clean | tpe_gp_w | 10 | 25.2 | 1.47 | 1.59 | 1.298 | 0.635 |
| Rosenbrock | norm | clean | tpe_refine | 24 | 38.5 | 0.3954 | 0.5708 | 0.9035 | 0.6115 |
| Rosenbrock | norm | clean | tpe_w_sign | 8 | 26.5 | 1.589 | 1.794 | 1.322 | 0.7205 |
| Rosenbrock | norm | clean | tpe_w_sign_inv | 14 | 32.29 | 1.531 | 1.87 | 1.292 | 0.7295 |
| Rosenbrock | norm | clean | tpe_w_smooth | 14 | 25 | 1.379 | 1.742 | 1.236 | 0.7338 |
| Rosenbrock | norm | clean | tpe_w_smooth_inv | 18 | 36.22 | 1.376 | 1.622 | 1.248 | 0.68 |
| Rosenbrock | norm | noisy_y | optuna | 26 | 51.77 | 0.3558 | 0.8502 | 0.6932 | 0.4851 |
| Rosenbrock | norm | noisy_y | random | 12 | 50.5 | 0.6715 | 0.6731 | 0.8068 | 0.5421 |
| Rosenbrock | norm | noisy_y | tpe | 10 | 21.6 | 1.593 | 1.825 | 1.323 | 0.7066 |
| Rosenbrock | norm | noisy_y | tpe_gp | 12 | 32.5 | 1.865 | 1.931 | 1.33 | 0.7003 |
| Rosenbrock | norm | noisy_y | tpe_gp_refine | 26 | 30.23 | 0.4575 | 0.9641 | 0.8704 | 0.6204 |
| Rosenbrock | norm | noisy_y | tpe_gp_w | 10 | 23.2 | 1.455 | 1.528 | 1.3 | 0.6123 |
| Rosenbrock | norm | noisy_y | tpe_refine | 18 | 46.11 | 0.4284 | 0.5503 | 1.017 | 0.6003 |
| Rosenbrock | norm | noisy_y | tpe_w_sign | 12 | 28.33 | 1.651 | 1.833 | 1.305 | 0.7307 |
| Rosenbrock | norm | noisy_y | tpe_w_sign_inv | 12 | 24.67 | 1.62 | 1.896 | 1.301 | 0.7473 |
| Rosenbrock | norm | noisy_y | tpe_w_smooth | 16 | 26.25 | 1.483 | 1.761 | 1.253 | 0.7202 |
| Rosenbrock | norm | noisy_y | tpe_w_smooth_inv | 12 | 21.17 | 1.461 | 1.648 | 1.285 | 0.6764 |
| Rosenbrock | raw | clean | optuna | 32 | 55.25 | 0.3045 | 0.848 | 0.6479 | 0.4841 |
| Rosenbrock | raw | clean | random | 12 | 50.5 | 0.6699 | 0.6726 | 0.8094 | 0.5436 |
| Rosenbrock | raw | clean | tpe | 8 | 20 | 1.533 | 1.804 | 1.274 | 0.6918 |
| Rosenbrock | raw | clean | tpe_gp | 34 | 28.88 | 0.4135 | 1.057 | 0.7635 | 0.6618 |
| Rosenbrock | raw | clean | tpe_gp_refine | 14 | 32 | 0.2261 | 0.1639 | 0.7095 | 0.4471 |
| Rosenbrock | raw | clean | tpe_gp_w | 8 | 42 | 0.2954 | 0.2597 | 0.8261 | 0.4406 |
| Rosenbrock | raw | clean | tpe_refine | 24 | 38.5 | 0.3954 | 0.5708 | 0.9035 | 0.6115 |
| Rosenbrock | raw | clean | tpe_w_sign | 8 | 26.5 | 1.589 | 1.794 | 1.322 | 0.7205 |
| Rosenbrock | raw | clean | tpe_w_sign_inv | 14 | 32.29 | 1.531 | 1.87 | 1.292 | 0.7295 |
| Rosenbrock | raw | clean | tpe_w_smooth | 14 | 25 | 1.379 | 1.742 | 1.236 | 0.7338 |
| Rosenbrock | raw | clean | tpe_w_smooth_inv | 18 | 36.22 | 1.376 | 1.622 | 1.248 | 0.68 |
| Rosenbrock | raw | noisy_y | optuna | 26 | 51.77 | 0.3558 | 0.8502 | 0.6932 | 0.4851 |
| Rosenbrock | raw | noisy_y | random | 12 | 50.5 | 0.6715 | 0.6731 | 0.8068 | 0.5421 |
| Rosenbrock | raw | noisy_y | tpe | 10 | 21.6 | 1.593 | 1.825 | 1.323 | 0.7066 |
| Rosenbrock | raw | noisy_y | tpe_gp | 32 | 28.44 | 0.2657 | 0.3022 | 0.8299 | 0.5308 |
| Rosenbrock | raw | noisy_y | tpe_gp_refine | 12 | 20.67 | 0.23 | 0.1687 | 0.6716 | 0.4387 |
| Rosenbrock | raw | noisy_y | tpe_gp_w | 8 | 60 | 0.3183 | 0.2396 | 0.8663 | 0.4368 |
| Rosenbrock | raw | noisy_y | tpe_refine | 18 | 46.11 | 0.4284 | 0.5503 | 1.017 | 0.6003 |
| Rosenbrock | raw | noisy_y | tpe_w_sign | 12 | 28.33 | 1.651 | 1.833 | 1.305 | 0.7307 |
| Rosenbrock | raw | noisy_y | tpe_w_sign_inv | 12 | 24.67 | 1.62 | 1.896 | 1.301 | 0.7473 |
| Rosenbrock | raw | noisy_y | tpe_w_smooth | 16 | 26.25 | 1.483 | 1.761 | 1.253 | 0.7202 |
| Rosenbrock | raw | noisy_y | tpe_w_smooth_inv | 12 | 21.17 | 1.461 | 1.648 | 1.285 | 0.6764 |
| Sphere | norm | clean | optuna | 6 | 64 | 0.01705 | 0.01828 | 0.1141 | 0.06343 |
| Sphere | norm | clean | random | 0 |  | 0.4018 | 0.4152 | 0.5556 | 0.3051 |
| Sphere | norm | clean | tpe | 36 | 59.28 | 0.1392 | 0.2829 | 0.2364 | 0.2887 |
| Sphere | norm | clean | tpe_gp | 46 | 54.48 | 0.08402 | 0.1609 | 0.1776 | 0.2291 |
| Sphere | norm | clean | tpe_gp_refine | 100 | 18.92 | 4.024e-07 | 6.195e-07 | 0.0004692 | 0.0004269 |
| Sphere | norm | clean | tpe_gp_w | 28 | 62.43 | 0.1011 | 0.1779 | 0.211 | 0.2379 |
| Sphere | norm | clean | tpe_refine | 100 | 19.92 | 6.981e-07 | 1.634e-06 | 0.0005607 | 0.0006195 |
| Sphere | norm | clean | tpe_w_sign | 28 | 61.79 | 0.1648 | 0.3993 | 0.2486 | 0.3209 |
| Sphere | norm | clean | tpe_w_sign_inv | 48 | 59.71 | 0.0918 | 0.1901 | 0.1792 | 0.2443 |
| Sphere | norm | clean | tpe_w_smooth | 20 | 48.8 | 0.1765 | 0.3299 | 0.2854 | 0.3084 |
| Sphere | norm | clean | tpe_w_smooth_inv | 46 | 56.52 | 0.09304 | 0.1731 | 0.19 | 0.2386 |
| Sphere | norm | noisy_y | optuna | 8 | 66 | 0.01714 | 0.01815 | 0.1154 | 0.06175 |
| Sphere | norm | noisy_y | random | 0 |  | 0.4018 | 0.4152 | 0.5556 | 0.3051 |
| Sphere | norm | noisy_y | tpe | 26 | 64.92 | 0.126 | 0.2748 | 0.229 | 0.2712 |
| Sphere | norm | noisy_y | tpe_gp | 32 | 62.75 | 0.08345 | 0.1687 | 0.1855 | 0.2214 |
| Sphere | norm | noisy_y | tpe_gp_refine | 96 | 24.12 | 0.00107 | 0.001232 | 0.02769 | 0.01741 |
| Sphere | norm | noisy_y | tpe_gp_w | 24 | 63.08 | 0.08862 | 0.1561 | 0.2087 | 0.2123 |
| Sphere | norm | noisy_y | tpe_refine | 98 | 24.92 | 0.0006047 | 0.0008322 | 0.01943 | 0.01507 |
| Sphere | norm | noisy_y | tpe_w_sign | 22 | 67.45 | 0.1999 | 0.4695 | 0.2726 | 0.3543 |
| Sphere | norm | noisy_y | tpe_w_sign_inv | 36 | 68.33 | 0.09839 | 0.2052 | 0.1966 | 0.2444 |
| Sphere | norm | noisy_y | tpe_w_smooth | 16 | 61.88 | 0.1708 | 0.3343 | 0.2826 | 0.3016 |
| Sphere | norm | noisy_y | tpe_w_smooth_inv | 24 | 60.58 | 0.09846 | 0.2019 | 0.2027 | 0.2396 |
| Sphere | raw | clean | optuna | 6 | 64 | 0.01705 | 0.01828 | 0.1141 | 0.06343 |
| Sphere | raw | clean | random | 0 |  | 0.4018 | 0.4152 | 0.5556 | 0.3051 |
| Sphere | raw | clean | tpe | 36 | 59.28 | 0.1392 | 0.2829 | 0.2364 | 0.2887 |
| Sphere | raw | clean | tpe_gp | 84 | 45.9 | 0.003201 | 0.01286 | 0.02371 | 0.05137 |
| Sphere | raw | clean | tpe_gp_refine | 100 | 15.06 | 1.542e-06 | 4.428e-06 | 0.0007865 | 0.0009609 |
| Sphere | raw | clean | tpe_gp_w | 82 | 45.59 | 0.002107 | 0.008753 | 0.02206 | 0.04025 |
| Sphere | raw | clean | tpe_refine | 100 | 19.92 | 6.981e-07 | 1.634e-06 | 0.0005607 | 0.0006195 |
| Sphere | raw | clean | tpe_w_sign | 28 | 61.79 | 0.1648 | 0.3993 | 0.2486 | 0.3209 |
| Sphere | raw | clean | tpe_w_sign_inv | 48 | 59.71 | 0.0918 | 0.1901 | 0.1792 | 0.2443 |
| Sphere | raw | clean | tpe_w_smooth | 20 | 48.8 | 0.1765 | 0.3299 | 0.2854 | 0.3084 |
| Sphere | raw | clean | tpe_w_smooth_inv | 46 | 56.52 | 0.09304 | 0.1731 | 0.19 | 0.2386 |
| Sphere | raw | noisy_y | optuna | 8 | 66 | 0.01714 | 0.01815 | 0.1154 | 0.06175 |
| Sphere | raw | noisy_y | random | 0 |  | 0.4018 | 0.4152 | 0.5556 | 0.3051 |
| Sphere | raw | noisy_y | tpe | 26 | 64.92 | 0.126 | 0.2748 | 0.229 | 0.2712 |
| Sphere | raw | noisy_y | tpe_gp | 58 | 46.55 | 0.004551 | 0.007789 | 0.05501 | 0.03906 |
| Sphere | raw | noisy_y | tpe_gp_refine | 98 | 18.86 | 0.0007766 | 0.001039 | 0.02245 | 0.01651 |
| Sphere | raw | noisy_y | tpe_gp_w | 56 | 45.86 | 0.005578 | 0.01099 | 0.05767 | 0.04745 |
| Sphere | raw | noisy_y | tpe_refine | 98 | 24.92 | 0.0006047 | 0.0008322 | 0.01943 | 0.01507 |
| Sphere | raw | noisy_y | tpe_w_sign | 22 | 67.45 | 0.1999 | 0.4695 | 0.2726 | 0.3543 |
| Sphere | raw | noisy_y | tpe_w_sign_inv | 36 | 68.33 | 0.09839 | 0.2052 | 0.1966 | 0.2444 |
| Sphere | raw | noisy_y | tpe_w_smooth | 16 | 61.88 | 0.1708 | 0.3343 | 0.2826 | 0.3016 |
| Sphere | raw | noisy_y | tpe_w_smooth_inv | 24 | 60.58 | 0.09846 | 0.2019 | 0.2027 | 0.2396 |

Дополнительно в `results/tables/`: per_seed_final.csv, iteration_history.csv, raw_vs_norm_comparison.csv, significance_tests.csv, significance_robust.csv, all_results.xlsx.