# tpe_study — чистые воспроизводимые эксперименты по способам изменения TPE

Самодостаточный, аккуратно написанный проект для сравнения **способов модификации TPE**
(Tree-structured Parzen Estimator) на 2D benchmark-функциях. Каждая модификация — это
**отдельный изолированный фактор**, поэтому сравнения честные (ablation одного фактора).

> Это «идеальная» переработка исходных ноутбуков (`fin_*`). Исходники не тронуты; здесь —
> корректная версия без известных дефектов (см. `docs/DESIGN.md`, раздел 1).

## Быстрый старт
```bash
cd tpe_study
pip install -r requirements.txt
PYTHONHASHSEED=0 python run.py            # полный прогон (~8-10 мин)
PYTHONHASHSEED=0 python run.py --quick    # быстрая проверка (3 seeds)
```
После запуска:
- таблицы → `results/tables/` (`all_results.csv`, `summary_key_metrics.csv`, `per_seed_final.csv`,
  `ablation_vs_tpe.csv`, `significance_tests.csv`, `all_results.xlsx`);
- графики → `results/figures/` (`conv_*.png` — сходимость, `map_*.png` — карты выбора точек);
- разбор чисел → `docs/RESULTS.md`; статья → `docs/ARTICLE.md`.

## Тесты
```bash
pytest                 # программные тесты корректности кода (tests/)
```
Статистические тесты значимости (парный Уилкоксон + Холм) считаются автоматически в `run.py`
и пишутся в `results/tables/significance_tests.csv`. Разница двух видов тестов — в `docs/DESIGN.md`.

## Что сравнивается
| algorithm | модификация (один фактор) |
|---|---|
| `random` | — (нижняя граница) |
| `tpe` | базовый TPE |
| `tpe_gradw` | + градиентное взвешивание наблюдений (истинный ∇f в реальной точке) |
| `tpe_gp` | + GP-переранжирование кандидатов |
| `tpe_gradw_gp` | + оба (это «gTPE») |
| `optuna` | внешний референс TPE |

Плюс фактор `scale ∈ {raw, norm}` (нормализация целевой функции) и `data ∈ {clean, noisy_y}`.

## Документация
- `docs/DESIGN.md` — архитектура: что где, какие алгоритмы, откуда что берётся, в каком порядке и почему.
- `docs/RESULTS.md` — табличные результаты и графики после запуска, с выводами.

## Принципы корректности
Единый конфиг для всех алгоритмов, общие случайные числа (один шум на seed для всех методов),
оценка качества всегда по raw clean функции, фиксированные seeds и `PYTHONHASHSEED=0`.
Подробности — в `docs/DESIGN.md`, раздел 6.

## Зависимости
Только `numpy`, `scipy`, `pandas`, `matplotlib`, `optuna` — без ConfigSpace/parzen-estimator
и без Google Drive. Работает локально и в Colab.
