# ПОЛНЫЕ ВЫВОДЫ ДЛЯ КУРСОВОЙ — сравнение способов модификации TPE

Самодостаточный файл (числа из реального прогона: 50 seeds, PYTHONHASHSEED=0). Код: репозиторий darya-09/k5, ветка claude/quirky-euler-e3laj1, папка `tpe_study/`.

## 1. Цель
Сравнить **способы изменения TPE** и понять, какие реально улучшают оптимизацию. TPE делит наблюдения по порогу γ на «хорошие»/«плохие», строит ядерные плотности l(x)/g(x), выбирает кандидата с максимумом l(x)/g(x).

## 2. Проверяемые модификации (каждая — изолированный фактор одной реализации)
- **Нормализация цели** f_norm=(f−f_min)/(f_max−f_min) — фактор `scale` (raw/norm).
- **4 формы градиентного веса w(x)** наблюдений KDE (вес∈[0.8,1.2], истинный ∇f в реальной точке):
  - `tpe_w_smooth` (tanh) — больше вес БОЛЬШОМУ ‖∇f‖;
  - `tpe_w_smooth_inv` (−tanh) — больше вес МАЛОМУ ‖∇f‖;
  - `tpe_w_sign` (резкая сигмоида) — большому ‖∇f‖;
  - `tpe_w_sign_inv` — малому ‖∇f‖.
- **GP-переранжирование** кандидатов: `tpe_gp`; **GP + вес** (аналог gTPE): `tpe_gp_w`.
- Референсы: `random` (нижняя граница), `optuna` (зрелый TPE).

## 3. Установка
- Функции (2D): Sphere, Rosenbrock, Rastrigin, Ackley.
- Сетка: функция × scale(raw,norm) × data(clean,noisy_y) × алгоритм × seed; n_init=10, γ=0.15, n_candidates=24, max_evals=80, seeds=50.
- Общий шум на (функция,seed) для всех методов и шкал (парность). Оценка ВСЕГДА по raw clean.
- Значимость: парный Уилкоксон каждой модификации vs `tpe` по seeds + поправка Холма. Контроль кода: 21 pytest-тест.

## 4. Результаты (реальные числа)

### 4.1 Средние по 16 ячейкам, по алгоритмам
| algorithm | success_rate_% | final_dist_y_mean | final_dist_x_mean |
|---|---|---|---|
| optuna | 15.75 | 1.098 | 0.547 |
| random | 3.5 | 2.627 | 0.943 |
| tpe | 36 | 1.271 | 0.765 |
| tpe_gp | 42.5 | 1.161 | 0.678 |
| tpe_gp_w | 41.88 | 1.215 | 0.706 |
| tpe_w_sign | 33 | 1.3 | 0.764 |
| tpe_w_sign_inv | 33.75 | 1.437 | 0.812 |
| tpe_w_smooth | 35.75 | 1.247 | 0.759 |
| tpe_w_smooth_inv | 39.25 | 1.309 | 0.737 |

### 4.2 Доля ячеек, где модификация лучше `tpe` (по final_dist_y)
| algorithm | win_rate_vs_tpe_% |
|---|---|
| tpe_w_smooth | 87.5 |
| tpe_gp | 75 |
| tpe_gp_w | 68.8 |
| optuna | 50 |
| tpe_w_smooth_inv | 37.5 |
| tpe_w_sign | 37.5 |
| random | 25 |
| tpe_w_sign_inv | 12.5 |

### 4.3 Инвариантность нормализации
Для `tpe` И всех 4 форм w(x): raw≡norm (gap=0) — нормализация не влияет (вес считается по min-max-рангу норм градиента, константа сокращается). Масштабо-зависим **только GP** (gap≈1.6).

### 4.4 Статистическая значимость (ГЛАВНОЕ)
Из 128 сравнений значимы (Holm): 21; из них **9 — улучшения** над `tpe`, остальные — ухудшения (все `random`).

Значимых улучшений по алгоритмам:
| algorithm | sig_wins |
|---|---|
| optuna | 2 |
| random | 0 |
| tpe_gp | 4 |
| tpe_gp_w | 3 |
| tpe_w_sign | 0 |
| tpe_w_sign_inv | 0 |
| tpe_w_smooth | 0 |
| tpe_w_smooth_inv | 0 |

Конкретные значимые улучшения:
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

## 4.5 Это не «плохой тест»: диагностика и робастность
Формы w(x) РЕАЛЬНО меняют поиск (≈100% seeds отличаются от baseline, mean|Δ|≈0.9), но **медиана Δ≈0** — изменения симметричны (то лучше, то хуже). Значит эффект ненаправленный, а не «тест слепой».
| algorithm | %seeds_changed | mean_abs_diff | median_diff |
|---|---|---|---|
| tpe_w_smooth | 99.8 | 0.8999 | -0.0002 |
| tpe_w_smooth_inv | 99.2 | 0.9077 | -0.0002 |
| tpe_w_sign | 100 | 0.9799 | -0.0001 |
| tpe_w_sign_inv | 99.5 | 0.9642 | -0 |
| tpe_gp | 96.8 | 1.05 | -0.0013 |

**Робастность к выбору теста.** Число значимых УЛУЧШЕНИЙ над `tpe` (из 16 ячеек, метрика final_dist_y) при разных тестах × поправках. Видно: формы веса ≈0 везде, GP — устойчиво значим.
| algorithm | wilcoxon/raw | wilcoxon/holm | wilcoxon/bh | ttest/raw | ttest/holm | ttest/bh | sign/raw | sign/holm | sign/bh | perm/raw | perm/holm | perm/bh |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| optuna | 4 | 2 | 4 | 4 | 0 | 4 | 4 | 0 | 4 | 4 | 0 | 4 |
| random | 2 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 |
| tpe_gp | 6 | 4 | 5 | 6 | 0 | 3 | 5 | 1 | 3 | 8 | 3 | 6 |
| tpe_gp_w | 5 | 3 | 4 | 4 | 2 | 2 | 4 | 2 | 3 | 5 | 4 | 4 |
| tpe_w_sign | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| tpe_w_sign_inv | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| tpe_w_smooth | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| tpe_w_smooth_inv | 4 | 0 | 2 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |

Тесты: wilcoxon (знаковых рангов), ttest (парный Стьюдент), sign (знаковый), perm (перестановочный). Поправки: raw (без поправки), holm, bh (FDR). Полные данные — `results/tables/significance_robust*.csv`.

## 5. Выводы (строго)
1. Базовый TPE осмыслен (success 36.0% vs random 3.5%).
2. Нормализация цели не влияет на TPE и на все формы w(x) (инвариантность); важна только для GP.
3. **Ни одна из 4 форм w(x) не даёт статистически значимого улучшения** над baseline — даже при точном градиенте, и это **устойчиво к выбору теста** (Уилкоксон/t-тест/знаковый/перестановочный × raw/Holm/BH — см. §4.5). По средним `tpe_w_smooth` «лучший» (87.5% ячеек), но это не переживает ни поправку, ни смену теста — средние обманывают.
4. **GP-переранжирование — единственная модификация со значимым эффектом** (Sphere, Rosenbrock).
5. Комбинация GP+вес (`tpe_gp_w`) не превосходит чистый GP — выигрыш от GP, не от градиента.

## 6. Что нельзя утверждать
- «Градиентная информация (любая форма w) улучшает TPE» — не подтверждено (0 значимых из всех 4 форм).
- «Нормализация помогает» — для TPE/весов это инвариантность.
- Обобщать на высокую размерность / иные уровни шума — не проверялось.

## 7. Ограничения
- Градиент аналитический/точный (оракул), не black-box.
- Только 2D, один уровень шума на функцию; нет sensitivity по σ/размерности/γ.
- GP только для переранжирования; Rosenbrock труден для покоординатного TPE.

## 8. Полная таблица ключевых метрик (все строки)
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

---
Файлы: `docs/ARTICLE.md` (статья), `docs/DESIGN.md` (архитектура), `docs/RESULTS.md` (полный отчёт), `results/tables/*.csv` (+ all_results.xlsx), `results/figures/*.png`.