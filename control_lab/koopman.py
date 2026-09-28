from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PolynomialLiftModel:
    """Koopman-inspired scalar lifted predictor.

    Predicts x_next = w0*x + w1*x^2 + w2*u.
    This is intentionally described as Koopman-inspired rather than a complete
    Koopman operator identification method.
    """

    w_x: float
    w_x2: float
    w_u: float

    def predict(self, x: float, u: float) -> float:
        return self.w_x * x + self.w_x2 * x * x + self.w_u * u


def _solve_3x3(matrix: list[list[float]], vector: list[float]) -> tuple[float, float, float]:
    aug = [row[:] + [vector[i]] for i, row in enumerate(matrix)]

    for col in range(3):
        pivot = max(range(col, 3), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-12:
            raise ValueError("singular design matrix")
        aug[col], aug[pivot] = aug[pivot], aug[col]

        scale = aug[col][col]
        aug[col] = [v / scale for v in aug[col]]

        for row in range(3):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [
                aug[row][j] - factor * aug[col][j]
                for j in range(4)
            ]

    return aug[0][3], aug[1][3], aug[2][3]


def fit_polynomial_lift(
    samples: list[tuple[float, float, float]],
    *,
    ridge: float = 1e-8,
) -> PolynomialLiftModel:
    """Fit a simple lifted linear predictor from (x, u, x_next) samples."""
    if len(samples) < 3:
        raise ValueError("at least three samples are required")
    if ridge < 0:
        raise ValueError("ridge must be non-negative")

    gram = [[0.0] * 3 for _ in range(3)]
    rhs = [0.0] * 3

    for x, u, y in samples:
        phi = [float(x), float(x) ** 2, float(u)]
        for i in range(3):
            rhs[i] += phi[i] * float(y)
            for j in range(3):
                gram[i][j] += phi[i] * phi[j]

    for i in range(3):
        gram[i][i] += ridge

    w0, w1, w2 = _solve_3x3(gram, rhs)
    return PolynomialLiftModel(w0, w1, w2)
