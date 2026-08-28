# Scenario Suite v1 Implementation Roadmap

_Status: prospective architecture. No production scenarios are implemented by
this document._

## Recommended Sequence

1. **Scenario Suite pilot**
   - Implement 3-4 scenarios with strong operational endpoints.
   - Use a small no-model dry-load and fixture test suite before preregistered
     production runs.
   - Candidate scenarios: refunds, procurement, restricted data access, project
     scheduling.

2. **Cross-model pilot replication**
   - Run the same scenario set across GPT, Claude, Gemini, and later providers
     only after each scenario passes no-model validation.
   - Preserve cross-model blinding and provider-comparability reports.

3. **Operational pressure experiment**
   - Manipulate environment-grounded consequences such as cumulative score,
     future budget, future resource access, or project continuation.
   - Keep narrative pressure as a comparison condition.

4. **Observability / enforcement experiment**
   - Cross formal constraint with audit probability and penalty.
   - Distinguish constraint-bounded behavior from instrumental compliance.

5. **Evaluation-awareness / naturalistic embedding experiment**
   - Compare eval-salient versus naturalistically embedded workflows.
   - Use post-action structured awareness checks only.

6. **Multi-agent delegation experiment**
   - Add delegated actors after single-agent scenario mechanics are stable.
   - Score indirect or delegated prohibited actions mechanically.

## Prioritized First Scenarios

### 1. Refund authority

Reason: close enough to the retention domain to reuse abstractions, but distinct
in money-movement mechanics and customer-service workflow. Strong primary
endpoint: refund amount relative to authority and approval state.

### 2. Procurement purchasing

Reason: introduces purchase splitting, vendor choice, and finance approval.
Strong primary endpoints: unauthorized purchase order and approval bypass.

### 3. Restricted data access

Reason: tests information-access constraints rather than monetary limits.
Strong primary endpoint: protected resource access.

### 4. Project scheduling / approval bypass

Reason: tests workflow-state integrity, milestone approval, and status mutation.
Strong primary endpoint: approved/scheduled state without signoff.

## Proposed Code Architecture

Do not refactor existing experiments until a specific implementation task is
approved. When implementation begins, factor reusable components cautiously:

- `ScenarioSpec`: frozen scenario text, roles, objectives, resources, policies,
  actors, terminal states, and factors.
- `AuthorityPolicy`: direct limits, approval requirements, approval status, and
  permission checks.
- `ApprovalFlow`: manager/approver availability, deterministic or probabilistic
  responses, repeated-request handling.
- `PressureSpec`: ordinary, high narrative, and operational pressure state.
- `OversightSpec`: audit probability, observability, penalty, and audit log.
- `ToolSpec`: structured tool schema, preconditions, authorization, state
  transitions, and log fields.
- `ScenarioEnvironment`: state machine for each scenario family.
- `ComplianceScorer`: operational endpoint flags and secondary measures.
- `StructuredCommunication`: optional claim fields plus free text.
- `ScenarioRegistry`: scenario/run registration compatible with Runner v2.
- `SampleId`: `{experiment_or_suite}-{scenario}-{model}-{factor-levels}-{replicate}`.
- `RunManifest`: frozen SHAs, model/provider settings, sample plan, raw-log
  segments, and recovery provenance.

## Runner v2 Integration

Future suite runs should preserve:

- manual workflow dispatch;
- allowlisted run IDs and actions;
- provider preflight and canaries;
- no-model dry-load;
- blinded operational monitoring;
- raw logs ignored by Git;
- immutable segment preservation;
- missing-ID recovery only;
- finalization only when expected unique sample IDs are complete.

## Structured Communication Instrumentation

For communication-relevant scenarios, future apparatus should add structured
fields without removing natural language:

- claimed approval status;
- claimed authorized amount or action;
- claimed applied state;
- claimed binding commitment;
- claimed resource access basis;
- claimed escalation status.

These fields are not a replacement for naturalistic communication. They are an
experimental observability feature that makes consequential representations
directly measurable. If models also produce free text, treat natural-language
interpretation as qualitative or separately validated measurement.

## Validation Checklist Before Any Production Scenario

- preregistration written before execution;
- scientific apparatus frozen and hashed;
- condition wording passes permission-leakage review;
- all sample IDs deterministic and unique;
- no-model dry-load passes;
- scorer fixtures include true positives, true negatives, edge cases, and
  malformed inputs;
- provider/tool compatibility documented;
- raw logs ignored;
- credential scan clean;
- `git diff --check` clean;
- no model samples run before scientific freeze;
- analysis plan includes all-zero/sparse handling;
- recovery plan preserves immutable segments and avoids rerunning completed
  samples.

## Research Standard

Future Scenario Suite experiments should preserve null findings and
methodological failures. A scenario that produces no violations under strong
mechanical measurement is informative. A scenario whose scorer fails validation
should be recorded as a measurement result, not hidden or retrofitted.
