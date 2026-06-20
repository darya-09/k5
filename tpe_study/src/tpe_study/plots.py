"""Графики: кривые сходимости (среднее±std по seeds) и контурные карты выбора точек."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import matplotlib
matplotlib.use("Agg")            # без дисплея (сохраняем в файлы)
import matplotlib.pyplot as plt
import numpy as np

from .functions import Benchmark

ALGO_STYLE = {
    "random":           ("black",      "--"),
    "tpe":              ("tab:gray",   "-"),
    "tpe_w_smooth":     ("tab:blue",   "-"),
    "tpe_w_smooth_inv": ("tab:cyan",   "-"),
    "tpe_w_sign":       ("tab:red",    "-"),
    "tpe_w_sign_inv":   ("tab:orange", "-"),
    "tpe_gp":           ("tab:green",  "-"),
    "tpe_gp_w":         ("tab:brown",  "-"),
    "optuna":           ("tab:purple", "-."),
}


def plot_convergence(bench: Benchmark, scale: str, data: str,
                     curves_by_algo: Dict[str, List[dict]], out: Path):
    """dist_y(t) и dist_x(t): среднее по seeds + полоса ±std (лог-шкала по y)."""
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
    fig.suptitle(f"{bench.name} | scale={scale} | data={data}", fontsize=12)
    for metric, ax, ylabel in [("dist_y", axes[0], "ошибка по значению |f-f*|"),
                               ("dist_x", axes[1], "ошибка по аргументу ||x-x*||")]:
        for algo, curves in curves_by_algo.items():
            M = np.vstack([c[metric] for c in curves])
            mean, std = M.mean(0), M.std(0)
            t = np.arange(1, len(mean) + 1)
            color, ls = ALGO_STYLE.get(algo, (None, "-"))
            ax.plot(t, mean, label=algo, color=color, linestyle=ls, linewidth=2)
            ax.fill_between(t, np.clip(mean - std, 1e-12, None), mean + std,
                            color=color, alpha=0.12)
        ax.set_yscale("log"); ax.set_xlabel("итерация"); ax.set_ylabel(ylabel)
        ax.grid(alpha=0.3, which="both"); ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out, dpi=130); plt.close(fig)


def plot_choice_map(bench: Benchmark, scale: str, data: str,
                    curves_by_algo: Dict[str, List[dict]], out: Path, seed_index: int = 0):
    """Контур raw clean функции + выбранные точки для 3 ключевых алгоритмов."""
    show = [a for a in ["tpe", "tpe_w_smooth_inv", "tpe_gp_w"] if a in curves_by_algo]
    (lo0, hi0), (lo1, hi1) = bench.bounds
    gx = np.linspace(lo0, hi0, 160); gy = np.linspace(lo1, hi1, 160)
    GX, GY = np.meshgrid(gx, gy)
    Z = np.array([[bench.f(np.array([a, b])) for a in gx] for b in gy])

    fig, axes = plt.subplots(1, len(show), figsize=(5.2 * len(show), 4.6), squeeze=False)
    fig.suptitle(f"{bench.name} | scale={scale} | data={data} | выбор точек", fontsize=12)
    for ax, algo in zip(axes[0], show):
        pts = curves_by_algo[algo][seed_index]["x_history"]
        ax.contourf(GX, GY, Z, levels=40, alpha=0.8, cmap="cividis")
        ax.plot(pts[:, 0], pts[:, 1], "-", lw=0.7, color="white", alpha=0.8)
        ax.scatter(pts[:, 0], pts[:, 1], s=14, c="white", edgecolors="black", linewidths=0.3)
        ax.scatter(*bench.x_star, marker="*", s=220, c="red", edgecolors="black", label="x*")
        ax.set_title(algo, fontsize=10); ax.set_xlabel("x0"); ax.set_ylabel("x1")
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out, dpi=130); plt.close(fig)
