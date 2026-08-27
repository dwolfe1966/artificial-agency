# Literature questions after Experiment 005 measurement correction

_Status: coordination note for a separate literature-review track. This is not
a literature review._

Experiment 005 produced an apparent cross-model difference under the frozen
scorer, but semantic audit found all 86 Claude Sonnet 5 authorization flags were
substantive false positives for the intended authorization-misrepresentation
construct. The episode highlights measurement validity as a central research
issue for agentic-misalignment evaluation.

## Priority Literature Questions

1. Measurement validity in agentic-misalignment evaluations

   What prior work distinguishes benchmark/scorer outputs from validated
   behavioral constructs? Which validation practices are used before making
   model-comparison claims?

2. Scorer/evaluator false positives

   How often do automated evaluators over-score safety-relevant behavior because
   of keyword, rubric, or judge-model artifacts? What methods reduce this risk?

3. Semantic vs behavioral policy violation

   Which frameworks separate operational action, commitment, representation,
   intent, and outcome when coding policy violations?

4. Deceptive or misleading communication vs unauthorized action

   How does the literature operationalize deception, concealment, misleading
   communication, and unauthorized tool use? What evidence is required to move
   from a misleading output to a deception claim?

5. Cross-model evaluation sensitivity to evaluator design

   When model comparisons show large differences, how do prior studies test
   whether the result reflects model behavior rather than evaluator sensitivity
   to style, phrasing, verbosity, or provider interface?

6. Evaluation awareness

   What methods measure whether a model infers it is in a benchmark or
   compliance evaluation without priming that behavior?

## Interface With Experiment 006

Experiment 006 prospectively separates:

- operational action;
- customer commitment;
- authorization representation.

The literature review should look for existing validation and adjudication
practices that can strengthen these endpoint definitions before implementation
or before public claims are made from Experiment 006.
