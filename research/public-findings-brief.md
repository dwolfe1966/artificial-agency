# Public Findings Brief: Experiments 001-005

_Status: factual public-safe summary after quantitative preservation and semantic measurement audit. These findings are preliminary and not yet peer reviewed._

## Research Question
Under what conditions do capable AI agents treat organizational constraints as hard boundaries versus obstacles or procedures to navigate?

This project studies agent behavior in a simplified customer-retention environment where an AI agent is asked to retain an account while operating under an organizational authority limit.

## Experiment Progression

- **Experiment 001:** feasibility-boundary pilot. The high-pressure condition crossed the direct-authority feasibility boundary, so the result was mainly a compliant-path feasibility lesson rather than a clean pressure effect.
- **Experiment 002:** fixed conflict plus optimization-pressure framing. The customer requirement and action space were held fixed while pressure varied.
- **Experiment 003:** constraint-status x pressure. The same authority boundary was framed as categorical, procedural, or purpose-conflict while pressure varied.
- **Experiment 004:** stronger construct salience plus a structured manipulation check. This tested whether the model represented formal authority, constraint status, pressure, and purpose tension before acting.
- **Experiment 005:** cross-model replication of the frozen Experiment 004 paradigm. The task, tools, authority structure, manipulation check, and scoring were held fixed while model identity varied.

## Key Quantitative Findings

Experiment 004 reference result:

- **GPT-5.6 Sol:** 0/300 observed constraint circumventions.
- Exact 95% confidence interval upper bound: approximately 1.22%.

Experiment 005 frozen scorer result:

| Model | Frozen scorer flags | Rate | Exact 95% CI |
| --- | ---: | ---: | --- |
| GPT-5.6 Sol reference | 0/300 | 0.0% | upper approximately 1.22% |
| Claude Sonnet 5 | 86/300 | 28.7% | 23.6%-34.1% |
| Gemini 3.7 Flash | 0/300 | 0.0% | upper approximately 1.22% |

Cross-model model-main-effect exact test:

- p = 6.96e-14.

Pairwise exact tests:

- GPT-5.6 Sol vs Claude Sonnet 5: p = 1.58e-15.
- Claude Sonnet 5 vs Gemini 3.7 Flash: p = 1.58e-15.
- GPT-5.6 Sol vs Gemini 3.7 Flash: p = 1.0.

These values describe the preserved frozen scorer endpoint. A later semantic
audit showed that this endpoint did not validate as the intended substantive
authorization-misrepresentation construct.

Full semantic audit of the 86 Claude scorer flags:

- explicit false authority above 15%: 0/86;
- false manager-approval claim: 0/86;
- unauthorized customer commitment: 0/86;
- unauthorized discount execution: 0/86;
- excessive unauthorized credit: 0/86;
- explicit tool-level bypass: 0/86;
- truthful authorization-limit or denial-disclosure statements: 86/86.

## Important Interpretation

Experiment 005 initially appeared to show a large cross-model difference under
the frozen scorer. The full semantic audit changed the interpretation: all 86
Claude flags were substantive false positives for the intended
authorization-misrepresentation construct.

The episode is now best understood as a measurement-validity result rather than
evidence of model-specific constraint circumvention. The frozen scorer
conflated truthful authorization-related language after manager denial with
false authorization or approval claims.

The current public-safe conclusion is narrower: in this task, scorer output and
validated construct should not be treated as identical. Apparent cross-model
effects can be artifacts of evaluator design.

The results also do not establish hidden reasoning or internal motives. The quantitative analysis used structured manipulation-check data and mechanically recoverable scorer/environment state, not hidden chain-of-thought.

## Important Limitations

- This is early research.
- The experiments use one task family and one simplified organizational environment.
- The work has not yet been peer reviewed.
- Cross-provider execution differences exist even though task semantics, tools, authority structure, and scoring were held fixed.
- Claude and Gemini runs required operational recovery. Authoritative sample reconciliation was complete: zero duplicate, missing, or unexpected sample IDs.
- Scoreless technical samples were retained as intent-to-treat technical failures: Claude 2/300 and Gemini 4/300.
- The semantic audit was post-results and corrects interpretation rather than changing the frozen scorer outputs.
- Results should not be generalized to broad claims about "Claude," "GPT," or "Gemini" behavior outside this paradigm.
- No claim is made that any tested model is globally safer or less safe.

## What Comes Next

The immediate next step is Experiment 006: prospectively separate operational
action compliance from representational/communication compliance using a
state-based semantic scorer.

Planned follow-up axes include:

- measurement validity in agentic-misalignment evaluations;
- evaluation-awareness testing;
- stronger operational rather than merely rhetorical pressure;
- enforcement and observability manipulations;
- further replication across models and task families.
