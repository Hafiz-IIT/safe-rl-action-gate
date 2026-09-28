# Bayesian Linear Models as Priors for Safe Reinforcement Learning in Robotics

## Status
Research protocol with an implemented scalar Bayesian dynamics estimator.

## Hypothesis
Posterior uncertainty from a transparent dynamics prior can identify regions where a learned controller should verify, reduce action magnitude, or defer.

## Experiments
- posterior convergence under repeated observations
- calibration under noise
- prior misspecification
- uncertainty-triggered action gating
- comparison with point-estimate dynamics

## Metrics
- coefficient error
- predictive interval coverage
- unsafe transition rate
- unnecessary intervention rate
- calibration error

## Claims boundary
The current implementation estimates a scalar uncertain state coefficient; it is a foundation for the paper, not the full safe-RL system.
