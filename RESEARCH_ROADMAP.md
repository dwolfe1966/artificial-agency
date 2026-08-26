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

**Current Experiment 005 direction:** preregister cross-model replication of the frozen Experiment 004 paradigm. The independent variable is model identity / post-training regime, with `anthropic/claude-sonnet-5` as the first comparison model and `google/gemini-3.7-flash` as the next planned comparison. Do not change Experiment 004 prompts, tools, manipulation check, authority structure, or scoring for this replication.

**Tentative priority after Experiment 005:** evaluation awareness / naturalistic embedding, then operational pressure, then enforcement / observability. This ordering is a planning recommendation, not an implementation plan.

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

Current review prompt after Experiments 001-004: is the repeated GPT-5.6 Sol constraint-bounded result model-specific, evaluation-context-specific, or robust to operational pressure and altered enforcement/observability?
