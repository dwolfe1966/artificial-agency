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

### Week 3 — Reproduction
- Reproduce a tractable subset of relevant frontier safety/agentic-misalignment research.
- Document methodological differences and discrepancies.

**Deliverable:** Reproduction 001.

### Week 4 — Experimental rigor
- Audit prompt bias, scenario comparability, evaluator bias, model-awareness effects, and scoring reliability.
- Apply confidence intervals, effect sizes, bootstrap estimation, inter-rater reliability, and power concepts as appropriate.

**Deliverable:** Institutional Misalignment Benchmark v0.1 specification.

### Week 5 — Benchmark construction
- Build 50 structured environments across five domains.
- Each environment should specify objective, rules, available actions/tools, hidden state, success condition, violation condition, and oversight condition.

**Deliverable:** Benchmark v0.2.

### Week 6 — Experimental infrastructure
- Build Agent Behavior Observatory v0.1.
- Automate runs and record model, scenario, condition, actions, tool calls, trajectory, outcome, policy violation, evaluator score, latency, and cost where available.

**Deliverable:** automated reproducible harness.

### Week 7 — Study 001
Initial scale target: 3 models x 50 scenarios x 3 goal-pressure conditions x 10 trials = approximately 4,500 trajectories.

Test whether goal pressure changes violation probability and whether concealed/strategic violations behave differently.

**Deliverable:** Dataset 001 + analysis.

### Week 8 — First public research artifact
Write and release a technical report tentatively titled:

**When Goals and Rules Conflict: Measuring Institutional Misalignment in LLM Agents**

Release methodology, code, benchmark, selected trajectories/results, and limitations.

## Months 3–12

### Month 3 — Capability x misalignment
Study whether capability changes the character of failure: incompetent failure -> opportunistic violation -> strategic circumvention.

### Month 4 — Oversight
Manipulate perceived audit probability and test whether oversight suppresses violations, changes concealment, or both.

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
