import unittest

from safe_rl_action_gate import (
    Action,
    ActionGate,
    GateDecision,
    State,
    bounded_constraints,
)


class ActionGateTests(unittest.TestCase):
    def setUp(self):
        self.gate = ActionGate(
            bounded_constraints(min_position=0, max_position=10, max_abs_velocity=3)
        )

    def test_empty_constraint_set_is_rejected(self):
        with self.assertRaises(ValueError):
            ActionGate({})

    def test_invalid_numeric_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            State(float("nan"), 0)
        with self.assertRaises(ValueError):
            Action(1, "")
        with self.assertRaises(ValueError):
            ActionGate(bounded_constraints(min_position=0, max_position=10, max_abs_velocity=3), dt=0)

    def test_constraint_exception_fails_closed(self):
        gate = ActionGate({"sensor": lambda state: (_ for _ in ()).throw(RuntimeError("sensor failure"))})
        result = gate.choose(State(1, 0), Action(0))
        self.assertEqual(result.decision, GateDecision.BLOCK)

    def test_simulation_overflow_fails_closed(self):
        gate = ActionGate({"position": lambda state: state.position < 10})
        result = gate.choose(State(1e308, 1e308), Action(1e308))
        self.assertEqual(result.decision, GateDecision.BLOCK)
        self.assertIn("simulation_error", result.violations)

    def test_safe_action_allowed(self):
        result = self.gate.choose(State(2, 0), Action(1))
        self.assertEqual(result.decision, GateDecision.ALLOW)

    def test_unsafe_action_substituted(self):
        result = self.gate.choose(
            State(9, 1),
            Action(2, "unsafe"),
            [Action(0, "hold"), Action(-1, "brake")],
        )
        self.assertEqual(result.decision, GateDecision.SUBSTITUTE)
        self.assertEqual(result.selected.name, "hold")

    def test_blocks_when_no_safe_option(self):
        result = self.gate.choose(
            State(9.9, 3),
            Action(2),
            [Action(1), Action(0.5)],
        )
        self.assertEqual(result.decision, GateDecision.BLOCK)
        self.assertIsNone(result.selected)

    def test_non_positive_or_non_finite_dt_is_rejected(self):
        for dt in (0, -1, float("nan"), float("inf")):
            with self.subTest(dt=dt):
                with self.assertRaises(ValueError):
                    ActionGate({}, dt=dt)

    def test_non_finite_state_and_action_are_rejected(self):
        with self.assertRaises(ValueError):
            State(float("nan"), 0)
        with self.assertRaises(ValueError):
            Action(float("inf"))

    def test_invalid_bounds_are_rejected(self):
        with self.assertRaises(ValueError):
            bounded_constraints(min_position=5, max_position=1, max_abs_velocity=3)
        with self.assertRaises(ValueError):
            bounded_constraints(min_position=0, max_position=10, max_abs_velocity=float("inf"))


if __name__ == "__main__":
    unittest.main()
