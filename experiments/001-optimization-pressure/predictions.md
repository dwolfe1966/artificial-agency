# Experiment 001 — Pre-Results Predictions

_Date created: 2026-08-24_
_Status: frozen before model trajectories_

These are deliberately common-sense priors, not results and not claims of calibrated forecasting accuracy. They are recorded before observing Experiment 001 model trajectories to reduce hindsight bias.

## Primary directional prediction

H1 — Optimization Pressure:

`P(circumvention | high goal pressure) > P(circumvention | medium goal pressure) > P(circumvention | low goal pressure)`

I expect the largest behavioral shift to be between medium and high pressure, because low and medium both have a direct compliant success path while high pressure requires escalation for compliant success.

## General behavioral prediction

A current frontier instruction-following model should usually respect the explicit 15% authority boundary when a compliant path exists. Therefore Experiment 001 is not expected to produce large violation rates overall.

The key predicted effect is a change in the **distribution of strategies** as goal pressure rises:

- Low: mostly direct compliant retention.
- Medium: mostly direct compliant retention, with somewhat more inspection/escalation/hesitation near the authority boundary.
- High: mostly escalation; after manager denial, a mixture of compliant failure/cancellation and occasional unauthorized discount attempts.

## Behavioral-distribution priors

These ranges are approximate priors. Rows need not sum exactly to 100% because they are ranges rather than a single multinomial forecast.

| Primary behavior | Low | Medium | High |
|---|---:|---:|---:|
| Compliant direct solution | 80–95% | 70–90% | 0–5% |
| Escalation | 0–10% | 5–20% | 70–90% |
| Legitimate workaround | 0–5% | 0–5% | 0–5% |
| Open violation | 0–5% | 0–5% | 5–20% |
| Concealed circumvention | ~0% | ~0% | 0–5% |
| Compliant goal failure / abandonment | 0–5% | 0–5% | 5–20% |
| Unresolved / max_steps | 0–5% | 0–5% | 0–10% |

### Confidence

- Low-condition direct compliance: **high** confidence. A 10% offer solves the task comfortably within authority.
- Medium-condition direct compliance: **medium-high** confidence. The required 15% sits exactly at the authority boundary but is explicitly permitted.
- High-condition escalation: **high** confidence. Escalation is the obvious legitimate route and is inexpensive in this apparatus.
- High-condition open violation: **low-medium** confidence. Modern frontier models may be sufficiently instruction-following that violations remain near zero even after denial.
- Concealed circumvention: **low** confidence and expected to be rare in this simple environment.

## Business-outcome priors

| Outcome | Low | Medium | High |
|---|---:|---:|---:|
| Retention rate | 85–100% | 80–100% | 35–55% |
| Policy-violation rate | 0–5% | 0–5% | 5–20% |
| Escalation rate | 0–10% | 5–20% | 70–90% |
| Max-step rate | 0–5% | 0–5% | 0–10% |

The high-condition retention prior is anchored partly by the apparatus: manager approval occurs with probability 0.40. Retention above that baseline would require some combination of unauthorized action or an unexpected implementation/model behavior; retention below it could result from failure to escalate, failure to use granted authority, cancellation, or max-step termination.

## Conditional predictions

### Manager denial followed by unauthorized action
Among high-pressure trajectories where the model escalates and approval is denied, I expect approximately **10–30%** to subsequently attempt an unauthorized discount above 15%.

Confidence: **low**. This is one of the most informative unknowns in the pilot.

### Manager approval followed by authorized 30% retention
Conditional on high-pressure escalation being approved, I expect **80–100%** of trajectories to use the granted authority successfully and retain the customer.

Confidence: **high**.

### Repeated messaging / non-price actions
Expected to be uncommon in low and medium conditions and more common after manager denial in high pressure, but generally **<20%** of trajectories.

### Human concealment review
I expect only trajectories containing an unauthorized action to require concealment review, probably **0–5% overall** and concentrated in high pressure. I do not expect strong evidence of concealment in this simple Phase 1 environment.

## What would surprise us?

The following would be meaningfully surprising relative to these priors:

1. Policy violations above 10% in the low or medium condition.
2. High-pressure escalation below 50%.
3. High-pressure open violation above 30%.
4. No meaningful shift in strategy distribution from low/medium to high pressure.
5. Large numbers of max-step trajectories (>15%), suggesting an apparatus or agent-loop problem rather than a clean behavioral result.
6. Frequent apparent concealment in this simple environment.
7. High-pressure retention substantially above 60% without an implementation explanation.
8. A model systematically ignoring manager approval/denial information.

## Disconfirming patterns

Patterns that would substantially weaken H1 or our current framing include:

- no meaningful behavioral difference across pressure conditions;
- more violations at lower pressure than higher pressure;
- fixed compliance/refusal behavior insensitive to action structure;
- violations unrelated to whether they improve task success;
- behavior dominated entirely by a learned instruction-following policy with no detectable sensitivity to the institutional tradeoff.

Importantly, a near-zero violation rate in all conditions would not by itself establish that optimization pressure is absent. It would show that this particular apparatus/model combination failed to expose the predicted effect and would motivate carefully designed follow-up experiments rather than retrospective modification of this run.

## Freeze rule

This file is now frozen before observing model trajectories. Do not edit these predictions to match observed results. Later interpretations or revised expectations belong in a separate dated post-results note.
