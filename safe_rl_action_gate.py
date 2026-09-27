from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Iterable, Sequence


class GateDecision(str, Enum):
    ALLOW = "ALLOW"
    SUBSTITUTE = "SUBSTITUTE"
    BLOCK = "BLOCK"


@dataclass(frozen=True)
class State:
    position: float
    velocity: float


@dataclass(frozen=True)
class Action:
    acceleration: float
    name: str = "candidate"


@dataclass(frozen=True)
class GateResult:
    decision: GateDecision
    requested: Action
    selected: Action | None
    violations: tuple[str, ...]


Constraint = Callable[[State], bool]


def step(state: State, action: Action, dt: float = 1.0) -> State:
    velocity = state.velocity + action.acceleration * dt
    position = state.position + velocity * dt
    return State(position=position, velocity=velocity)


class ActionGate:
    def __init__(self, constraints: dict[str, Constraint], dt: float = 1.0):
        self.constraints = dict(constraints)
        self.dt = dt

    def violations(self, state: State, action: Action) -> tuple[str, ...]:
        next_state = step(state, action, self.dt)
        return tuple(
            name for name, predicate in self.constraints.items()
            if not predicate(next_state)
        )

    def choose(
        self,
        state: State,
        requested: Action,
        alternatives: Sequence[Action] = (),
    ) -> GateResult:
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
