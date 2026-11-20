from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Sequence
import math


def _finite_number(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    return float(value)


class GateDecision(str, Enum):
    ALLOW = "ALLOW"
    SUBSTITUTE = "SUBSTITUTE"
    BLOCK = "BLOCK"


@dataclass(frozen=True)
class State:
    position: float
    velocity: float

    def __post_init__(self):
        _finite_number("position", self.position)
        _finite_number("velocity", self.velocity)


@dataclass(frozen=True)
class Action:
    acceleration: float
    name: str = "candidate"

    def __post_init__(self):
        _finite_number("acceleration", self.acceleration)
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("action name must be a non-empty string")


@dataclass(frozen=True)
class GateResult:
    decision: GateDecision
    requested: Action
    selected: Action | None
    violations: tuple[str, ...]


Constraint = Callable[[State], bool]


def step(state: State, action: Action, dt: float = 1.0) -> State:
    if not isinstance(state, State) or not isinstance(action, Action):
        raise TypeError("step requires State and Action values")
    dt = _finite_number("dt", dt)
    if dt <= 0:
        raise ValueError("dt must be positive")
    velocity = state.velocity + action.acceleration * dt
    position = state.position + velocity * dt
    return State(position=position, velocity=velocity)


class ActionGate:
    def __init__(self, constraints: dict[str, Constraint], dt: float = 1.0):
        dt = _finite_number("dt", dt)
        if dt <= 0:
            raise ValueError("dt must be positive")
        if not isinstance(constraints, dict) or not constraints or any(
            not isinstance(name, str) or not name.strip() or not callable(predicate)
            for name, predicate in constraints.items()
        ):
            raise ValueError("constraints must map non-empty names to callables")
        self.constraints = dict(constraints)
        self.dt = dt

    def violations(self, state: State, action: Action) -> tuple[str, ...]:
        try:
            next_state = step(state, action, self.dt)
        except (ArithmeticError, ValueError):
            return ("simulation_error",)
        violations = []
        for name, predicate in self.constraints.items():
            try:
                result = predicate(next_state)
            except Exception:
                violations.append(f"constraint_error:{name}")
                continue
            if not isinstance(result, bool) or not result:
                violations.append(name if isinstance(result, bool) else f"constraint_invalid:{name}")
        return tuple(violations)

    def choose(
        self,
        state: State,
        requested: Action,
        alternatives: Sequence[Action] = (),
    ) -> GateResult:
        if not isinstance(state, State) or not isinstance(requested, Action):
            raise TypeError("choose requires State and Action values")
        if not isinstance(alternatives, Sequence) or isinstance(alternatives, (str, bytes)):
            raise ValueError("alternatives must be a sequence of Action values")
        if any(not isinstance(action, Action) for action in alternatives):
            raise ValueError("alternatives must contain only Action values")
        requested_violations = self.violations(state, requested)
        if not requested_violations:
            return GateResult(GateDecision.ALLOW, requested, requested, ())

        safe_alternatives = [
            action for action in alternatives
            if not self.violations(state, action)
        ]
        if safe_alternatives:
            # Minimal intervention: choose closest acceleration to the requested action.
            selected = min(
                safe_alternatives,
                key=lambda a: abs(a.acceleration - requested.acceleration),
            )
            return GateResult(
                GateDecision.SUBSTITUTE,
                requested,
                selected,
                requested_violations,
            )

        return GateResult(
            GateDecision.BLOCK,
            requested,
            None,
            requested_violations,
        )


def bounded_constraints(
    *,
    min_position: float,
    max_position: float,
    max_abs_velocity: float,
) -> dict[str, Constraint]:
    min_position = _finite_number("min_position", min_position)
    max_position = _finite_number("max_position", max_position)
    max_abs_velocity = _finite_number("max_abs_velocity", max_abs_velocity)
    if min_position > max_position or max_abs_velocity < 0:
        raise ValueError("position bounds must be ordered and velocity bound non-negative")
    return {
        "position_lower_bound": lambda s: s.position >= min_position,
        "position_upper_bound": lambda s: s.position <= max_position,
        "velocity_bound": lambda s: abs(s.velocity) <= max_abs_velocity,
    }


if __name__ == "__main__":
    gate = ActionGate(
        bounded_constraints(min_position=0, max_position=10, max_abs_velocity=3)
    )
    state = State(position=9, velocity=1)
    requested = Action(acceleration=2, name="speed-up")
    alternatives = [Action(0, "hold"), Action(-1, "brake")]
    print(gate.choose(state, requested, alternatives))
