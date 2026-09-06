# Recovery Semantics

## Atomic Sequence Rule

The authoritative recovery unit is the full 10-episode sequence.

If a sequence fails technically at any point, including Episode 7, do not
combine Episodes 1-6 from one execution with Episodes 7-10 from another.

Preferred recovery:

- preserve the failed partial execution as non-authoritative provenance;
- rerun the entire sequence from the original sequence ID, seed, model,
  pressure condition, scenario, and replicate;
- do not rerun a sequence that is already authoritative and complete.

## No Partial Awareness Recovery

Do not perform awareness-only recovery. A recovered sequence must execute the
complete Phase A operational sequence and the Phase B post-sequence awareness
measurement.

## Deterministic Seeds

Assign one deterministic sequence-level seed.

If stochastic mechanics are later implemented inside the sequence, episode
stochastic events must derive from:

- sequence seed;
- episode index;
- event type.

Recovery must reproduce the same stochastic environment given the same event
path.

## Missing-Sequence Recovery

Missing-ID recovery selects missing sequence IDs only. It must never rerun an
authoritative completed sequence.

Runtime recovery metadata must distinguish:

- authoritative completed sequences;
- failed partial sequences;
- recovered authoritative sequences;
- excluded provenance-only attempts.
