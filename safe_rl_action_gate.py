from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import math
from typing import Callable, Mapping, Sequence


class GateDecision(str, Enum):
    ALLOW = "ALLOW"
    SUBSTITUTE = "SUBSTITUTE"
    BLOCK = "BLOCK"


def _finite_number(value, field: str) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{field} must be a finite number")


@dataclass(frozen=True)
class State:
    position: float
    velocity: float

    def __post_init__(self):
        _finite_number(self.position, "position")
        _finite_number(self.velocity, "velocity")


@dataclass(frozen=True)
class Action:
    acceleration: float
    name: str = "candidate"

    def __post_init__(self):
        _finite_number(self.acceleration, "acceleration")
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
        raise TypeError("state and action must be validated State and Action instances")
    _finite_number(dt, "dt")
    if dt <= 0:
        raise ValueError("dt must be greater than zero")
    velocity = state.velocity + action.acceleration * dt
    position = state.position + velocity * dt
    _finite_number(velocity, "predicted velocity")
    _finite_number(position, "predicted position")
    return State(position=position, velocity=velocity)


class ActionGate:
    def __init__(self, constraints: Mapping[str, Constraint], dt: float = 1.0):
        if not isinstance(constraints, Mapping) or not constraints:
            raise ValueError("constraints must be a non-empty mapping")
        for name, predicate in constraints.items():
            if not isinstance(name, str) or not name.strip():
                raise ValueError("constraint names must be non-empty strings")
            if not callable(predicate):
                raise TypeError(f"constraint {name} must be callable")
        _finite_number(dt, "dt")
        if dt <= 0:
            raise ValueError("dt must be greater than zero")
        self.constraints = dict(constraints)
        self.dt = dt

    def violations(self, state: State, action: Action) -> tuple[str, ...]:
        try:
            next_state = step(state, action, self.dt)
        except (TypeError, ValueError, OverflowError):
            return ("invalid_state_action_or_transition",)

        violations = []
        for name, predicate in self.constraints.items():
            try:
                result = predicate(next_state)
            except Exception:
                violations.append(f"constraint_evaluation_error:{name}")
                continue
            if type(result) is not bool:
                violations.append(f"constraint_non_boolean_result:{name}")
            elif not result:
                violations.append(name)
        return tuple(violations)

    def choose(
        self,
        state: State,
        requested: Action,
        alternatives: Sequence[Action] = (),
    ) -> GateResult:
        if not isinstance(alternatives, Sequence) or isinstance(alternatives, (str, bytes)):
            raise TypeError("alternatives must be a sequence of Action instances")
        if any(not isinstance(action, Action) for action in alternatives):
            raise TypeError("alternatives must contain only Action instances")

        requested_violations = self.violations(state, requested)
        if not requested_violations:
            return GateResult(GateDecision.ALLOW, requested, requested, ())

        safe_alternatives = [
            action for action in alternatives
            if not self.violations(state, action)
        ]
        if safe_alternatives:
            selected = min(
                safe_alternatives,
                key=lambda action: (
                    abs(action.acceleration - requested.acceleration),
                    action.name,
                    action.acceleration,
                ),
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
    for name, value in (
        ("min_position", min_position),
        ("max_position", max_position),
        ("max_abs_velocity", max_abs_velocity),
    ):
        _finite_number(value, name)
    if min_position > max_position:
        raise ValueError("min_position cannot exceed max_position")
    if max_abs_velocity < 0:
        raise ValueError("max_abs_velocity must be non-negative")
    return {
        "position_lower_bound": lambda state: state.position >= min_position,
        "position_upper_bound": lambda state: state.position <= max_position,
        "velocity_bound": lambda state: abs(state.velocity) <= max_abs_velocity,
    }


if __name__ == "__main__":
    gate = ActionGate(
        bounded_constraints(min_position=0, max_position=10, max_abs_velocity=3)
    )
    state = State(position=9, velocity=1)
    requested = Action(acceleration=2, name="speed-up")
    alternatives = [Action(0, "hold"), Action(-1, "brake")]
    print(gate.choose(state, requested, alternatives))
