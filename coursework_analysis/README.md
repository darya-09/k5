> ⚠️ **УСТАРЕЛО / АРХИВНЫЙ СЛОЙ.** Этот каталог — ранний слой-обёртка над исходными ноутбуками;
> он **не исполнялся** (папки `results/`, `tables/`, `figures/` пусты, код требует Google Drive).
> Актуальная самодостаточная реализация с реальными результатами — в **`../tpe_study/`**.
> Общий аудит репозитория — в **`../FINAL_PROJECT_REPORT.md`**. Этот каталог сохранён как провенанс.

# coursework_analysis — рабочий слой над исследованием ТПЕ

Этот каталог создан **рядом** с исходными ноутбуками и **не изменяет** их.
Все обёртки, унификация, сбор результатов и отчёты — здесь.

## Структура
```
coursework_analysis/
  colab_experiments/                 # Google Colab notebooks (обёртки)
    00_repository_map.ipynb          # карта репозитория
    01_experiment_baseline_clean.ipynb
    02_experiment_baseline_noisy.ipynb
    03_experiment_raw_vs_norm.ipynb        # метод 1: нормализация
    04_experiment_tpe_wx_gradient.ipynb    # метод 2: w(x)
    05_experiment_gtpe.ipynb               # метод 3: gTPE
    06_compare_results.ipynb               # единые таблицы + графики
    07_final_summary_for_coursework.ipynb  # сборка отчётов
  configs/
    common_config.json               # общие параметры + флаги несостыковок
    experiments_config.json          # реестр экспериментов и какие CSV куда
  results/raw/                        # собранные CSV из исходников + *_runmeta.json
  results/processed/                  # очищенные/объединённые данные
  tables/                            # experiments_summary.csv, metrics_comparison.xlsx, ablation_*
  figures/                           # графики .png
  reports/
    final_experiments_summary.md            # ГЛАВНЫЙ отчёт
    final_experiments_summary_for_chat.txt  # текст для передачи в другой чат
    repository_map.md
    experiment_analyses.md                  # разбор каждого файла
    scientific_review.md                    # научная корректность
```

## Как пользоваться
1. Открыть `colab_experiments/00_repository_map.ipynb` — обзор.
2. Прогнать `01..05` (ячейка `run_original_and_harvest(EXP_ID)`): они выполняют **исходные**
   ноутбуки как есть (через `nbconvert --execute`) и складывают CSV в `results/raw/`.
3. `06_compare_results.ipynb` — собирает `tables/` и `figures/`.
4. `07_final_summary_for_coursework.ipynb` — печатает финальные отчёты.

## Важно про воспроизводимость
Код **не запускается без Google Drive**: пакет `tpe/` (репозиторий оптимизатора) лежит только в Drive,
в git его нет. Параметры зашиты в исходниках; обёртки их не переопределяют (правило «не менять исходники»).
Полный список «Нужно предоставить» — в `reports/final_experiments_summary.md` §13.

## Архитектурная рекомендация (кратко; подробно — §ниже)
**Оставить отдельные эксперименты, но добавить тонкий общий слой** (этот каталог), а не сливать всё в один pipeline.
Причины: исходники почти дублируют друг друга, но различаются ключевыми факторами (n_init, пороги, набор вариантов,
способ генерации шума) — насильное слияние спрячет именно те различия, которые важны для честного сравнения.

### Если в будущем рефакторить в единый pipeline
Вынести в модуль `tpe_bench/`:
- `functions.py` (clean/grad/norm — сейчас дублируются в 5 файлах);
- `noise.py` (единый генератор шума с фиксированным seed, без `hash()`);
- `runner.py` (`run_once`, `run_optuna`, `run_gtpe`);
- `weights.py` (w(x));
- `metrics.py`, `plots.py`;
- `configs/*.yaml` на каждый эксперимент (один меняющийся фактор на конфиг);
- `main.py --exp <id>`.
Тогда «способ изменения ТПЕ» = один параметр конфига, а baseline и пороги общие → честное сравнение по построению.

### Что уже реализовано / что предлагается
- **Реализовано (в исходниках):** baseline, метод 1, метод 2, метод 3, метрики, графики, 30 seeds.
- **Реализовано (здесь):** карта, разбор, единый сбор результатов, сравнительные таблицы, отчёты, чек-лист доступов.
- **Предлагается (новые идеи):** проверка вызова weight_fn; стат-тесты; sensitivity по σ/γ; честный noisy для fin_3;
  ablation gTPE; шумный градиент. См. `reports/scientific_review.md` §8.12.
