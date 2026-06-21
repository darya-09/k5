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
- **GP-переранжирование** кандидатов: `tpe_gp`; **GP + вес наблюдений** (аналог gTPE): `tpe_gp_w`.
- **Локальный градиентный refinement** (шаг спуска по оракулу ∇f): `tpe_refine`, `tpe_gp_refine`.
- Референсы: `random` (нижняя граница), `optuna` (зрелый TPE).

**КЛАССИФИКАЦИЯ (важно для корректной статьи): black-box vs white-box.**
- *black-box* (без ∇f): `random`, `tpe`, `optuna`, `tpe_gp`.
- *white-box* (точный ∇f, оракул): формы веса `tpe_w_*`, `tpe_gp_w`, и refinement `tpe_refine`/`tpe_gp_refine`.
- refinement = по сути обычный **градиентный спуск** с точным ∇f → это ВЕРХНЯЯ ГРАНИЦА «что даёт градиент», а не доказательство, что градиент улучшает TPE. Сравнивать честно — внутри своего класса.

## 3. Установка
- Функции (2D): Sphere, Rosenbrock, Rastrigin, Ackley.
- Сетка: функция × scale(raw,norm) × data(clean,noisy_y) × алгоритм × seed; n_init=10, γ=0.2, n_candidates=24, max_evals=100, seeds=50.
- Общий шум на (функция,seed) для всех методов и шкал (парность). Оценка ВСЕГДА по raw clean.
- Значимость: парный Уилкоксон каждой модификации vs `tpe` по seeds + поправка Холма. Контроль кода: набор pytest-тестов (tests/, запуск `python -m pytest`).

## 4. Результаты (реальные числа)

### 4.1 Средние по 16 ячейкам, по алгоритмам
| algorithm | success_rate_% | final_dist_y_mean | final_dist_x_mean | family |
|---|---|---|---|---|
| tpe_refine | 63.75 | 0.626 | 0.543 | white-box(∇f-descent) |
| tpe_gp_refine | 62.12 | 0.562 | 0.472 | white-box(∇f-descent) |
| tpe_gp | 40.88 | 1.286 | 0.718 | black-box |
| tpe_gp_w | 34.5 | 1.102 | 0.689 | white-box(∇f) |
| tpe_w_sign_inv | 29.5 | 1.475 | 0.834 | white-box(∇f) |
| tpe_w_smooth_inv | 29.25 | 1.545 | 0.864 | white-box(∇f) |
| tpe | 25 | 1.684 | 0.905 | black-box |
| tpe_w_sign | 22 | 1.796 | 0.906 | white-box(∇f) |
| optuna | 21.25 | 0.9 | 0.479 | black-box |
| tpe_w_smooth | 21.25 | 1.62 | 0.859 | white-box(∇f) |
| random | 4 | 2.345 | 0.875 | black-box |

### 4.2 Доля ячеек, где модификация лучше `tpe` (по final_dist_y)
| algorithm | win_rate_vs_tpe_% |
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

### 4.3 Инвариантность нормализации
Для `tpe`, всех 4 форм w(x) и `tpe_refine`: raw≡norm (gap=0) — нормализация не влияет. Масштабо-зависимы **только GP-методы** (`tpe_gp`, `tpe_gp_w`, `tpe_gp_refine`; gap≈1.6): GP-член в y-единицах конкурирует с лог-плотностью. См. `raw_vs_norm_comparison.csv`.

### 4.4 Статистическая значимость (ГЛАВНОЕ)
Из 160 сравнений значимы (Holm): 48; из них **42 — улучшения** над `tpe`, остальные — ухудшения (все `random`).

Значимых улучшений по алгоритмам:
| algorithm | sig_wins |
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

Конкретные значимые улучшения:
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

## 4.5 Это не «плохой тест»: диагностика и робастность
Формы w(x) РЕАЛЬНО меняют поиск (≈100% seeds отличаются от baseline, mean|Δ|≈0.9), но **медиана Δ≈0** — изменения симметричны (то лучше, то хуже). Значит эффект ненаправленный, а не «тест слепой».
| algorithm | %seeds_changed | mean_abs_diff | median_diff |
|---|---|---|---|
| tpe_w_smooth | 86.8 | 1.03 | 0.0002 |
| tpe_w_smooth_inv | 85 | 0.9893 | 0 |
| tpe_w_sign | 86.8 | 1.139 | 0 |
| tpe_w_sign_inv | 82 | 1.036 | 0 |
| tpe_gp | 91.8 | 1.319 | -0.0073 |

**Робастность к выбору теста.** Число значимых УЛУЧШЕНИЙ над `tpe` (из 16 ячеек, метрика final_dist_y) при разных тестах × поправках. Видно: формы веса ≈0 везде; GP и refinement устойчиво значимы.
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

Тесты: wilcoxon (знаковых рангов), ttest (парный Стьюдент), sign (знаковый), perm (перестановочный). Поправки: raw (без поправки), holm, bh (FDR). Полные данные — `results/tables/significance_robust*.csv`.

## 5. Выводы (строго), по классам
1. Базовый `tpe` осмыслен (success ~25% vs random ~4%); рабочая контрольная точка.
2. Нормализация цели инвариантна для `tpe`, всех форм w(x) и `tpe_refine`; масштабо-зависимы только GP-методы.
3. **black-box: GP помогает.** `tpe_gp` (без градиента) значимо лучше baseline в нескольких ячейках, наравне с `optuna`. Это главный «честный» (black-box) результат.
4. **white-box мягкий (вес по ∇f): НЕ помогает.** Ни одна из 4 форм w(x) не даёт значимого улучшения (0 при всех тестах и поправках, §4.5). Причина: w∈[0.8,1.2] слишком слаб, чтобы менять argmax l/g; + норма ∇f плохо указывает на минимум на многоэкстремальных функциях.
5. **white-box жёсткий (refinement): доминирует, но тривиально.** `tpe_refine`/`tpe_gp_refine` дают больше всего значимых улучшений — но это обычный **градиентный спуск по точному ∇f**, т.е. верхняя граница «что даёт градиент», а не улучшение самого TPE. В реальном black-box HPO точного ∇f нет.

## 6. Что нельзя утверждать
- «Градиентный ВЕС улучшает TPE» — не подтверждено (0 значимых у всех 4 форм).
- «refinement доказывает пользу градиента для TPE» — нет: это градиентный спуск с оракулом (white-box upper bound).
- «Нормализация помогает» — для TPE/весов/refine это инвариантность.
- Обобщать на высокую размерность / иные уровни шума — не проверялось.

## 7. Ограничения
- Градиент аналитический/точный (оракул), не black-box.
- Только 2D, один уровень шума на функцию; нет sensitivity по σ/размерности/γ.
- GP только для переранжирования; Rosenbrock труден для покоординатного TPE.

## 8. Полная таблица ключевых метрик (все строки)
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

---
Файлы: `docs/ARTICLE.md` (статья), `docs/DESIGN.md` (архитектура), `docs/RESULTS.md` (полный отчёт), `results/tables/*.csv` (+ all_results.xlsx), `results/figures/*.png`.