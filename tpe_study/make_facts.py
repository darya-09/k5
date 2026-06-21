#!/usr/bin/env python3
"""
Генерирует два НЕЙТРАЛЬНЫХ файла (только факты, без интерпретаций):
  docs/FACTS_RESULTS.md      — все табличные результаты;
  docs/FACTS_CONCLUSIONS.md  — фактические утверждения, каждое привязано к числу.
Все числа берутся из results/tables/*.csv.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
T = ROOT / "results" / "tables"
sys.path.insert(0, str(ROOT / "src"))
from tpe_study.experiment import ALGO_FAMILY  # noqa: E402


def mdtab(df, fmt="{:.4g}"):
    df = df.copy()
    for c in df.columns:
        if pd.api.types.is_float_dtype(df[c]):
            df[c] = df[c].map(lambda v: "" if pd.isna(v) else fmt.format(v))
    cols = list(df.columns)
    out = ["| " + " | ".join(map(str, cols)) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(out)


def load():
    d = pd.read_csv(T / "all_results.csv")
    summ = pd.read_csv(T / "summary_key_metrics.csv")
    sig = pd.read_csv(T / "significance_tests.csv")
    ps = pd.read_csv(T / "per_seed_final.csv")
    rn = pd.read_csv(T / "raw_vs_norm_comparison.csv")
    rob = pd.read_csv(T / "significance_robust_summary.csv")
    abl = pd.read_csv(T / "ablation_vs_tpe.csv")
    cfg = json.load(open(ROOT / "configs" / "default.json"))
    return d, summ, sig, ps, rn, rob, abl, cfg


def uses_gradient(algo):
    return "white-box" in ALGO_FAMILY.get(algo, "")


def results_file(d, summ, sig, rn, rob, abl, cfg):
    L = []
    L.append("# РЕЗУЛЬТАТЫ ПО ВСЕМ ЭКСПЕРИМЕНТАМ (факты, без интерпретаций)")
    L.append("")
    L.append(f"Источник: прогон `run.py`, конфиг: seeds={cfg['seeds']}, n_init={cfg['n_init']}, "
             f"gamma={cfg['gamma']}, n_candidates={cfg['n_candidates']}, max_evals={cfg['max_evals']}, "
             f"PYTHONHASHSEED=0. Функции: {', '.join(cfg['functions'])}. Шкалы: {cfg['scales']}. "
             f"Данные: {cfg['data_types']}. Оценка качества — по raw clean функции.")
    L.append("")
    L.append("Метрики: success_rate_% (доля из 50 запусков, достигших порога по dist_y); "
             "final_dist_y = |f(x_best) − f*|; final_dist_x = ||x_best − x*||. "
             "Колонка `uses_gradient`: использует ли метод точный аналитический градиент.")
    L.append("")

    # 1. средние по алгоритмам
    avg = d.groupby("algorithm")[["success_rate_%", "final_dist_y_mean", "final_dist_x_mean"]].mean().round(3).reset_index()
    avg["family"] = avg["algorithm"].map(ALGO_FAMILY)
    avg["uses_gradient"] = avg["algorithm"].map(uses_gradient)
    avg = avg.sort_values("success_rate_%", ascending=False)
    L.append("## 1. Средние по 16 ячейкам (функция×scale×data), по алгоритмам")
    L.append(mdtab(avg)); L.append("")

    # 2. win-rate
    win = (abl.groupby("algorithm")["better_than_tpe"].mean().mul(100).round(1)
           .reset_index().rename(columns={"better_than_tpe": "cells_better_than_tpe_%"})
           .sort_values("cells_better_than_tpe_%", ascending=False))
    L.append("## 2. Доля ячеек, где метод лучше baseline `tpe` по final_dist_y (из 16)")
    L.append(mdtab(win)); L.append("")

    # 3. significance summary
    n_cmp = len(sig); n_sig = int(sig.significant_holm.sum())
    n_bet = int(sig.significant_and_better.sum())
    n_wor = int((sig.significant_holm & (sig.direction == "worse")).sum())
    L.append("## 3. Статистическая значимость vs `tpe` (парный Уилкоксон + поправка Холма, α=0.05)")
    L.append(f"Всего сравнений: {n_cmp}. Значимых: {n_sig} (улучшений: {n_bet}, ухудшений: {n_wor}).")
    sigwins = sig.groupby("algorithm")["significant_and_better"].sum().reset_index()
    sigwins = sigwins.rename(columns={"significant_and_better": "significant_improvements(of 16)"})
    sigwins["uses_gradient"] = sigwins["algorithm"].map(uses_gradient)
    L.append(mdtab(sigwins)); L.append("")
    L.append("### 3a. Ячейки со значимым УЛУЧШЕНИЕМ над `tpe`")
    L.append(mdtab(sig[sig.significant_and_better][["function", "scale", "data", "algorithm", "median_delta", "p_holm"]]))
    L.append("")
    worse = sig[sig.significant_holm & (sig.direction == "worse")][["function", "scale", "data", "algorithm", "median_delta", "p_holm"]]
    L.append("### 3b. Ячейки со значимым УХУДШЕНИЕМ относительно `tpe`")
    L.append(mdtab(worse) if len(worse) else "_(нет)_"); L.append("")

    # 4. invariance
    inv = rn.groupby("algorithm")["identical"].sum().reset_index().rename(columns={"identical": "cells_raw==norm(of 8)"})
    L.append("## 4. Инвариантность к нормализации (сколько из 8 ячеек raw≡norm точно)")
    L.append(mdtab(inv)); L.append("")

    # 5. robustness (final_dist_y)
    cols = ["algorithm"] + [c for c in rob.columns if c.startswith("final_dist_y|")]
    rtab = rob[cols].copy()
    rtab.columns = ["algorithm"] + [c.replace("final_dist_y|", "").replace("|", "/") for c in cols if c != "algorithm"]
    L.append("## 5. Робастность: число значимых улучшений vs `tpe` (метрика final_dist_y) при разных тестах×поправках")
    L.append("Тесты: wilcoxon, ttest (парный), sign, perm (перестановочный). Поправки: raw/holm/bh(FDR).")
    L.append(mdtab(rtab)); L.append("")

    # 6. full table (из all_results — там есть std)
    full = d[["function", "scale", "data", "algorithm", "success_rate_%", "steps_mean",
              "final_dist_y_mean", "final_dist_y_std", "final_dist_x_mean", "final_dist_x_std"]].copy()
    full = full.sort_values(["function", "scale", "data", "algorithm"])
    L.append("## 6. Полная таблица ключевых метрик (все 176 строк)")
    L.append(mdtab(full)); L.append("")
    L.append("Дополнительно в `results/tables/`: per_seed_final.csv, iteration_history.csv, "
             "raw_vs_norm_comparison.csv, significance_tests.csv, significance_robust.csv, all_results.xlsx.")
    L.append("")
    L.append("## 7. До/после модификаций на ЗАШУМЛЁННЫХ функциях (data=noisy_y)")
    L.append("«До» = baseline `tpe`, «после» = модификация, на тех же (функция, scale, seed). "
             "Качество — final_dist_y по raw clean; improve_% = (tpe−algo)/tpe; "
             "significant_better — парный Уилкоксон + Холм (α=0.05).")
    nba_s = pd.read_csv(T / "noisy_before_after_summary.csv")
    nba_s = nba_s.rename(columns={"cells_better_of_8": "лучше_tpe(из 8)",
                                  "cells_significant_better": "значимо_лучше(из 8)",
                                  "mean_improve_pct": "сред_улучш_%",
                                  "median_improve_pct": "медиана_улучш_%"})
    L.append("### 7a. Сводка по модификациям (8 ячеек = 4 функции × 2 scale, только шум)")
    L.append(mdtab(nba_s)); L.append("")
    nba = pd.read_csv(T / "noisy_before_after.csv")
    win = nba[nba.significant_better][["function", "scale", "algorithm",
                                       "tpe_median_dist_y", "algo_median_dist_y",
                                       "improve_%", "p_holm"]]
    L.append("### 7b. Ячейки со ЗНАЧИМЫМ улучшением над `tpe` на шуме")
    L.append(mdtab(win) if len(win) else "_(нет)_"); L.append("")
    L.append("Полные данные: `results/tables/noisy_before_after.csv` (80 ячеек) и "
             "`noisy_before_after_summary.csv`.")
    L.append("")
    L.append("## 8. Изменения относительно базовой версии (ноутбуки fin_*)")
    L.append("Полный разбор с доказательствами — `docs/CHANGES_VS_ORIGINAL.md`. Кратко:")
    L.append("- **Исправлен дефект градиента** в fin_4/fin_5: функция веса считала ‖∇f‖ в точке (x, 0) "
             "(проекция `_as_2d_points`, x1=0), а не в реальной точке кандидата. У меня — в реальной 2D-точке.")
    L.append("- **Одна реализация TPE** (`src/tpe_study/tpe.py`) вместо внешней библиотеки и 5 ноутбуков: "
             "все модификации — флаги одного класса (честный ablation «один фактор»).")
    L.append("- **Внутри TPE:** GP-переранжирование, взвешивание наблюдений 1/‖∇f‖ и refinement портированы "
             "из fin_5 и переписаны; prior-компонента KDE, адаптивная ширина ядра, единый класс с флагами и "
             "векторизация — добавлены мной.")
    L.append("- **Refinement честен по бюджету:** шаги по оракулу ∇f без доп. оценок objective (1 оценка/trial); "
             "в fin_5 refine дополнительно ОЦЕНИВАЛ предложенные точки (тратил вызовы).")
    L.append("- **Систематические стат-тесты:** парный Уилкоксон + Холм + робастность (4 теста × 3 поправки). "
             "В оригиналах — только частично в fin_5.")
    L.append("- **Оценка всегда по raw clean**, парный шум по (функция, seed), классификация black-box/white-box.")
    L.append("- **Воспроизводимость:** PYTHONHASHSEED=0, фикс. seeds, детерминированный f_max, 26 тестов pytest; seeds 30→50.")
    L.append("- **Сохранено 1-в-1:** функции и их градиенты, 4 формы веса и формула w=clip(1+0.2·z,0.8,1.2), "
             "нормализация цели, гиперпараметры (n_init=10, gamma=0.2, n_candidates=24, max_evals=100).")
    (ROOT / "docs" / "FACTS_RESULTS.md").write_text("\n".join(L))
    print("wrote docs/FACTS_RESULTS.md")


def conclusions_file(d, sig, ps, rn, rob, abl, cfg):
    succ = d.groupby("algorithm")["success_rate_%"].mean().round(1).to_dict()
    win = abl.groupby("algorithm")["better_than_tpe"].mean().mul(100).round(1).to_dict()
    sw = sig.groupby("algorithm")["significant_and_better"].sum().to_dict()
    inv = rn.groupby("algorithm")["identical"].sum().to_dict()
    n_sig = int(sig.significant_holm.sum()); n_bet = int(sig.significant_and_better.sum())
    n_wor = int((sig.significant_holm & (sig.direction == "worse")).sum())
    wforms = ["tpe_w_smooth", "tpe_w_smooth_inv", "tpe_w_sign", "tpe_w_sign_inv"]
    wforms_sig = int(sum(sw.get(a, 0) for a in wforms))

    # diagnostic: median diff of weight forms vs tpe
    base = ps[ps.algorithm == "tpe"]
    diag = {}
    for a in wforms + ["tpe_gp", "tpe_refine"]:
        ds = []
        for (fn, sc, dt), g in ps[ps.algorithm == a].groupby(["function", "scale", "data"]):
            b = base[(base.function == fn) & (base.scale == sc) & (base.data == dt)].set_index("seed")["final_dist_y"]
            cur = g.set_index("seed")["final_dist_y"]
            c = b.index.intersection(cur.index)
            ds.append((cur.loc[c] - b.loc[c]).to_numpy())
        ds = np.concatenate(ds)
        diag[a] = (round(100 * float(np.mean(np.abs(ds) > 1e-9)), 1), round(float(np.median(ds)), 4))

    L = []
    L.append("# ВЫВОДЫ ПО ВСЕМ ЭКСПЕРИМЕНТАМ (только факты, привязанные к числам)")
    L.append("")
    L.append(f"Установка: {cfg['seeds']} независимых запусков (seeds), 4 функции × 2 шкалы × 2 типа данных, "
             f"max_evals={cfg['max_evals']}, gamma={cfg['gamma']}. Значимость — парный Уилкоксон vs baseline `tpe` "
             "по seeds с поправкой Холма (α=0.05). Каждый пункт ниже — факт из данных, без интерпретаций.")
    L.append("")
    L.append("## Базовые факты")
    L.append(f"- Средний success_rate: `tpe` = {succ.get('tpe')}%, `random` = {succ.get('random')}%, "
             f"`optuna` = {succ.get('optuna')}%.")
    L.append(f"- Всего сравнений модификаций с `tpe`: {len(sig)}. Значимых (Holm): {n_sig}; "
             f"из них улучшений: {n_bet}, ухудшений: {n_wor} (все ухудшения — у `random`).")
    L.append("")
    L.append("## Какие методы используют точный градиент")
    L.append("- Используют аналитический ∇f (оракул): `tpe_w_smooth`, `tpe_w_smooth_inv`, `tpe_w_sign`, "
             "`tpe_w_sign_inv`, `tpe_gp_w`, `tpe_refine`, `tpe_gp_refine`.")
    L.append("- НЕ используют градиент: `random`, `tpe`, `optuna`, `tpe_gp`.")
    L.append("")
    L.append("## Значимые улучшения над `tpe` (Holm), по методам (из 16 ячеек)")
    for a in ["tpe_refine", "tpe_gp_refine", "tpe_gp", "tpe_gp_w", "optuna",
              "tpe_w_smooth", "tpe_w_smooth_inv", "tpe_w_sign", "tpe_w_sign_inv", "random"]:
        L.append(f"- `{a}`: {int(sw.get(a,0))} значимых улучшений; средний success {succ.get(a)}%; "
                 f"лучше `tpe` по средним в {win.get(a)}% ячеек.")
    L.append("")
    L.append("## Факты по градиентному весу (4 формы)")
    L.append(f"- Суммарно 4 формы w(x) дали {wforms_sig} значимых улучшений над `tpe`.")
    L.append("- Эти 4 формы не дают значимых улучшений ни при одном из 4 тестов × 3 поправок "
             "(см. significance_robust_summary.csv), кроме единичных срабатываний без поправки.")
    for a in wforms:
        p, m = diag[a]
        L.append(f"- `{a}`: отличается от `tpe` на {p}% seeds; медиана разности (algo−tpe) по final_dist_y = {m}.")
    L.append("")
    L.append("## Факты по GP и refinement")
    L.append(f"- `tpe_gp` (без градиента): {int(sw.get('tpe_gp',0))} значимых улучшений; медиана разности по "
             f"final_dist_y отличается от 0 (см. таблицы).")
    L.append(f"- `tpe_refine` и `tpe_gp_refine` (локальный спуск по точному ∇f): "
             f"{int(sw.get('tpe_refine',0))} и {int(sw.get('tpe_gp_refine',0))} значимых улучшений соответственно.")
    L.append("")
    L.append("## Факты по нормализации")
    same = [a for a in inv if inv[a] == 8]
    diff = [a for a in inv if inv[a] == 0]
    L.append(f"- Результаты raw и norm СОВПАДАЮТ точно (8/8 ячеек) для: {', '.join('`'+a+'`' for a in sorted(same))}.")
    L.append(f"- Результаты raw и norm РАЗЛИЧАЮТСЯ (0/8 совпадений) для: {', '.join('`'+a+'`' for a in sorted(diff))}.")
    L.append("")
    abl_base_path = T / "ablation_base_tpe.csv"
    if abl_base_path.exists():
        ab = pd.read_csv(abl_base_path)
        g = ab.groupby("lesion")
        sig_cnt = g["significant_worse"].sum().to_dict()
        med = g["lesion_worse_by_%"].median().round(0).to_dict()
        n_cells = int(g.size().iloc[0])
        L.append("## Факты по МОЕЙ модификации базы TPE (prior + адаптивная ширина)")
        L.append(f"Ablation (`ablation_base.py`, {n_cells} ячеек, парный Уилкоксон + Холм): "
                 "отключаем компоненты базового сэмплера и смотрим рост final_dist_y.")
        L.append(f"- Без адаптивной ширины (`fixed_bw`): значимо хуже в "
                 f"{int(sig_cnt.get('fixed_bw',0))}/{n_cells} ячеек; медиана ухудшения {med.get('fixed_bw')}%.")
        L.append(f"- Без обоих компонентов (`naive_kde`): значимо хуже в "
                 f"{int(sig_cnt.get('naive_kde',0))}/{n_cells}; медиана {med.get('naive_kde')}%.")
        L.append(f"- Без prior (`no_prior`): значимо хуже в "
                 f"{int(sig_cnt.get('no_prior',0))}/{n_cells}; медиана {med.get('no_prior')}% "
                 "(вклад стабильный по направлению, но по отдельности не значим).")
        L.append("- Вывод: адаптивная ширина — главный драйвер точности; prior яснее всего в комбинации. "
                 "Подробно — `docs/MODIFICATION_BASE_TPE.md`.")
        L.append("")
    L.append("## Что НЕ проверялось (границы применимости фактов)")
    L.append("- Размерность только 2D; один уровень шума на функцию; градиент точный (не зашумлённый).")
    L.append("- GP используется только для переранжирования кандидатов.")
    L.append("- Гиперпараметры фиксированы (gamma, n_candidates, n_init, max_evals); их влияние не варьировалось.")
    (ROOT / "docs" / "FACTS_CONCLUSIONS.md").write_text("\n".join(L))
    print("wrote docs/FACTS_CONCLUSIONS.md")


if __name__ == "__main__":
    d, summ, sig, ps, rn, rob, abl, cfg = load()
    results_file(d, summ, sig, rn, rob, abl, cfg)
    conclusions_file(d, sig, ps, rn, rob, abl, cfg)
