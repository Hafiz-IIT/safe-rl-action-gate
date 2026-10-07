# Safe RL Action Gate

<p align="center">
  <strong>Action Authorization for Sequential Decision Systems</strong><br/>
  <sub>Separate policy generation from safety-critical action authorization.</sub>
</p>

<p align="center">
  <a href="https://github.com/Hafiz-IIT/safe-rl-action-gate/actions"><img src="https://img.shields.io/github/actions/workflow/status/Hafiz-IIT/safe-rl-action-gate/ci.yml?label=CI" alt="CI"/></a>
  <img src="https://img.shields.io/badge/status-research%20prototype-blue" alt="Research prototype"/>
  <img src="https://img.shields.io/badge/domain-safe%20RL-purple" alt="Safe RL"/>
</p>

## Research question

**What should happen when a learned policy proposes an action that violates an explicit safety constraint?**

Instead of silently modifying policy behavior, the gate makes the authorization decision inspectable:

```
Policy proposal
     ↓
Transition prediction
     ↓
Constraint evaluation
     ├── ALLOW
     ├── SUBSTITUTE
     └── BLOCK
```

## Try it

```bash
python safe_rl_action_gate.py
python -m unittest discover -s tests -v
```

The `control_lab/` extension explores linear LQR priors, residual controllers, a transparent Koopman-inspired lift and Bayesian scalar dynamics uncertainty.

## Implemented

- explicit state/action model
- configurable safety constraints
- one-step transition model
- safe-action substitution
- blocking when no admissible alternative exists
- control/research extensions
- deterministic tests + CI

## Why this is interesting

The project treats **action authorization as a separate system boundary**. That makes it possible to study safety mechanisms without pretending the learned policy itself is reliable.

## Research boundary

The control and RL components are research prototypes. They are not claims of certified safety, real-world robotic deployment or performance superiority.

Related work: [Agent Evidence Probes](https://github.com/Hafiz-IIT/agent-evidence-probes) · [Memory Governor](https://github.com/Hafiz-IIT/memory-governor)
