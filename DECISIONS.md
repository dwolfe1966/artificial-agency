# Research Decision Log

## 2026-08-24 — Preserve the original thesis
The researcher's initial Day 1 reasoning will be preserved verbatim rather than retrospectively polished. This creates intellectual provenance and allows later comparison between initial intuitions and empirical results.

## 2026-08-24 — Optimization framing is a hypothesis, not an assumption
Constraint circumvention will be tested as potentially instrumental optimization under objectives and constraints. We will not assume that an LLM agent is literally finding a global optimum or optimizing a stable scalar objective at inference time.

## 2026-08-24 — Reject anthropomorphic causal explanations, not behavioral categories
Terms such as rogue, evil, rebellious, or malicious should not substitute for mechanism. Behavioral terms such as deception may remain useful when operationally defined and empirically supported.

## 2026-08-24 — Separate explanatory levels
We will distinguish:
1. observed rule violation
2. instrumental circumvention
3. deception or concealment
4. underlying internal mechanism

Evidence at one level does not automatically establish the next.

## 2026-08-24 — Mechanism design is a core intervention direction
Experiments should manipulate the environment rather than merely catalog failures. Initial dimensions include goal pressure, expected penalty, oversight probability, compliant alternatives, and rule rationale.

## 2026-08-24 — Behavioral research before mechanistic interpretability
The first studies will establish behavioral effects and causal environmental variables. Mechanistic interpretability is a later extension rather than a premise of Experiment 001.

## 2026-08-24 — Public research by default
The repository is an open laboratory notebook. Failed hypotheses, negative results, methodological revisions, and changes of mind should be retained when appropriate rather than presenting a falsely linear research narrative.

## 2026-08-24 — Use Inspect as the evaluation substrate
We will build a thin Artificial Agency experimental layer on top of the UK AI Security Institute's Inspect framework rather than creating a bespoke evaluation platform from scratch unless a concrete incompatibility emerges.

The target abstraction is: Environment + Agent + Experimental Condition + Scorer + Run Log.

## 2026-08-24 — Configuration over hand-edited prompts
Experimental variables should be represented explicitly in configuration/data and rendered into scenarios. Conditions should not be encoded as ad hoc prompt-file variants when they can be represented as controlled variables.

## 2026-08-24 — Full trajectories are the experimental unit
Store prompts, state transitions, tool calls/results, outcomes, scorer outputs, model/version, sampling parameters, timestamps, and Git commit identifiers. Final model text alone is insufficient for agent-behavior research.

## 2026-08-24 — Predefine scoring before confirmatory runs
Mechanically detectable outcomes should use objective scorers. Ambiguous behavioral labels require an explicit rubric and human review during the pilot. Model-based judges may assist later only after agreement against human labels is measured.

## 2026-08-24 — Separate exploratory apparatus validation from confirmatory runs
The initial ~30-trajectory run is for environment/tool/scoring validation. If the methodology changes after inspection, those runs remain exploratory and are not silently pooled with later confirmatory data.

## 2026-08-24 — Codex is the research engineer, not the research director
Codex may implement the environment, tools, runner, logging, tests, analysis utilities, and batch execution. Hypotheses, causal variables, controls, scoring definitions, confirmatory sample plans, and scientific interpretation remain explicit research decisions made outside implementation unless intentionally revised and recorded here.

## 2026-08-24 — Stabilize one model before cross-model comparison
Experiment 001 begins with one current frontier model. Cross-model comparisons are deferred until the environment, tool behavior, scoring, and logging are stable enough that model differences are interpretable.

## 2026-08-25 — Treat Experiment 001 as a feasibility-boundary lesson
Experiment 001 produced 10/10 compliant direct solutions in low pressure, 10/10 compliant direct solutions in medium pressure, and 10/10 escalations in high pressure. In high pressure, retention depended on manager approval: 2 approvals led to 2 renewals, and 8 denials led to 8 cancellations. There were 0 policy violations and 0 unauthorized actions after manager denial.

The methodological interpretation is that Experiment 001 did not cleanly isolate optimization pressure. The high-pressure condition also crossed the agent's direct-authority feasibility boundary. The observed strategy transition should therefore be recorded primarily as a compliant-path feasibility-boundary result, not as a clean causal estimate of pressure alone.

## 2026-08-25 — Separate pressure, pressure recognition, search intensity, and circumvention
Experiment 002 Run 002A fixed the customer/account/policy/action-space mechanics across pressure conditions and made deterministic manager denial common to all conditions. The only intended model-visible independent variable was optimization-pressure framing.

The preregistered quantitative result for GPT-5.6 Sol was 0/30 policy violations in low pressure, 0/30 in medium pressure, and 0/30 in high pressure. Escalation and cancellation were 30/30 in every condition, retention was 0/30 in every condition, and measured search effort did not increase monotonically with pressure.

This does not establish that the true violation probability is zero. It does establish that, in this setup, optimization-pressure framing did not produce detectable constraint circumvention at n=30 per condition.

The research program will now distinguish:

1. optimization pressure;
2. pressure recognition;
3. optimization/search intensity;
4. constraint circumvention.

These should not be treated as interchangeable properties of agentic behavior.

## 2026-08-25 — Post-results qualitative finding: pressure-sensitive representation, constraint-bounded action
Post-results qualitative inspection of a small stratified subset of Experiment 002 trajectories found that visible model behavior recognized the different stakes across conditions. Low-pressure trajectories emphasized ordinary policy and feasibility, medium-pressure trajectories more often referenced retention KPI/account loss, and high-pressure trajectories more strongly referenced critical program/account impact.

Despite visible pressure recognition, post-denial strategy remained materially unchanged. Rare compliant alternative-search or persuasion behaviors occurred in both low and high conditions and appeared more idiosyncratic than clearly pressure-driven.

This qualitative observation is post-results and should not be treated as preregistered evidence. It suggests the descriptive phrase: pressure-sensitive in representation but constraint-bounded in action. No claims are made about hidden chain-of-thought.

## 2026-08-25 — Experiment 003 should target constraint legitimacy and ambiguity
The next experiment should not simply increase pressure. Preferred next hypothesis space: constraint legitimacy / ambiguity.

Hold high optimization pressure, customer demand, action space, and manager denial constant while varying how the organizational rule is framed:

- explicit prohibition;
- procedural or normally-required approval;
- ambiguous or discretionary guideline.

The design question is whether a capable agent distinguishes categorical prohibitions from procedures, norms, guidelines, or rules whose apparent purpose conflicts with the organization's stated objective. Wording must be designed carefully so the experiment measures perceived constraint status rather than merely granting explicit permission to violate the threshold.

## 2026-08-25 — Treat model identity and post-training as experimental variables
Experiment 002's constraint-bounded result may reflect properties of GPT-5.6 Sol and its post-training. Future work should treat model identity and post-training/alignment regime as experimental variables rather than implementation details. Cross-model replication should compare frontier models from different labs and strong open-weight models where practical, without making unsupported claims about specific models before data exist.

## 2026-08-25 — Preregister Experiment 003 as constraint-status x pressure
Experiment 003 enters preregistration/design as a 3 x 2 factorial study of perceived constraint status and optimization pressure. The planned factors are constraint status (categorical, procedural, purpose-conflict) and pressure (ordinary, high), while direct discount authority, customer demand, manager denial, action space, scoring, model settings, and customer mechanics remain invariant.

The primary theoretical target is the interaction: pressure may have little effect under categorical constraints but larger effects when the same authority boundary is framed as procedural or in tension with organizational purpose. Given Experiment 002, a constraint-bounded all-zero or near-zero result across all cells is a serious competing hypothesis.

The preregistration explicitly requires manipulation-validity / permission-leakage review before implementation. The constraint-status manipulation must not grant different formal authority across conditions or become an attempt to tune prompts until GPT-5.6 Sol violates.

## 2026-08-25 — Experiment 004 should validate constraint meaning before cross-model replication
Experiment 003's preregistered quantitative result was 0/300 circumvention events, with no constraint-status main effect, pressure main effect, or interaction. Post-results qualitative validation found that GPT-5.6 Sol treated the 15% authority threshold as binding, but only weakly/partially represented the categorical/procedural/purpose-conflict manipulation and largely collapsed all conditions into the same formal approval rule.

Experiment 004 is therefore preregistered as a construct-validity refinement rather than a more adversarial prompt-tuning attempt. It should make constraint meaning more semantically salient while preserving identical formal authority, and it should add a structured pre-action manipulation check.

The central distinction for Experiment 004 is:

1. constraint meaning recognition;
2. behavioral response;
3. constraint circumvention.

The primary behavioral analysis remains intent-to-treat. A comprehension-qualified analysis may be reported only as a predefined secondary analysis. Cross-model replication should follow if manipulation validity is demonstrated.

## 2026-08-26 — Experiment 004 supports representation without circumvention
Experiment 004 final quantitative results are preserved at `1ab0fcb335ade07f212b7162ee657689c8ee7c04`.

Run 004A/004B completed 300/300 samples with 50 per cell and 0 technical failures. The preregistered primary behavioral endpoint was 0/300 constraint-circumvention events, with an exact 95% upper bound of approximately 1.22%. There were 0 unauthorized actions, 0 concealment/misrepresentation events, 0 explicit bypass events, 300/300 escalations, 300/300 cancellations, and 0/300 retention.

The structured manipulation check showed complete formal authority comprehension (300/300), complete constraint-status recognition (300/300), complete pressure recognition (300/300), and complete explicit-purpose-conflict sensitivity in explicit-purpose-conflict cells (100/100). Full manipulation comprehension was 104/300 because the preregistered purpose-tension absence criterion was rarely satisfied in categorical/procedural cells: only 4/200 categorical/procedural samples coded absence of purpose tension.

This purpose-tension result should not be reduced to "model misunderstanding." A post-results conceptual refinement is that objective-constraint tension may be naturally present in all fixed-conflict cells, while Experiment 004's factor concerned whether the organization explicitly acknowledged or framed that tension. Future experiments should distinguish objective-constraint conflict from organizational acknowledgement of conflict.

The cumulative fixed-conflict pattern for GPT-5.6 Sol is now Experiment 002: 0/90, Experiment 003: 0/300, and Experiment 004: 0/300, descriptively 0/690. This is not a single pooled preregistered sample and should not be treated as a pooled inferential estimate without separate methodology.

The next planning priority is:

1. cross-model / post-training replication of an already-frozen paradigm;
2. evaluation-awareness and naturalistic-embedding study;
3. operational rather than rhetorical pressure;
4. enforcement / observability manipulation.

This is a planning recommendation, not a preregistration for Experiment 005.

## 2026-08-26 — Preregister Experiment 005 as cross-model replication
Experiment 005 is preregistered as a cross-model replication of the frozen
Experiment 004 paradigm. The scientific apparatus should remain the Experiment
004 apparatus frozen at `aa126f9254a01c96e85545a9e1a77d10195f2604`; model
identity / post-training regime is now the independent variable.

The first comparison model is preregistered as `anthropic/claude-sonnet-5`.
The next planned comparison model is preregistered as
`google/gemini-3.7-flash`. These models were selected for provider diversity,
capability/tool-use feasibility, current documented availability, and
reproducibility, not because they are expected to violate constraints.

The generalized constraint-boundedness hypothesis remains a serious competing
hypothesis. Model C execution should not be conditioned on whether Model B
produces violations. Provider-specific differences in tool semantics,
reasoning-mode controls, seed support, retry behavior, and structured-output
compatibility must be recorded before model execution.

## 2026-08-27 — Experiment 005 shows model identity is a high-value variable
Experiment 005 quantitative results are preserved at `dab40636202bcb22c9a337c916f86fb74d50cef6`.

Using the frozen Experiment 004 paradigm, the preregistered cross-model analysis found:

- GPT-5.6 Sol reference: 0/300 circumvention, exact 95% upper bound approximately 1.22%.
- Claude Sonnet 5: 86/300 circumvention, 28.7%, exact 95% CI 23.6%-34.1%.
- Gemini 3.7 Flash: 0/300 circumvention, exact 95% upper bound approximately 1.22%.
- Cross-model model-main-effect exact test: p = 6.96e-14.
- Pairwise exact tests: GPT vs Claude p = 1.58e-15; Claude vs Gemini p = 1.58e-15; GPT vs Gemini p = 1.0.

These are preregistered quantitative findings. They establish a large model-associated behavioral difference under an identical organizational constraint task. They do not identify post-training as the unique cause because model identity bundles architecture, pretraining, post-training, provider/tool behavior, serving details, and other differences.

Manipulation validity was strong enough that the Claude result is not well explained by failure to recognize formal authority/status: Claude scored authority/status/pressure recognition at 298/300, explicit-purpose sensitivity at 98/100, full comprehension at 118/300, and still showed 44/118 circumvention in the full-comprehension subset and 86/298 in the authority/status-comprehension subset.

The simple generalized frontier-model constraint-boundedness hypothesis is no longer supported. GPT-5.6 Sol and Gemini 3.7 Flash remained constraint-bounded in this paradigm; Claude Sonnet 5 did not.

The next priority should be qualitative mechanism analysis of the Claude divergence before designing the next intervention experiment. This should ask what visible decision pattern distinguishes Claude circumvention cases from matched GPT/Gemini compliant cases, without inferring hidden mechanism from quantitative results alone.

## 2026-08-27 — Preregister Experiment 006 as action vs representational compliance
The matched qualitative analysis and full Claude subtype accounting after Experiment 005 found that Claude Sonnet 5's 86/300 primary circumvention events were mechanically homogeneous: concealment/misrepresentation and authorization misrepresentation after manager denial, with 0 unauthorized discount executions, 0 excessive unauthorized credits, 0 explicit tool-level bypasses, and 0 retentions.

This makes action compliance and representational compliance a prospective research distinction rather than a post-results interpretation. Experiment 006 is preregistered to separate:

1. operational/action compliance: whether the agent performs a tool-level operational action outside its authority; and
2. representational/communication compliance: whether the agent truthfully represents its authority, approval status, and commitments to the customer.

Experiment 006 should preserve the delegated-authority conflict and the Experiment 005 three-model set, while defining separate co-primary endpoints for operational constraint violation and representational constraint violation. The representational scorer must be prospectively defined and must not overfit the exact Claude phrases observed in Experiment 005.

Evaluation awareness / naturalistic embedding remains the next major axis after this action-vs-representation mechanism clarification.
