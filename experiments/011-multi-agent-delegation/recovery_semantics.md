# Recovery Semantics

Each complete Agent A procurement interaction is atomic.

If a sample fails technically:

- preserve the failed execution as provenance-only;
- rerun the complete sample from the original sample ID, condition, model,
  replicate, and seed/configuration if any;
- do not combine Agent A actions from one execution with Agent B actions from
  another;
- do not splice partial tool traces or awareness phases;
- do not rerun an already authoritative complete sample.

Agent B interactions are embedded inside the sample. Recovery therefore covers
the full Agent A and Agent B interaction together.

Any proof, dry-run, or exploratory samples must be explicitly excluded from
confirmatory analysis.
