from __future__ import annotations

from typing import Callable


def residual_controller(
    *,
    base_gain: float,
    residual_policy: Callable[[float, int], float],
    residual_scale: float = 1.0,
    action_limit: float | None = None,
):
    """Compose a linear feedback controller with a bounded residual policy.

    u = -K*x + scale*delta_u

    This is a controller-composition primitive, not a trained RL algorithm.
    """

    if residual_scale < 0:
        raise ValueError("residual_scale must be non-negative")
    if action_limit is not None and action_limit <= 0:
        raise ValueError("action_limit must be positive")

    def controller(x: float, t: int) -> float:
        u = -base_gain * x + residual_scale * float(residual_policy(x, t))
        if action_limit is not None:
            u = max(-action_limit, min(action_limit, u))
        return u

    return controller
