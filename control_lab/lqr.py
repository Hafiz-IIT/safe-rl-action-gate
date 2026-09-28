from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Trajectory:
    states: tuple[float, ...]
    actions: tuple[float, ...]
    total_cost: float


def scalar_lqr_gain(
    a: float,
    b: float,
    q: float = 1.0,
    r: float = 0.1,
    *,
    iterations: int = 500,
    tolerance: float = 1e-12,
) -> float:
    """Solve the scalar discrete-time algebraic Riccati equation by iteration.

    Dynamics: x[t+1] = a*x[t] + b*u[t]
    Cost: sum(q*x^2 + r*u^2)

    Returns K for the controller u = -K*x.
    """
    if q < 0 or r <= 0:
        raise ValueError("q must be non-negative and r must be positive")
    if b == 0:
        raise ValueError("b must be non-zero for controllability in this scalar model")

    p = max(q, 1e-12)
    for _ in range(iterations):
        denom = r + (b * b * p)
        next_p = q + (a * a * p) - ((a * b * p) ** 2) / denom
        if abs(next_p - p) <= tolerance:
            p = next_p
            break
        p = next_p

    return (b * p * a) / (r + b * b * p)


def simulate_scalar(
    *,
    a: float,
    b: float,
    x0: float,
    controller: Callable[[float, int], float],
    steps: int,
    q: float = 1.0,
    r: float = 0.1,
    disturbance: Callable[[int], float] | None = None,
) -> Trajectory:
    if steps < 1:
        raise ValueError("steps must be >= 1")

    x = float(x0)
    states = [x]
    actions: list[float] = []
    total_cost = 0.0

    for t in range(steps):
        u = float(controller(x, t))
        total_cost += q * x * x + r * u * u
        w = 0.0 if disturbance is None else float(disturbance(t))
        x = a * x + b * u + w
        actions.append(u)
        states.append(x)

    return Trajectory(tuple(states), tuple(actions), total_cost)
