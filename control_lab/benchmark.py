from __future__ import annotations

from dataclasses import asdict

from .lqr import scalar_lqr_gain, simulate_scalar
from .residual import residual_controller


def run_model_mismatch_benchmark(
    *,
    design_a: float = 1.0,
    true_a: float = 1.15,
    b: float = 1.0,
    x0: float = 2.0,
    steps: int = 30,
) -> dict:
    """Compare an LQR baseline with a simple residual correction under mismatch.

    The residual is a deterministic heuristic used to exercise the architecture.
    It must not be described as a trained RL policy.
    """
    gain = scalar_lqr_gain(design_a, b, q=1.0, r=0.1)

    base = simulate_scalar(
        a=true_a,
        b=b,
        x0=x0,
        controller=lambda x, t: -gain * x,
        steps=steps,
    )

    residual = residual_controller(
        base_gain=gain,
        residual_policy=lambda x, t: -0.10 * x,
        residual_scale=1.0,
    )
    hybrid = simulate_scalar(
        a=true_a,
        b=b,
        x0=x0,
        controller=residual,
        steps=steps,
    )

    return {
        "design_a": design_a,
        "true_a": true_a,
        "gain": gain,
        "base_total_cost": base.total_cost,
        "hybrid_total_cost": hybrid.total_cost,
        "base_final_abs_state": abs(base.states[-1]),
        "hybrid_final_abs_state": abs(hybrid.states[-1]),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_model_mismatch_benchmark(), indent=2))
