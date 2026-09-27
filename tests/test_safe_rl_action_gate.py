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
        self.assertEqual(result.selected.name, "brake")

    def test_blocks_when_no_safe_option(self):
        result = self.gate.choose(
            State(9.9, 3),
            Action(2),
            [Action(1), Action(0.5)],
        )
        self.assertEqual(result.decision, GateDecision.BLOCK)
        self.assertIsNone(result.selected)


if __name__ == "__main__":
    unittest.main()
