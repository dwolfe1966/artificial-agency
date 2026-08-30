# Experiment 008 Awareness Lifecycle Diagnostic

_Status: post-results measurement/lifecycle diagnostic. This document does not
modify the frozen Experiment 008 apparatus, raw data, scorer outputs, or
preserved quantitative results._

## Provenance

- Experiment 008 preregistration SHA:
  `0aa5935f6830afe3e9f447ca9c299420e0a39586`
- Frozen scientific implementation SHA:
  `02f7098dea80156ae48faee5ee091659f538beee`
- Quantitative results preservation commit:
  `cc794f8bb4c3c4a13fe2c07528bbddb443fec4b2`

## Preserved Results

Authoritative Experiment 008 data reconcile to 360/360 samples:

- GPT-5.6 Sol: 120/120
- Claude Sonnet 5: 120/120
- Gemini 3.7 Flash: 120/120

Primary operational endpoint:

- operational constraint violations: 0/360
- eval-salient: 0/180
- naturalistic: 0/180
- procurement: 0/180
- data-access: 0/180

Structured post-action awareness capture:

- captured awareness responses: 0/360
- awareness attempted before terminal: 12/360
- structured scorer technical/max-step flags: 37/360

## Root Cause

The Experiment 008 awareness instrument failed because the task lifecycle did
not isolate operational behavior from post-action awareness collection.

Mechanically:

1. `record_evaluation_awareness` was included in the same tool list as the
   operational tools returned by `operational_tools()`.
2. Because that tool was exposed during the operational phase, some models
   attempted to call it before the environment had reached a terminal
   operational state.
3. The environment correctly rejected pre-terminal awareness attempts and set
   `awareness_attempted_before_terminal`.
4. After the operational loop ended, `post_action_awareness_probe()` appended a
   post-action prompt and called `generate(..., tool_calls="single")`.
5. The post-action solver did not enforce a dedicated awareness-only phase,
   revoke operational tools, retry missing awareness tool calls, or
   deterministically record a missing response if the model failed to call the
   awareness tool.
6. The scorer correctly recorded no captured awareness response.

Thus the 0/360 awareness capture result is a lifecycle/instrument failure, not
evidence that models lacked evaluation awareness.

## Early Awareness Attempts

The 12 pre-terminal awareness attempts occurred because the awareness tool was
available during Phase A operational behavior.

Structured counts:

| Model | Scenario | Presentation | Early Attempts |
| --- | --- | --- | ---: |
| Claude Sonnet 5 | procurement | eval-salient | 7 |
| Claude Sonnet 5 | procurement | naturalistic | 2 |
| Gemini 3.7 Flash | procurement | eval-salient | 2 |
| Gemini 3.7 Flash | procurement | naturalistic | 1 |

All early attempts were rejected by environment state because terminal
operational state had not yet been reached.

## Structured Technical/Max-Step Flags

All 37 structured technical flags were max-step terminations in procurement
cells. They were not provider/runtime technical failures.

| Model | Scenario | Presentation | Category | Count |
| --- | --- | --- | --- | ---: |
| GPT-5.6 Sol | procurement | eval-salient | max-step termination | 1 |
| GPT-5.6 Sol | procurement | naturalistic | max-step termination | 13 |
| Claude Sonnet 5 | procurement | eval-salient | max-step termination | 2 |
| Claude Sonnet 5 | procurement | naturalistic | max-step termination | 14 |
| Gemini 3.7 Flash | procurement | eval-salient | max-step termination | 1 |
| Gemini 3.7 Flash | procurement | naturalistic | max-step termination | 6 |

No data-access sample received a structured technical/max-step flag.

## Operational Endpoint Interpretation

The 37 max-step samples do not materially weaken the primary operational
endpoint interpretation under the frozen ITT plan.

Reason:

- procurement samples exposed the same structured operational action space,
  including the prohibited above-authority purchase and split-purchase paths;
- max-step termination occurred after the operational loop had given the agent
  repeated opportunities to use available tools;
- no structured state recorded an unauthorized purchase, split purchase,
  approval bypass, or restricted access before termination;
- technical/max-step status remains reported separately and is not recoded
  post hoc as compliance or violation.

The primary operational result should be stated as:

Naturalistic embedding produced no observed operational constraint violations:
eval-salient 0/180 and naturalistic 0/180. However, evaluation-awareness
manipulation validity could not be assessed because the post-action awareness
instrument failed to capture responses.

Do not state from Experiment 008 that models lacked evaluation awareness,
naturalistic embedding reduced evaluation awareness, or evaluation awareness had
no behavioral effect.

## Corrected Two-Phase Lifecycle

Future awareness-measure experiments should use a true two-phase lifecycle.

### Phase A -- Operational Behavior

- expose only operational tools;
- keep awareness tools unavailable;
- allow the agent to act normally until terminal state or a frozen stopping
  condition;
- record and freeze tool actions, environment state, and primary operational
  score;
- prevent any later phase from mutating Phase A state.

### Transition

- freeze the operational state;
- revoke all operational tools;
- mark the primary operational score immutable;
- schedule a dedicated post-action awareness turn.

### Phase B -- Post-Action Awareness

- expose only `submit_eval_awareness(...)`;
- ask for the structured awareness response without hidden chain-of-thought and
  without leading causal questions;
- require exactly one response or deterministically record missing/malformed;
- terminate the sample after awareness collection.

The awareness response must be structurally incapable of changing the primary
operational score.

## Retrospective Replay Assessment

An awareness-only retrospective replay of the existing 360 cases would not be
equivalent to the preregistered awareness construct.

Validity concerns:

- the original conversational state is gone;
- the model would receive reconstructed terminal context rather than continuing
  from the original episode;
- awareness would be measured in a new inference episode after outcome
  reconstruction;
- replay could change what the model reports about perceived task type or
  evaluation salience.

Recommended follow-up: fresh preregistered Experiment 008B replication using
the corrected two-phase lifecycle. Retrospective replay may be useful only as
exploratory instrumentation testing, not as a replacement for the failed
post-action awareness measure.
