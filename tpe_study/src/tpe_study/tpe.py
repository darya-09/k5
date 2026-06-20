"""
Чистая, самодостаточная реализация Tree-structured Parzen Estimator (TPE)
с ИЗОЛИРОВАННЫМИ переключателями модификаций (по одному фактору на флаг).

Зачем своя реализация, а не repo-`tpe`:
- Все варианты используют ОДИН и тот же базовый код -> сравнение "baseline vs модификация"
  меняет ровно один фактор (корректный ablation). В исходных ноутбуках gTPE был отдельной
  реализацией, а w(x) применялся к среднему координат — сравнения были спутаны.
- Зависимости только numpy/scipy -> воспроизводится где угодно (без ConfigSpace/Drive).

Базовый TPE (Bergstra et al., 2011):
  1) первые n_init точек — равномерно случайно;
  2) делим наблюдения по порогу gamma на "хорошие" (good, l) и "плохие" (bad, g);
  3) строим по каждому измерению взвешенные KDE l(x) и g(x);
  4) генерируем кандидатов из l(x) и выбираем максимизирующего l(x)/g(x).

ФЛАГИ-МОДИФИКАЦИИ (каждый — отдельный эксперимент):
  - gradient_weight: веса наблюдений в KDE = 1/(||∇f(x)||+eps)^p. Использует ИСТИННЫЙ
    градиент в РЕАЛЬНОЙ точке наблюдения (исправление дефекта исходного метода 2).
  - gp_rerank: TPE предлагает кандидатов, простой GP пере-ранжирует их по mean/variance.
Нормализация objective — отдельный фактор и задаётся снаружи (см. objective.py), т.к. это
свойство задачи, а не сэмплера.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Sequence, Tuple

import numpy as np
from scipy.special import logsumexp

Array = np.ndarray
ObjectiveFn = Callable[[Array], Tuple[float, Array]]   # x -> (value, grad)


# --------------------------------------------------------------------------- #
# 1D взвешенный ядерный оценщик плотности (гауссово ядро, Скоттова ширина)
# --------------------------------------------------------------------------- #
class WeightedKDE1D:
    """Гауссова смесь по наблюдениям + ШИРОКАЯ prior-компонента.

    Prior (как `consider_prior` в Optuna/Bergstra) — отдельный широкий гауссиан в центре
    области. Без него «хорошая» плотность схлопывается в моду, TPE перестаёт исследовать
    и застревает. С prior сохраняется исследование, и алгоритм спускается к оптимуму.

    Представление: набор компонент (центры, ширины, веса), смешиваемых через logsumexp.
    """
    def __init__(self, samples: Array, lo: float, hi: float,
                 weights: Optional[Array] = None, min_bw_frac: float = 1e-2,
                 prior_weight: float = 1.0):
        samples = np.asarray(samples, dtype=float).ravel()
        self.lo, self.hi = float(lo), float(hi)
        span = max(hi - lo, 1e-12)

        n = samples.size
        if weights is None:
            w = np.ones(n)
        else:
            w = np.clip(np.asarray(weights, dtype=float).ravel(), 1e-12, np.inf)

        # Компоненты смеси = наблюдения + prior (широкий гауссиан в центре области).
        mid = 0.5 * (lo + hi)
        self.centers = np.append(samples, mid)
        comp_w = np.append(w, prior_weight)
        self.weights = comp_w / comp_w.sum()

        # АДАПТИВНАЯ ширина ядра (Bergstra "magic clip"): для каждого центра ширина =
        # max(расстояние до левого, до правого соседа) в отсортированном ряду центров.
        # Это даёт узкие ядра в плотных (хороших) областях и широкие в разреженных -> спуск.
        order = np.argsort(self.centers)
        c = self.centers[order]
        k = c.size
        sig = np.empty(k)
        for i in range(k):
            left = c[i] - c[i - 1] if i > 0 else c[i] - lo
            right = c[i + 1] - c[i] if i < k - 1 else hi - c[i]
            sig[i] = max(left, right)
        bws = np.empty(k)
        bws[order] = sig
        bws[n] = span                                  # prior-компонента всегда широкая
        self.bws = np.clip(bws, min_bw_frac * span, span)
        self.bw = float(np.median(self.bws[:n])) if n else span   # для справки
        # лог-веса с полом, чтобы не ловить log(0) при нулевом весе компоненты
        self.log_weights = np.log(np.where(self.weights > 0, self.weights, 1e-300))

    def _log_components(self, xs: Array) -> Array:
        z = (xs[:, None] - self.centers[None, :]) / self.bws[None, :]   # (m, k)
        return -0.5 * z ** 2 - np.log(self.bws)[None, :] - 0.5 * math.log(2 * math.pi)

    def logpdf_many(self, xs: Array) -> Array:
        xs = np.asarray(xs, dtype=float)
        out = logsumexp(self.log_weights[None, :] + self._log_components(xs), axis=1)
        out[(xs < self.lo) | (xs > self.hi)] = -np.inf
        return out

    def logpdf(self, x: float) -> float:
        if x < self.lo or x > self.hi:
            return -np.inf
        return float(self.logpdf_many(np.array([x]))[0])

    def sample_many(self, rng: np.random.Generator, n: int) -> Array:
        """Выборка n точек из смеси (включая prior-компоненту)."""
        idx = rng.choice(self.centers.size, size=n, p=self.weights)
        xs = self.centers[idx] + rng.normal(0.0, 1.0, size=n) * self.bws[idx]
        return np.clip(xs, self.lo, self.hi)

    def sample(self, rng: np.random.Generator) -> float:
        return float(self.sample_many(rng, 1)[0])


def _uniform_logpdf(x: float, lo: float, hi: float) -> float:
    return -np.inf if (x < lo or x > hi) else -math.log(max(hi - lo, 1e-12))


# --------------------------------------------------------------------------- #
# Простейший GP (RBF) для пере-ранжирования кандидатов (только для gp_rerank)
# --------------------------------------------------------------------------- #
class SimpleGP:
    """Мини-GP с нормализацией X/Y и медианной длиной корреляции. Только для re-ranking."""
    def __init__(self, noise: float = 1e-6):
        self.noise = noise
        self.fitted = False

    def fit(self, X: Array, y: Array) -> "SimpleGP":
        X = np.asarray(X, dtype=float); y = np.asarray(y, dtype=float).ravel()
        if X.shape[0] < 2:
            self.fitted = False
            return self
        self.x_min = X.min(0); rng = X.max(0) - self.x_min
        self.x_range = np.where(rng > 1e-12, rng, 1.0)
        Xn = (X - self.x_min) / self.x_range
        self.y_mean = float(y.mean()); self.y_std = float(y.std()) or 1.0
        yn = (y - self.y_mean) / self.y_std
        iu, ju = np.triu_indices(Xn.shape[0], k=1)
        d = np.sqrt(((Xn[iu] - Xn[ju]) ** 2).sum(1)) if len(iu) else np.array([1.0])
        self.ls = max(float(np.median(d)) if d.size else 1.0, 1e-6)
        self.Xn = Xn
        K = self._k(Xn, Xn) + (self.noise + 1e-12) * np.eye(Xn.shape[0])
        try:
            self.L = np.linalg.cholesky(K)
            self.alpha = np.linalg.solve(self.L.T, np.linalg.solve(self.L, yn))
            self._pinv = None
        except np.linalg.LinAlgError:
            self._pinv = np.linalg.pinv(K); self.alpha = self._pinv @ yn; self.L = None
        self.fitted = True
        return self

    def _k(self, A: Array, B: Array) -> Array:
        sq = ((A[:, None, :] - B[None, :, :]) ** 2).sum(2)
        return np.exp(-0.5 * sq / self.ls ** 2)

    def predict(self, x: Array) -> Tuple[float, float]:
        if not self.fitted:
            return 0.0, 1.0
        xn = ((np.asarray(x, float) - self.x_min) / self.x_range).reshape(1, -1)
        k = self._k(self.Xn, xn)[:, 0]
        mu = float(k @ self.alpha)
        if self.L is not None:
            v = np.linalg.solve(self.L, k); var = float(max(1.0 - v @ v, 1e-10))
        else:
            var = float(max(1.0 - k @ self._pinv @ k, 1e-10))
        return self.y_mean + self.y_std * mu, (self.y_std ** 2) * var


# --------------------------------------------------------------------------- #
# Сам TPE
# --------------------------------------------------------------------------- #
@dataclass
class TPE:
    bounds: Sequence[Tuple[float, float]]
    n_init: int = 10
    gamma: float = 0.2                 # доля "хороших" наблюдений
    n_candidates: int = 24             # кандидатов на одну итерацию (n_ei_candidates)
    min_bw_frac: float = 1e-2
    seed: Optional[int] = None
    # --- флаги-модификации (по одному фактору) ---
    # weight_shape: форма градиентного веса w(x) для наблюдений KDE «хорошей» группы.
    #   None         — без веса (базовый TPE);
    #   "smooth"     — w растёт с ‖∇f‖ (tanh): предпочтение точкам с БОЛЬШИМ градиентом;
    #   "smooth_inv" — w растёт при МАЛОМ ‖∇f‖ (−tanh): предпочтение «плоским»/стационарным;
    #   "sign"       — резкая версия smooth (сигмоида·5);
    #   "sign_inv"   — резкая версия smooth_inv.
    # Все формы дают w∈[0.8,1.2] (мягкая модификация), как в исходных ноутбуках,
    # но градиент берётся в РЕАЛЬНОЙ точке наблюдения (исправление дефекта оригинала).
    weight_shape: Optional[str] = None
    gp_rerank: bool = False
    gp_beta: float = 0.2
    # --- состояние ---
    history_x: List[Array] = field(default_factory=list)
    history_y: List[float] = field(default_factory=list)
    history_g: List[Array] = field(default_factory=list)

    def __post_init__(self):
        self.bounds = [(float(a), float(b)) for a, b in self.bounds]
        self.dim = len(self.bounds)
        self.rng = np.random.default_rng(self.seed)
        assert self.weight_shape in (None, "smooth", "smooth_inv", "sign", "sign_inv")
        if self.gp_rerank:
            self.gp = SimpleGP()

    # ---- публичный API ----
    def optimize(self, objective: ObjectiveFn, n_trials: int) -> dict:
        for _ in range(n_trials):
            x = self._ask()
            value, grad = objective(x)
            self.history_x.append(np.asarray(x, float))
            self.history_y.append(float(value))
            self.history_g.append(np.asarray(grad, float))
        best_i = int(np.argmin(self.history_y))
        return {
            "x_history": np.array(self.history_x),
            "y_history": np.array(self.history_y),
            "best_x": self.history_x[best_i],
            "best_y": self.history_y[best_i],
        }

    # ---- внутреннее ----
    def _ask(self) -> Array:
        if len(self.history_y) < self.n_init:
            return self._sample_uniform()
        return self._sample_tpe()

    def _sample_uniform(self) -> Array:
        return np.array([self.rng.uniform(lo, hi) for lo, hi in self.bounds])

    def _split(self) -> Tuple[List[int], List[int]]:
        y = np.array(self.history_y)
        n_good = max(1, int(math.ceil(self.gamma * len(y))))
        order = np.argsort(y)
        good, bad = order[:n_good].tolist(), order[n_good:].tolist()
        if not bad:                       # подстраховка
            bad = [good.pop()]
        return good, bad

    def _obs_weights(self, idx: List[int]) -> Optional[Array]:
        """Веса наблюдений «хорошей» группы для KDE. Без модификации -> None (равные веса).

        4 формы w(x) (как в исходных ноутбуках), но по ИСТИННОМУ ‖∇f‖ в РЕАЛЬНОЙ точке:
          1) нормируем нормы градиентов наблюдений в [-1,1] (z0);
          2) применяем форму z=shape(z0);
          3) w = clip(1 + 0.2*z, 0.8, 1.2)  — мягкая модификация базового l(x)/g(x).
        smooth/sign дают больший вес большому градиенту; *_inv — малому градиенту.
        """
        if self.weight_shape is None:
            return None
        norms = np.array([np.linalg.norm(self.history_g[i]) for i in idx], dtype=float)
        v_min, v_max = float(norms.min()), float(norms.max())
        if (v_max - v_min) <= 1e-12:
            z0 = np.zeros_like(norms)                      # все градиенты равны -> нейтрально
        else:
            z0 = 2.0 * (norms - v_min) / (v_max - v_min) - 1.0
        if self.weight_shape == "smooth":
            z = np.tanh(z0)
        elif self.weight_shape == "smooth_inv":
            z = -np.tanh(z0)
        elif self.weight_shape == "sign":
            z = 2.0 / (1.0 + np.exp(-np.clip(5.0 * z0, -500, 500))) - 1.0
        elif self.weight_shape == "sign_inv":
            z = -(2.0 / (1.0 + np.exp(-np.clip(5.0 * z0, -500, 500))) - 1.0)
        return np.clip(1.0 + 0.2 * z, 0.8, 1.2)

    def _fit_kdes(self, idx: List[int], weights: Optional[Array]) -> List[WeightedKDE1D]:
        return [
            WeightedKDE1D(
                samples=np.array([self.history_x[i][d] for i in idx]),
                lo=self.bounds[d][0], hi=self.bounds[d][1],
                weights=weights, min_bw_frac=self.min_bw_frac,
            )
            for d in range(self.dim)
        ]

    def _sample_tpe(self) -> Array:
        good, bad = self._split()
        l_models = self._fit_kdes(good, self._obs_weights(good))   # хорошие (с весами)
        g_models = self._fit_kdes(bad, None)                       # плохие (равные веса)

        if self.gp_rerank:
            self.gp.fit(np.array(self.history_x), np.array(self.history_y))

        # Кандидаты сэмплируем из l(x) и оцениваем ВЕКТОРИЗОВАННО (быстро).
        cand = np.column_stack([l_models[d].sample_many(self.rng, self.n_candidates)
                                for d in range(self.dim)])           # (n_cand, dim)
        logl = sum(l_models[d].logpdf_many(cand[:, d]) for d in range(self.dim))
        logg = sum(g_models[d].logpdf_many(cand[:, d]) for d in range(self.dim))
        score = logl - logg                                          # = log l(x)/g(x)

        if self.gp_rerank:
            for i in range(self.n_candidates):
                mu, var = self.gp.predict(cand[i])
                score[i] += -mu + self.gp_beta * math.sqrt(max(var, 1e-12))

        best_i = int(np.argmax(score))
        x = cand[best_i]
        return x if np.all(np.isfinite(x)) else self._sample_uniform()
