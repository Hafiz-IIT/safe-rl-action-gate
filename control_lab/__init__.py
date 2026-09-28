"""Transparent control/research baselines used by the safe-RL experiments."""

from .lqr import scalar_lqr_gain, simulate_scalar
from .residual import residual_controller
from .koopman import fit_polynomial_lift
from .bayesian import BayesianScalarDynamics

__all__ = [
    "scalar_lqr_gain",
    "simulate_scalar",
    "residual_controller",
    "fit_polynomial_lift",
    "BayesianScalarDynamics",
]
