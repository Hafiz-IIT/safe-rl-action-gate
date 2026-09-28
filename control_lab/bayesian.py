from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass
class BayesianScalarDynamics:
    """Bayesian estimator for an uncertain scalar state coefficient.

    Model:
        x_next = a*x + known_b*u + noise
        noise ~ N(0, noise_variance)

    Prior:
        a ~ N(prior_mean, prior_variance)
    """

    known_b: float
    noise_variance: float
    mean: float = 1.0
    variance: float = 1.0

    def __post_init__(self) -> None:
        if self.noise_variance <= 0:
            raise ValueError("noise_variance must be positive")
        if self.variance <= 0:
            raise ValueError("prior variance must be positive")

    def update(self, *, x: float, u: float, x_next: float) -> None:
        precision_prior = 1.0 / self.variance
        precision_obs = (x * x) / self.noise_variance
        target = x_next - self.known_b * u

        posterior_variance = 1.0 / (precision_prior + precision_obs)
        posterior_mean = posterior_variance * (
            precision_prior * self.mean
            + (x * target) / self.noise_variance
        )

        self.mean = posterior_mean
        self.variance = posterior_variance

    @property
    def std(self) -> float:
        return sqrt(self.variance)

    def predict(self, *, x: float, u: float) -> tuple[float, float]:
        mean_next = self.mean * x + self.known_b * u
        epistemic_variance = (x * x) * self.variance
        total_variance = epistemic_variance + self.noise_variance
        return mean_next, sqrt(total_variance)
