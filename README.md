# Safe RL Action Gate

> **A transparent runtime shield that can allow, substitute, or block an action before it reaches the environment.**

A learned or heuristic policy can propose an action that violates known state constraints. This repository studies a minimal-intervention gate between policy output and environment transition.

## What is implemented

- state and action abstractions
- deterministic transition model
- configurable state-safety constraints
- candidate-action violation checking
- minimal-intervention safe substitution
- explicit BLOCK when no safe alternative exists
- audit-friendly gate result

## Repository map

| Path | Purpose |
|---|---|
| `safe_rl_action_gate.py` | Core implementation |
| `tests/` | Deterministic unit tests |
| `examples/` | Reproducible synthetic/example input |
| `docs/architecture.md` | System architecture and decision flow |
| `docs/research-agenda.md` | Questions, experiments, and publication lineage |
| `STATUS.md` | Implemented vs. research-stage claims |
| `CITATION.cff` | Software citation metadata |
| `NOTICE.md` | Scope and use notice |

## Quick start

```bash
python -m unittest discover -s tests -v
python safe_rl_action_gate.py
```

The current prototype uses only the Python standard library unless the implementation itself states otherwise.

## Architecture in one line

**policy action → predict transition → constraint checks → safe alternatives → minimal intervention → ALLOW / SUBSTITUTE / BLOCK**

## Research lineage

This repository is the executable seed for the historical robotics/control research program combining linear models, classical control, and reinforcement learning.

Historical paper titles are preserved as **research directions**, not represented as published papers unless a DOI/preprint record is later added.

## Evaluation plan

Evaluate requested-action intervention rate, constraint violations prevented, unnecessary substitutions, and task degradation under increasingly aggressive policies and model mismatch.

## Current status

**Maturity: reproducible research prototype.** This is not a trained RL policy, not a formal control-barrier-function implementation, and not a proof of closed-loop safety.

See `STATUS.md` and `docs/research-agenda.md` for the exact claims boundary and next empirical steps.
