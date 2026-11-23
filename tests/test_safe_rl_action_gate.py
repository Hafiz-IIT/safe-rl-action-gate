import math
import unittest

from safe_rl_action_gate import (
    Action,
    ActionGate,
    GateDecision,
    State,
    bounded_constraints,
    step,
)


class ActionGateTests(unittest.TestCase):
    def setUp(self):
        self.gate = ActionGate(
            bounded_constraints(min_position=0, max_position=10, max_abs_velocity=3)
        )

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

    def test_non_finite_state_and_action_are_rejected(self):
        for value in (math.nan, math.inf, -math.inf):
            with self.subTest(value=value), self.assertRaises(ValueError):
                State(value, 0)
            with self.subTest(value=value), self.assertRaises(ValueError):
                Action(value)

    def test_invalid_dt_and_overflow_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "greater than zero"):
            step(State(0, 0), Action(0), dt=0)
        gate = ActionGate({"finite": lambda state: True}, dt=1e308)
        result = gate.choose(State(1e308, 1e308), Action(1e308))
        self.assertEqual(result.decision, GateDecision.BLOCK)
        self.assertIn("invalid_state_action_or_transition", result.violations)

    def test_constraint_exception_and_non_boolean_result_fail_closed(self):
        broken = ActionGate({
            "raises": lambda state: 1 / 0,
            "not_boolean": lambda state: 1,
        })
        result = broken.choose(State(0, 0), Action(0))
        self.assertEqual(result.decision, GateDecision.BLOCK)
        self.assertIn("constraint_evaluation_error:raises", result.violations)
        self.assertIn("constraint_non_boolean_result:not_boolean", result.violations)

    def test_invalid_constraint_configuration_rejected(self):
        with self.assertRaisesRegex(ValueError, "non-empty mapping"):
            ActionGate({})
        with self.assertRaisesRegex(TypeError, "callable"):
            ActionGate({"bad": True})
        with self.assertRaisesRegex(ValueError, "cannot exceed"):
            bounded_constraints(min_position=2, max_position=1, max_abs_velocity=3)
        with self.assertRaisesRegex(ValueError, "non-negative"):
            bounded_constraints(min_position=0, max_position=1, max_abs_velocity=-1)

    def test_substitution_tie_break_is_independent_of_input_order(self):
        alternatives = [Action(0, "z-hold"), Action(0, "a-hold")]
        first = self.gate.choose(State(9, 1), Action(2), alternatives)
        second = self.gate.choose(State(9, 1), Action(2), list(reversed(alternatives)))
        self.assertEqual(first.selected.name, "a-hold")
        self.assertEqual(second.selected.name, "a-hold")

    def test_invalid_alternative_types_rejected(self):
        with self.assertRaisesRegex(TypeError, "only Action"):
            self.gate.choose(State(2, 0), Action(0), [object()])


if __name__ == "__main__":
    unittest.main()
