# Разбор экспериментов (по каждому исходному файлу)

> Все числа ниже взяты из **сохранённых выводов** самих исходных ноутбуков (30 seeds).
> Это реальные результаты, а не пересчёт. Полные таблицы воспроизводятся прогоном `colab_experiments/01–05`.

---

## 1. `fin_fin_1 (2).ipynb` — «01 Baseline (clean)»

- **Роль:** базовая контрольная точка.
- **Цель:** показать, что repo-TPE без модификаций осмысленно работает (бьёт random, сравним с Optuna).
- **Способ изменения ТПЕ:** нет.
- **Входные данные:** 4 clean функции (Sphere/Rosenbrock/Rastrigin/Ackley, 2D), bounds зашиты.
- **Ключевые параметры:** `SEEDS=range(30)`, `N_INIT=25` (❗отличается от остальных), `MAX_EVALS=100`,
  `BASE_KWARGS={n_ei_candidates:24, min_bandwidth_factor:1e-2, top:0.2}`. Пороги мягкие (Sphere 1e-2 …).
- **Метод:** `RandomSearch`, `TPEOptimizer` (no_w), `Optuna TPESampler`.
- **Основная логика:** `run_once` → `build_curves_from_history` строит best-so-far по dist_x/dist_y; `run_benchmark` гоняет random+tpe; шаг до порога считается по `dist_y_curve`.
- **Что считается / метрики:** success_rate_%, steps_mean/var, final_dist_x_mean/var, final_dist_y_mean/var, по-seed steps.
- **Файлы:** `results/01_baseline_summary_clean.csv`, `results/01_baseline_iteration_history_clean.csv`; графики dist_x/dist_y + карты траекторий.
- **Реальные результаты (success_rate %):** Sphere no_w **60.0** / optuna 43.3 / random 3.3; Rosenbrock no_w **53.3** / optuna 30 / random 23.3; Rastrigin no_w **56.7** / optuna 36.7 / random 3.3; Ackley no_w 23.3 / optuna **36.7** / random 3.3.
- **Выводы МОЖНО:** repo-TPE стабильно > random; на 3/4 функций ≥ Optuna при n_init=25.
- **Выводы НЕЛЬЗЯ:** переносить эти числа в сравнение с 03/04/05 (другой n_init и пороги).
- **Слабые места:** n_init=25 и мягкие пороги выбиваются из остальной серии.

---

## 2. `fin_fin_2 (1).ipynb` — «03 Noisy-y baseline»

- **Роль:** базовая точка + sensitivity к шуму.
- **Цель:** как шум в y влияет на random/no_w/optuna; качество меряется по clean.
- **Способ изменения ТПЕ:** нет; меняются только данные (clean vs noisy_y).
- **Параметры:** `N_INIT=10`, `MAX_EVALS=100`, пороги мягкие (как в 01), `NOISE_SIGMA` (Sphere 0.005 … Rastrigin 0.25).
- **Метод/логика:** `make_noisy_y_fn` добавляет N(0,σ) к clean; `run_benchmark_for_data` для clean/noisy. ❗ Для random и tpe — **разные** генераторы шума (10000+s, 20000+s), для optuna — 30000+s.
- **Метрики:** mean_steps, success_rate_%, clean_mean/median/std, dist_mean/median/std.
- **Файлы:** `results/03_noisy_y_baseline_summary.csv`; графики dist_x/dist_y/observed + карты.
- **Реальные результаты (mean_steps clean→noisy для no_w):** Rosenbrock 32.3→25.0; Rastrigin 45.6→44.6; Sphere 57.1→56.5; Ackley 58.2→58.6.
- **Выводы МОЖНО:** при выбранных небольших σ базовый TPE устойчив (метрики почти не падают).
- **Выводы НЕЛЬЗЯ:** обобщать на большие σ (тестировался один уровень шума); строго сравнивать методы внутри ноутбука (разный шум у разных методов).

---

## 3. `fin_3_raw_vs_norm_METRICS_VISIBLE_FIXED_2 (1).ipynb` — «04 Raw vs Normalized» (МЕТОД 1)

- **Роль:** первый «способ изменения ТПЕ».
- **Цель:** помогает ли TPE нормализация objective f_norm=(f−f_min)/(f_max−f_min)?
- **Способ изменения ТПЕ:** масштабирование целевой функции. f_max — по 50 000 случайных точек (seed=123), f_min=0.
- **Параметры:** `N_INIT=10`, `MAX_EVALS=100`, пороги **жёсткие** (Sphere 1e-3 …). σ_norm = σ_raw / (f_max−f_min).
- **Варианты×режимы:** {random,no_w,optuna} × {raw,norm} × {clean,noisy_y}. ❗ ГСЧ шума зависит от `hash((fn_name, scale_type, data_type))`.
- **Метрики:** success_rate_%, steps_*, final_dist_x_*, final_dist_y_*; + comparison-таблица raw vs norm; + iteration history.
- **Файлы:** `04_raw_vs_normalized_summary_clean.csv`, `..._comparison_clean.csv`, `..._iteration_history_clean.csv`.
- **🔑 РЕАЛЬНАЯ НАХОДКА (из comparison-таблицы):** на **clean** данных `delta_success_norm_minus_raw = 0` ВО ВСЕХ строках, а `raw_steps_mean == norm_steps_mean` (напр. Sphere no_w 57.588 == 57.588). То есть raw и norm для рангового TPE **идентичны** на clean.
- **Объяснение:** TPE/Optuna используют только **порядок** значений (split good/bad по γ). Монотонно-аффинное масштабирование порядок не меняет → инвариантность. Нормализация для рангового сэмплера на clean — **no-op**.
- **noisy_y различия** (напр. optuna Sphere noisy delta −6.67; Rastrigin −13.3) **артефактны**: scale_type входит в seed шума → raw и norm видят РАЗНЫЙ шум.
- **Выводы МОЖНО (строго):** для рангового TPE нормализация objective не влияет на clean-результат — экспериментально подтверждённая инвариантность.
- **Выводы НЕЛЬЗЯ:** трактовать noisy raw-vs-norm как пользу/вред нормализации — сравнение неконтролируемо по шуму.
- **Как починить:** для честного noisy-сравнения убрать `scale_type` из seed шума (общий шум для raw и norm). Это правка в НОВОМ коде, не в оригинале.

---

## 4. `fin_4_with_w_x.ipynb` — «TPE + w(x)» (МЕТОД 2)

- **Роль:** второй «способ изменения ТПЕ» — мягкий вес в KDE repo-TPE.
- **Цель:** улучшить TPE множителем w(x) по норме (аналитического) градиента.
- **Способ:** `TPEOptimizer(..., weight_fn=w)`, w(x)=clip(1+0.2·z, **0.8..1.2**), z из нормированной ||∇f||. Формы: `smooth`(tanh), `smooth_inv`, `sign_like`(сигмоида·5), `sign_like_inv`.
- **Параметры:** N_INIT=10, MAX_EVALS=100, пороги жёсткие. Аналитические ∇ для raw; для norm — ∇/(f_max−f_min).
- **Варианты×режимы:** {random,no_w,grad_smooth,grad_smooth_inv,grad_sign_like,grad_sign_like_inv,optuna} × {raw,norm} × {clean,noisy_y}. ❗ Все варианты при данном seed видят **один и тот же шум** (общие случайные числа) — хорошая парность (отличие от fin_3).
- **Метрики/файлы:** как в 03; `tpe_grad_weights_summary_full.csv` и `..._visible.csv`.
- **Реальный фрагмент (Sphere, raw, noisy_y, final_dist_y_mean):** grad_* и no_w в диапазоне ~0.006–0.02 — близко, без явного устойчивого лидера grad-формы.
- **🔴🔴 ПОДТВЕРЖДЁННЫЙ ДЕФЕКТ (проверено по исходнику `tpe/optimizer/tpe.py`, строки 232–252):** repo-`TPEOptimizer` вызывает `weight_fn` один раз на пачку кандидатов с 1D-массивом `samples = np.stack([x0,x1],axis=1).mean(axis=1)`, т.е. это **среднее координат (x0+x1)/2** на кандидата — НЕ 2D-точки и НЕ покоординатно. Затем `_as_2d_points` сопоставляет скаляру m точку **(m, 0)** и считает ∇f там → **градиент вычисляется в фиктивной точке**. Для Sphere истинная ‖∇f‖=2√(x0²+x1²), а код считает |x0+x1|. **Метод 2 в текущем виде НЕ реализует градиентное взвешивание.** (Это уже факт, не риск.)
- **🟠 Доп. деталь:** `compute_log_weight`→`scale_to_range` заново min-max-нормирует веса в [0.8,1.2] по кандидатам → множитель `1+0.2·z` из ноутбука отбрасывается, выживает только РАНГ grad-нормы-в-(m,0). Бо́льший вес → выше pi → кандидат предпочтительнее. Нормировка ∇ — константа, поэтому raw и norm для grad_* совпадают.
- **🟠 Ещё:** даже при верной точке использовался бы ТОЧНЫЙ аналитический ∇f benchmark-а → «белый ящик», не реальный black-box HPO.
- **Выводы МОЖНО (строго):** результаты grad_* нельзя интерпретировать как «градиентное взвешивание»; эффект мал и геометрически не осмыслен (~0.006–0.02, как no_w).
- **Выводы НЕЛЬЗЯ:** «w(x) по градиенту улучшает/ухудшает TPE» — метод сначала надо исправить.
- **Как исправить (в НОВОМ коде):** либо доработать repo-TPE так, чтобы `weight_fn` получал 2D-точки (n,2); либо считать вес внутри подкласса `TreeStructuredParzenEstimator`, где доступны и `config_cands['x0']`, и `['x1']`.

---

## 5. `fin_5_gTPE.ipynb` — «gTPE» (МЕТОД 3)

- **Роль:** третий «способ» — внешняя самостоятельная реализация gradient-aware TPE + GP.
- **Цель:** добавить gTPE как baseline в те же таблицы/графики.
- **Способ:** `GradientAwareTPE` (встроена строкой-исходником, выполнена через `exec` в модуль `gtpe_embedded`):
  взвешивание наблюдений KDE по 1/(||grad||+σ+ε) (`gradient_mode='weight'`) + **GP-reranking** кандидатов
  (RBF-GP с нормализацией X/Y, медианный lengthscale; score = logl − logg − μ + β·σ). `eval_repeats=1`, `gradient_refine_steps=0` (честный бюджет).
- **Сопоставление параметров:** gamma=top=0.2, n_candidates=24, n_startup=10, n_trials=100.
- **Все 8 вариантов:** добавляется `gTPE` к набору из fin_4.
- **🔴 КАВЕАТ 1:** gTPE — ДРУГАЯ реализация (своя KDE/split/GP), отличается от repo-TPE по МНОГИМ осям → «gTPE vs no_w» не ablation, а сравнение алгоритмов целиком.
- **🟠 КАВЕАТ 2:** в noisy_y градиент остаётся ТОЧНЫМ (шум только в value).
- **Реальный фрагмент (Sphere, raw, noisy_y):** gTPE final_dist_y_mean ≈ **0.397** против ~0.006–0.02 у repo-TPE/optuna → на гладкой функции gTPE заметно ХУЖЕ (вероятно, GP-reranking/веса мешают на простом ландшафте).
- **Выводы МОЖНО:** gTPE не доминирует; на ряде функций уступает.
- **Выводы НЕЛЬЗЯ:** называть gTPE улучшением TPE (другая реализация + точный градиент).
- **Доп. содержимое исходника:** внутри строки-исходника есть собственный `run_full_experiment` на rastrigin/rosenbrock/quadratic (3 функции, n_repeats=100) и unit-тесты `TestGradientAwareTPE` — они НЕ вызываются в основном пайплайне (только класс используется), но полезны как проверка корректности градиентов/GP.
