# Koopman-Based Linear Embeddings for Control of Automated Agents

## Status
Research protocol. The repository currently contains a **Koopman-inspired polynomial lift**, not a full Koopman operator pipeline.

## Hypothesis
A learned lifted linear representation can improve short-horizon prediction/control on mildly nonlinear dynamics while retaining more interpretability than a fully opaque policy.

## Baselines
- local linear dynamics
- polynomial lifted predictor
- nonlinear black-box predictor (future)
- controller using each model (future)

## Metrics
- one-step prediction RMSE
- rollout RMSE
- closed-loop cost
- constraint violations
- compute cost
- sensitivity to out-of-distribution states

## Promotion rule
Do not rename the current implementation “Koopman control” in results until operator identification and closed-loop evaluation are actually implemented.
