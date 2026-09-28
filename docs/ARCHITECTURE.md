# Architecture

## Purpose
Runtime safety shield for sequential decision systems that allows, substitutes or blocks proposed actions against explicit constraints.

## Flow
Policy proposal → transition prediction → constraint checks → minimal-intervention safe substitution → BLOCK when no safe alternative exists.

## Invariants
1. Unsafe requested actions must not pass unchanged.
2. A substitute must itself satisfy every registered constraint.
3. If no safe alternative exists, the gate must block.

## Failure handling
Outputs should remain inspectable and expose the reason for allow, substitute, block, abstain, verify, or escalate decisions.
