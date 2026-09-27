# Safe RL Action Gate

A transparent runtime action-gating prototype for sequential decision systems.

The gate sits between a policy and the environment and can **ALLOW, SUBSTITUTE, or BLOCK** an action when a predicted transition violates configured safety constraints.

## Implemented

- state/action abstractions
- configurable safety constraints
- candidate-action evaluation
- safe substitution when the requested action is unsafe
- explicit blocked state when no safe action exists
- audit-friendly decision object
- deterministic unit tests

## Quick start

```bash
python -m unittest discover -s tests -v
python safe_rl_action_gate.py
```

## Scope

This is a small research prototype for runtime shielding concepts. It is not a trained reinforcement-learning policy and does not claim formal control-barrier guarantees.
