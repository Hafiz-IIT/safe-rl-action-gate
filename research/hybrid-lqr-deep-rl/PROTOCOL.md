# Hybrid Control Architectures: Merging LQR and Deep RL for Robust Robot Autonomy

## Status
Architecture and experiment protocol.

## Research question
When does a learned residual provide useful nonlinear correction without destroying the stability/interpretability advantages of a linear controller?

## Architecture
state estimate -> LQR action -> learned residual -> action limiter -> safety gate -> environment

## Ablations
- LQR only
- RL only
- residual only
- LQR + residual
- LQR + residual + gate
- residual scale sweep
- model mismatch sweep

## Metrics
cumulative cost, violations, recovery time, intervention rate, action magnitude, and seed variance.

## Claims boundary
No deep-RL training result is claimed in the repository at this stage.
