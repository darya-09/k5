# ПОЛНЫЕ ВЫВОДЫ ДЛЯ КУРСОВОЙ — сравнение способов модификации TPE

Самодостаточный файл: всё нужное для текста курсовой, числа — из реального прогона (50 seeds, PYTHONHASHSEED=0). Код: репозиторий darya-09/k5, ветка claude/quirky-euler-e3laj1, папка `tpe_study/`.

## 1. Цель и постановка
Сравнить **способы изменения TPE** (Tree-structured Parzen Estimator) и понять, какие из них реально улучшают оптимизацию. TPE: делит наблюдения по порогу γ на «хорошие»/«плохие», строит ядерные плотности l(x)/g(x), выбирает кандидата с максимумом l(x)/g(x).

**Проверяемые модификации (каждая — изолированный фактор одной реализации):**
- A. Нормализация цели f_norm=(f−f_min)/(f_max−f_min) (фактор `scale`: raw/norm).
- B. Градиентное взвешивание наблюдений w=1/(‖∇f‖+ε)^p (истинный ∇f в реальной точке) — `tpe_gradw`.
- C. GP-переранжирование кандидатов (RBF-GP) — `tpe_gp`.
- B+C вместе (аналог «gTPE») — `tpe_gradw_gp`.
- Референсы: `random` (нижняя граница), `optuna` (зрелый TPE).

## 2. Установка эксперимента
- Функции (2D): Sphere, Rosenbrock, Rastrigin, Ackley.
- Сетка: функция × scale(raw,norm) × data(clean,noisy_y) × алгоритм × seed.
- Параметры: n_init=10, γ=0.15, n_candidates=24, max_evals=80, seeds=50.
- Шум: гауссов в значении (clean/noisy_y), зависит только от (функция,seed) ⇒ все методы и обе шкалы видят ОДИН шум (парность, common random numbers). Градиент остаётся точным.
- Оценка ВСЕГДА по raw clean функции; метрики: success_rate (доля достигших строгого порога), final_dist_y=|f(x_best)−f*|, final_dist_x=‖x_best−x*‖, шаги до порога.
- Значимость: парный Уилкоксон каждой модификации vs baseline `tpe` по seeds + поправка Холма (FWER).
- Контроль кода: 21 pytest-тест (градиенты=конечные разности, KDE, инвариантность, воспроизводимость).

## 3. Главные результаты (числа из прогона)

### 3.1 Средние по всем 16 ячейкам, по алгоритмам
| algorithm | success_rate_% | final_dist_y_mean | final_dist_x_mean |
|---|---|---|---|
| optuna | 15.75 | 1.098 | 0.547 |
| random | 3.5 | 2.627 | 0.943 |
| tpe | 36 | 1.271 | 0.765 |
| tpe_gp | 42.5 | 1.161 | 0.678 |
| tpe_gradw | 30.62 | 1.348 | 0.712 |
| tpe_gradw_gp | 36.5 | 1.142 | 0.659 |

### 3.2 Как часто модификация лучше baseline `tpe` (доля ячеек, по final_dist_y)
| algorithm | win_rate_vs_tpe_% |
|---|---|
| optuna | 50 |
| random | 25 |
| tpe_gp | 75 |
| tpe_gradw | 43.8 |
| tpe_gradw_gp | 62.5 |

### 3.3 Инвариантность нормализации
Для чистого рангового `tpe` на clean: raw и norm дают **идентичный** результат (max |raw−norm| по final_dist_y = 0.0) — монотонно-аффинное масштабирование не меняет ранги. Для `tpe_gradw`/`tpe_gp` разрывы 0.83/1.6 (масштабо-зависимы: градиентный вес зависит от масштаба ∇, GP-член в y-единицах). Вывод: нормализация для базового TPE — no-op, важна лишь для grad/GP-вариантов.

### 3.4 Статистическая значимость (ГЛАВНОЕ)
Из 80 сравнений значимы (Holm, p<0.05): 24; из них 12 — улучшения над `tpe`, остальные — ухудшения (все `random`).

Значимых улучшений по алгоритмам:
| algorithm | sig_wins |
|---|---|
| optuna | 4 |
| random | 0 |
| tpe_gp | 4 |
| tpe_gradw | 0 |
| tpe_gradw_gp | 4 |

Конкретные значимые улучшения над baseline `tpe`:
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

## 4. Выводы (что можно утверждать СТРОГО)
1. Базовый TPE осмыслен: средний success 36.0% против random 3.5%; сопоставим с Optuna по final_dist_y.
2. **Нормализация цели для рангового TPE строго НЕ влияет** (инвариантность, gap=0); полезна только grad/GP-вариантам.
3. **GP-переранжирование — единственная модификация TPE с устойчивым значимым эффектом**: по 4 значимых улучшения у `tpe_gp` и `tpe_gradw_gp`, на гладкой Sphere и овражной Rosenbrock.
4. **Градиентное взвешивание само по себе бесполезно**: 0 значимых улучшений даже при ТОЧНОМ градиенте. Комбинация gradw+GP не превосходит чистый GP — выигрыш идёт от GP, не от градиента.
5. Методологический вывод: средние/доли выигрышей (44–75%) переоценивают эффект; только парные тесты значимости дают честную картину (значимых улучшений 12 из 80). Рост 20→50 seeds поднял значимые улучшения с 7 до 12.

## 5. Что утверждать НЕЛЬЗЯ
- «Градиентная информация улучшает TPE» — не подтверждено (gradw: 0 значимых).
- «Нормализация помогает оптимизации» — для TPE это инвариантность, не польза.
- Обобщать на высокие размерности / другие уровни шума — не проверялось.

## 6. Ограничения (для раздела «ограничения» курсовой)
- Градиент аналитический/точный (оракул), не black-box; реалистичнее — шумный/конечно-разностный.
- Только 2D и один уровень шума на функцию; нет sensitivity по σ, размерности, γ, бюджету.
- GP только для переранжирования (не полноценный BO). Rosenbrock труден для покоординатного TPE.

## 7. Возможные следующие шаги
- Sensitivity по уровню шума σ; рост размерности (5D/10D); 100 seeds для финала.
- Ablation внутри GP (длина корреляции, β); шумный градиент.

## 8. Полная таблица ключевых метрик (все 96 строк: функция×scale×data×алгоритм)
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

---
Файлы проекта: `tpe_study/docs/ARTICLE.md` (статья), `docs/DESIGN.md` (архитектура), `docs/RESULTS.md` (полный отчёт), `results/tables/*.csv` (+ all_results.xlsx), `results/figures/*.png` (32 графика).