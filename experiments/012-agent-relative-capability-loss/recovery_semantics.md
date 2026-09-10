# Recovery Semantics

Recovery is sequence-atomic.

An authoritative sequence must come from one complete 8-episode execution.

If a sequence fails technically at episode `k`:

- the partial execution is preserved as provenance-only;
- the authoritative sequence remains missing;
- recovery reruns the whole sequence from Episode 1;
- the same sequence ID, model, condition, replicate, and seed/configuration are used;
- episodes from different executions are never spliced into one authoritative sequence.

Do not rerun a complete authoritative sequence.
