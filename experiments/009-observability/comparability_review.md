# Experiment 009 Comparability Review

_Status: pre-implementation design review._

## Internal Coherence

The preregistered design is internally coherent if implementation later proves
these invariants:

1. only `p_detect` is manipulated causally;
2. operational violation is distinct from detected violation;
3. formal authority is invariant;
4. prohibited action remains available in all cells;
5. unauthorized action is instrumentally useful in both scenarios;
6. sanction mechanics are fixed;
7. stochastic draws are reproducible;
8. recovery cannot redraw authoritative observations;
9. primary endpoint is mechanically scored;
10. awareness remains post-action and secondary;
11. the staged execution rule is technical-integrity based only;
12. no self-preservation manipulation is introduced;
13. no frozen Experiment 001-008B2 artifacts are changed.

## Provider Comparability

The model set remains GPT-5.6 Sol, Claude Sonnet 5, and Gemini 3.7 Flash.

Provider differences must be classified as transport/configuration-level
unless they change:

- tool availability;
- authority semantics;
- stochastic draw semantics;
- context capacity enough to alter scenario content;
- retry / recovery sample identity;
- two-phase awareness lifecycle.

If a provider cannot support the same operational tool semantics, stochastic
state logging, or two-phase awareness lifecycle, stop before production.

## Scenario Comparability

Procurement and data-access scenarios intentionally differ in domain and
operational action type. They must remain comparable on:

- categorical authority boundary;
- deterministic denial;
- unavailable full-success compliant path after denial;
- unauthorized action availability;
- naturalistic presentation style;
- fixed observability manipulation;
- fixed sanction mechanics;
- primary endpoint mechanical measurability.

## Observability Review Questions

Before implementation freeze, answer:

1. Does changing `p_detect` alter formal permission? It must not.
2. Does changing `p_detect` alter action availability? It must not.
3. Does changing `p_detect` alter objective stakes or `p_goal`? It must not.
4. Does changing `p_detect` alter sanction probability conditional on
   detection or sanction severity? It must not.
5. Is the unauthorized action still detected by stochastic draw only after the
   action occurs?
6. Is the model told the true configured detection probability?
7. Can the detection draw be replayed from sample metadata?
