# Evaluation Protocol

## Primary research question
How much safety benefit can an explicit runtime action gate provide before introducing formal barrier-function machinery?

## Metrics
- Raw constraint-violation rate
- Post-gate violation rate
- Intervention rate
- Substitution rate
- Blocked-action rate

## Falsification criteria
- The gate permits a predicted constraint violation.
- The chosen substitute violates a constraint.
- Blocking is skipped when no safe alternative exists.

## Reproducibility
```bash
python -m unittest discover -s tests -v
```
