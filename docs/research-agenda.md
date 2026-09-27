# Research agenda

## Central question

**Can a simple, explicit runtime action gate reduce unsafe transitions while minimizing unnecessary intervention?**

## Hypotheses

### H1
A runtime constraint gate reduces violations relative to an unconstrained policy in controlled simulations.

### H2
Minimal-intervention substitution preserves more task utility than unconditional blocking.

### H3
Gate performance degrades under transition-model mismatch, motivating uncertainty-aware or robust extensions.

## Proposed experiments

1. Generate random policies in bounded 1-D/2-D environments and compare violation counts with and without the gate.
2. Compare ALLOW/SUBSTITUTE/BLOCK strategies under equivalent safety constraints.
3. Inject transition-model error and measure how rapidly the safety benefit collapses.

## Primary metrics

- constraint violation rate
- intervention rate
- unnecessary intervention rate
- task-cost increase
- blocked-state rate

## Historical paper lineage

- **Bayesian Linear Models as Priors for Safe Reinforcement Learning in Robotics**
- **Towards Interpretable RL for Robotics through Linear Statistical Modeling**
- **Control Barrier Functions with Linear Model Residuals for Safe Robot Automation**
- **Bridging Classical Control and Modern AI: A Unified Framework for Automated Agents**

These titles come from earlier research planning and are retained as lineage. They are not publication claims.

## Promotion rule

A manuscript should move toward a public preprint only after the benchmark/protocol is frozen, baselines are reproduced, results and uncertainty are reported, failure cases are documented, and the paper contains an explicit limitations section.
