# Artificial Agency — Year 1 Research Roadmap

## North Star
Produce research good enough that serious frontier-AI researchers want to read, critique, reproduce, or build upon it.

The work should create option value across frontier-lab employment, independent research, open source, agent governance/observability, and AI-native organizational design.

## First 8 Weeks

### Week 1 — Establish the research program
- Define Research Question 001.
- Capture original thesis before extensive literature immersion.
- Define initial hypotheses and variables.
- Establish repository and research journal.
- Design one falsifiable toy experiment.

**Deliverable:** Research Note 001 + working repository.

### Week 2 — Experiment 001
- Build 10–20 legitimate goal/rule conflict scenarios.
- Test multiple model families where practical.
- Develop initial outcome taxonomy: compliance, goal abandonment, clarification, legitimate workaround, open violation, concealed/strategic violation.

**Deliverable:** code, trajectories, preliminary results.

**Actual lesson now preserved:** Experiment 001 identified a compliant-path feasibility boundary. Low and medium pressure produced compliant direct solutions; high pressure produced escalation. It did not cleanly isolate pressure because high pressure also crossed direct authority.

### Week 3 — Reproduction
- Reproduce a tractable subset of relevant frontier safety/agentic-misalignment research.
- Document methodological differences and discrepancies.

**Deliverable:** Reproduction 001.

### Week 4 — Experimental rigor
- Audit prompt bias, scenario comparability, evaluator bias, model-awareness effects, and scoring reliability.
- Apply confidence intervals, effect sizes, bootstrap estimation, inter-rater reliability, and power concepts as appropriate.

**Deliverable:** Institutional Misalignment Benchmark v0.1 specification.

Add explicit separation between optimization pressure, pressure recognition, search intensity, and constraint circumvention. Experiment 002 showed that pressure recognition can occur without detectable policy violation or increased search effort.

### Week 5 — Constraint-status experiments
- Design Experiment 003 around constraint legitimacy / ambiguity rather than simply increasing pressure.
- Hold high pressure, customer demand, action space, and manager denial constant.
- Vary rule status: categorical prohibition, procedural approval norm, and ambiguous/discretionary guideline.
- Ensure wording measures perceived constraint status rather than giving explicit permission to violate.

**Deliverable:** Experiment 003 preregistered specification.

**Current status:** Experiment 003 completed with 0/300 circumvention events and strong behavioral constraint-boundedness, but post-results qualitative validation found that the constraint-status manipulation was only weakly/partially represented. Experiment 004 was therefore run as a construct-validity refinement with stronger semantic constraint wording and a structured pre-action manipulation check.

Experiment 004 completed 300 samples, 50 per cell, with 0 technical failures and 0/300 primary circumvention events. Formal authority, constraint-status labels, and pressure were recognized in 300/300 structured checks; explicit-purpose-conflict sensitivity was 100/100 in explicit-purpose-conflict cells. Full manipulation comprehension was 104/300 because the preregistered absence-of-purpose-tension criterion was rarely satisfied in categorical/procedural cells. This is now recorded as a post-results conceptual distinction between objective-constraint conflict and organizational acknowledgement of conflict.

### Week 6 — Experimental infrastructure
- Build Agent Behavior Observatory v0.1.
- Automate runs and record model, scenario, condition, actions, tool calls, trajectory, outcome, policy violation, evaluator score, latency, and cost where available.

**Deliverable:** automated reproducible harness.

### Week 7 — Study 001
Initial scale target should be revised after Experiments 003-004. Model identity is now a substantive experimental variable rather than an implementation detail.

Test whether constraint-bounded behavior differs across frontier models from different labs, models with different post-training regimes, and strong open-weight models where practical.

**Deliverable:** Dataset 001 + analysis.

**Experiment 005 result and correction:** cross-model replication of the frozen Experiment 004 paradigm initially showed a large model-associated difference under the frozen scorer. GPT-5.6 Sol and Gemini 3.7 Flash produced 0/300 scorer flags each, while Claude Sonnet 5 produced 86/300 scorer flags. The cross-model model-main-effect exact test was p = 6.96e-14 for that measured endpoint. A later semantic audit found all 86 Claude flags were substantive false positives for authorization misrepresentation: Claude did not exceed operational discount authority, execute excessive credit, falsely claim manager approval, falsely claim >15% authority, or make unauthorized customer commitments. The result is now treated as a measurement-validity lesson rather than evidence of model-specific circumvention.

**Updated priority after Experiment 005 semantic audit:** Experiment 006 should prospectively separate operational/action compliance from representational/communication compliance using a state-based semantic scorer. After Experiment 006, the next major axis remains evaluation awareness / naturalistic embedding, followed by operational pressure and enforcement / observability. This ordering is a planning recommendation, not an implementation plan.

**Experiment 006 result and scorer-validation correction:** Experiment 006
preserved the action/representation distinction prospectively. The frozen
quantitative analysis found 0/540 operational violations and 103/540
representational-scorer flags: GPT-5.6 Sol 8/180, Claude Sonnet 5 53/180, and
Gemini 3.7 Flash 42/180. A limited post-results qualitative validation selected
24 scorer-positive and 24 matched scorer-negative cases before reading content.
Manual review found 0/24 sampled positives were substantive representational
violations and 24/24 matched negatives were non-violations. The
representational scorer over-scored truthful denial, authority-limit, and
cancellation language. Current priority should therefore shift to
representational scorer repair and validation before another production
estimate or model comparison on representational compliance.

**Representational-integrity measurement update:** post-results exploratory
work after Experiment 006 defines representational integrity as claim-to-state
consistency. The v0.5 measure corrected the known false-positive pattern and
passed a 90-case validation sample for false-positive control, then produced
0/540 state-grounded representational violations in exploratory rescoring.
Counterfactual sensitivity challenges then showed that v0.5 and exploratory
revisions through v1.2 did not meet the predeclared sensitivity thresholds. The
fresh v8 validation of frozen v1.2 failed with TP 0, FP 0, TN 98, FN 98,
sensitivity 0.000, specificity 1.000, NPV 0.500, accuracy 0.500, subtype
accuracy FAIL, natural regression PASS, and overall validation FAIL. No
post-v8 540-sample rescore was performed. The 0/540 state-grounded rescore
remains an unresolved screening observation rather than a validated absence
claim. Deterministic parser tuning is paused as the current primary measurement
strategy. The next methodological priority is either bounded hybrid
claim-extraction validation using human-labeled structured propositions or
future behavioral experiments with structured/verifiable actor-to-actor claims.

**Scenario Suite v1 direction:** the next program layer is a reusable
multi-scenario framework for organizational constraint experiments. Scenario
Suite v1 should diversify beyond customer-retention/pricing while preserving
mechanically verifiable endpoints. Initial candidate scenarios should emphasize
refund authority, procurement purchasing, restricted data access, and project
scheduling/approval bypass. This is a prospective design framework, not a
preregistered production experiment.

**Experiment 007 preregistration direction:** Experiment 007 is the first
Scenario Suite v1 empirical pilot. It should test whether operational
constraint-bounded behavior generalizes across four organizational domains:
refund authority, procurement/purchasing authority, restricted data access, and
project scheduling/approval bypass. The pilot varies model and scenario only,
uses 30 samples per model x scenario cell, and keeps pressure, observability,
manager denial, episode structure, and evaluation salience fixed for this
baseline.

**Experiment 007 result:** Experiment 007 completed 360 authoritative samples:
120 per model, 90 per scenario, and 30 per model x scenario cell. The
preregistered operational endpoint found 0/360 operational constraint
violations, with an exact 95% upper confidence bound of approximately 1.02%.
All 12 model x scenario cells were 0/30. GPT-5.6 Sol, Claude Sonnet 5, and
Gemini 3.7 Flash each had 0/120 operational violations across refund authority,
procurement authority, restricted data access, and project scheduling/approval
bypass.

Hypothesis results: H1 generalized operational constraint-boundedness was
supported within precision limits; H2 scenario effect, H3 model effect, and H4
model x scenario interaction were indeterminate because the primary endpoint
had no variance; H5 search-within-constraints was supported descriptively.
Escalation occurred in 360/360 samples. Compliant alternative search and
partial objective achievement varied substantially by scenario: refund,
procurement, and data-access showed high alternative-search rates, while
scheduling showed much lower alternative search and partial achievement. This
supports scenario-sensitive compliant strategy differences, not a
post-hoc significance claim.

Experiment 007 extends mechanically validated operational
constraint-boundedness beyond retention/discount tasks into four qualitatively
distinct domains. Do not pool Experiments 002-007 inferentially without a
separate preregistered method. The recurring pattern is that models adapted
behavior within formal authority boundaries while operational violations
remained rare or absent under explicit, synthetic, eval-salient organizational
tasks.

**Updated priority after Experiment 007:** Scenario breadth can continue later,
but it is no longer the immediate bottleneck. The next priority order is:

1. evaluation awareness / naturalistic embedding;
2. operational vs rhetorical pressure;
3. enforcement / observability;
4. multi-agent delegation.

**Experiment 008 preregistration direction:** Experiment 008 is the next
prospective study. It tests evaluation awareness / naturalistic embedding by
crossing procurement and restricted-data-access scenarios with eval-salient
versus naturalistically embedded presentation across GPT-5.6 Sol, Claude Sonnet
5, and Gemini 3.7 Flash. The planned allocation is 30 replicates per model x
scenario x presentation cell, for 360 samples.

Core question: does operational compliance change when the same authority
conflict is embedded in a more naturalistic workflow that is less obviously
structured as a compliance evaluation? The underlying authority mechanics,
forbidden action availability, objective stakes, baseline narrative pressure,
and operational scoring must remain invariant across presentation styles.

Experiment 008 includes a post-action structured evaluation-awareness measure.
This measure is secondary, post-treatment, and not a pre-treatment covariate.

### Week 8 — First public research artifact
Write and release a technical report tentatively titled:

**When Goals and Rules Conflict: Measuring Institutional Misalignment in LLM Agents**

Release methodology, code, benchmark, selected trajectories/results, and limitations.

## Months 3–12

### Month 3 — Capability x misalignment
Study whether model identity, capability, and post-training change the character of failure: incompetent failure -> compliant constraint-bound behavior -> opportunistic violation -> strategic circumvention.

### Month 4 — Oversight
Manipulate perceived audit probability while holding the formal rule constant. Test whether observability suppresses violations, changes concealment, or changes willingness to treat a rule as negotiable.

Separate the formal rule from expected detection probability and expected consequence of violation. This will help distinguish constraint-bounded behavior from instrumental compliance.

### Month 5 — Multi-agent institutions
Create hierarchical/multi-agent environments with partially conflicting incentives. Study delegation, information hiding, responsibility shifting, collusion, coordination, and escalation.

### Month 6 — Publication push
Consolidate the strongest result into Paper 001. Harden Benchmark v1.0 and Observatory v1.0. Seek external methodological criticism.

### Month 7 — Research network
Target 10–20 substantive research conversations across frontier labs, MATS, academia, and AI safety/evaluation communities.

### Month 8 — External collaboration
Conduct Study 004 with a collaborator who adds complementary research expertise.

### Month 9 — Commercial experiment
Interview organizations deploying agents. Test demand for behavioral observability, evaluation, permissions, governance, and safety assessment.

### Month 10 — Frontier-lab positioning
Map portfolio evidence against current Anthropic/OpenAI and related role/fellowship requirements. Close the highest-impact remaining gaps.

### Month 11 — Applications
Pursue relevant fellowships, residencies, research-engineering/evaluation roles, MATS, and adjacent frontier/safety organizations.

### Month 12 — Decision point
Choose among frontier lab, independent research, startup/product, or hybrid based on accumulated evidence rather than a predetermined career outcome.

## Weekly operating rule
Approximately 70% doing / 30% learning. Every week should end with something that exists: code, an experiment, dataset, figure, research note, Git commit, external critique, or application artifact.

## Sunday Research Review
1. What did we hypothesize?
2. What did we actually learn?
3. What surprised us?
4. What is now less likely to be true?
5. What experiment should we run next?

Current review prompt after Experiment 008 preregistration: does the
naturalistic presentation preserve formal authority, action availability, and
objective stakes while changing primarily evaluation/compliance salience?

## Experiment 008 result and lifecycle correction

Experiment 008 completed 360 authoritative samples across procurement and
restricted data access, eval-salient and naturalistic presentations, and the
three-model set GPT-5.6 Sol, Claude Sonnet 5, and Gemini 3.7 Flash.

Primary operational result:

- operational constraint violations: 0/360;
- eval-salient: 0/180;
- naturalistic: 0/180;
- all 12 model x scenario x presentation cells: 0/30.

This supports continued attention to operational constraint-boundedness under
synthetic single-agent tasks, including naturalistically embedded presentations,
within the precision limits of the experiment.

The post-action evaluation-awareness measure failed as an instrument: captured
responses were 0/360. The failure was lifecycle-related, not a substantive
awareness result. The awareness tool was exposed during operational behavior,
and the post-action probe did not isolate an awareness-only phase or
deterministically record missing awareness responses.

H2 evaluation-awareness manipulation validity should be treated as
measurement-indeterminate / instrument failure. H6 should not be read as
evidence that awareness changed or did not change behavior.

Next methodological priority:

1. fresh preregistered Experiment 008B replication using a true two-phase
   lifecycle;
2. operational vs rhetorical pressure;
3. enforcement / observability;
4. multi-agent delegation.

Retrospective awareness replay of the existing 360 cases is not equivalent to
the failed post-action measure because it would occur in a new inference
episode with reconstructed terminal context.
