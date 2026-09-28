# Residual Reinforcement Learning with Linear Statistical Priors for Robotic Automation

## Status
Research protocol / implementation groundwork. No trained RL result is claimed yet.

## Core hypothesis
A policy that learns a bounded residual around a competent linear controller can require fewer environment interactions and produce fewer catastrophic early actions than a policy trained from scratch.

## Baselines
1. LQR only
2. RL only
3. LQR + residual policy
4. LQR + residual policy + action safety gate

## Required experiments
- nominal dynamics
- plant/model mismatch
- additive disturbances
- action saturation
- sample-budget sweep
- residual-scale ablation
- gate/no-gate ablation

## Primary metrics
- cumulative cost
- constraint violations
- samples to threshold performance
- final-state error
- intervention rate
- variance across seeds

## Claims boundary
The current repository provides the linear baseline, residual composition primitive, safety gate, and deterministic benchmark harness. It does not yet include a learned PPO/SAC/DDPG residual policy.
