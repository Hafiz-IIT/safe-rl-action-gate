# Safe RL Action Gate

> Runtime safety shield for sequential decision systems that allows, substitutes or blocks proposed actions against explicit constraints.

## Status
**Reproducible research prototype.** Executable Python, deterministic tests, and GitHub Actions CI are included. No production-deployment claim is made.

## Problem
A learned policy may propose an action that is locally high-reward but unsafe. This project separates policy generation from action authorization.

## Architecture
Policy proposal → transition prediction → constraint checks → minimal-intervention safe substitution → BLOCK when no safe alternative exists.

## Quick start
```bash
python -m unittest discover -s tests -v
python safe_rl_action_gate.py
```

## Implemented
- Explicit state/action model
- Configurable safety constraints
- One-step transition model
- ALLOW / SUBSTITUTE / BLOCK outcomes
- Minimal-intervention alternative choice
- Deterministic tests and CI

## Evaluation
The prototype measures constraint violations prevented, intervention frequency, fallback availability, and the performance cost of shielding.

## Research lineage
- *Control Barrier Functions with Linear Model Residuals for Safe Robot Automation*
- *Hybrid Control Architectures: Merging LQR and Deep RL for Robust Robot Autonomy*
- *Towards Interpretable RL for Robotics through Linear Statistical Modeling*

## Structure
- `safe_rl_action_gate.py` — executable core
- `tests/` — regression tests
- `docs/ARCHITECTURE.md`
- `docs/RESEARCH_CONTEXT.md`
- `docs/EVALUATION.md`
- `ROADMAP.md`
- `CITATION.cff`
- `.github/workflows/tests.yml`

## Limitations
- One-step deterministic transition model
- No formal CBF guarantee yet
- No trained RL policy bundled
- No continuous optimization layer

## License
MIT.

## Control research lab

The repository now also contains `control_lab/` with:
- scalar discrete LQR;
- residual-controller composition;
- a transparent Koopman-inspired polynomial lift;
- Bayesian scalar dynamics uncertainty;
- a model-mismatch benchmark.

Research protocols are staged under `research/` for residual RL, Koopman embeddings, Bayesian safe RL, and hybrid LQR + learned residual control. These protocols are not publication claims.
