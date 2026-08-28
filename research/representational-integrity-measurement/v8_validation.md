# Fresh v8 Validation of Representational Integrity v1.2

_Status: fresh held-out validation result._

This validation used the already-frozen scorer:
`state-grounded-representational-integrity-v1.2`

Frozen scorer hash:
`7ba6d96d166297f3c27e61fbc1064c20c7c9d281f092b1a936da99582c180903`

Development commit:
`7a5c999129e855e808bfe0796f9b8bd4e3554ca2`

## Challenge Freeze

The v8 challenge was frozen before scoring in commit `4606b78`.

- Challenge version: `exp006-counterfactual-sensitivity-v8`
- Challenge SHA-256:
  `c5ee60827682de49cc64e2b32ec35ff6e0febefd46203f503592ed35c735f3e6`
- Total cases: 196
- Positive contradictions: 98
- Truthful matched controls: 98

Subtypes:

- `false_manager_approval`: 14
- `false_direct_authority`: 14
- `false_authorized_discount_amount`: 14
- `false_applied_discount`: 14
- `false_credit_authority_or_amount`: 14
- `false_binding_concession_state`: 14
- `false_requested_term_authority`: 14
- matched truthful controls for each family: 14 each

## One-Shot Result

| Metric | Value |
| --- | ---: |
| TP | 0 |
| FP | 0 |
| TN | 98 |
| FN | 98 |
| sensitivity | 0.000 |
| specificity | 1.000 |
| PPV | not estimable |
| NPV | 0.500 |
| accuracy | 0.500 |
| ambiguous predictions | 56 |
| ambiguity rate | 0.286 |

Subtype accuracy failed for every positive subtype and passed for each truthful
control subtype.

## Threshold Decision

Required thresholds were unchanged:

- sensitivity >= 0.95;
- specificity >= 0.95;
- PPV >= 0.95;
- NPV >= 0.95;
- subtype accuracy = 100%.

Decision: **FAIL**.

The validation failure was driven by sensitivity. The v8 challenge deliberately
used broader wording, including spelled-out percentages, indirect
authority/approval formulations, and account-state language not covered by the
v1.2 deterministic parser.

## Natural Regression Safety

The existing 48-case natural regression suite passed:

- false positives: 0/48.

Measurement unit tests passed:

- 34/34.

## Overall Validation

Overall validation: **FAIL**.

Because the fresh v8 validation failed, the 540-sample Experiment 006
authoritative dataset was not rescored in this task. Automated
representational measurement remains unresolved. The next measurement direction
should be either hybrid structured claim extraction or blinded/manual
annotation rather than further interpreting the current deterministic scorer as
a validated endpoint.

## Branch Closure

This result closes deterministic parser tuning as the current primary
measurement strategy. No v1.3 deterministic parser was created and the v1.2
scorer was not modified after v8 evaluation.

Validated Experiment 006 result:

- operational constraint violations: 0/540.

Invalidated or unresolved representational quantities:

- frozen Experiment 006 semantic representational flags: 103/540, not
  substantively validated;
- v0.5 exploratory state-grounded screen: 0/540, not sensitivity-validated;
- current representational-integrity violation rate in Experiment 006:
  unresolved.

The conceptual architecture remains useful, but deterministic claim extraction
did not generalize under the tested approach:

communication -> structured claims -> environment-state reconciliation.

Future work should consider LLM-assisted extraction of structured propositions
with deterministic state reconciliation, or experiments that make consequential
customer/inter-agent claims structurally observable at the time of action.
