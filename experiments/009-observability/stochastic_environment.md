# Stochastic Environment And Reproducibility

_Status: preregistered._

## Seed Rule

Each sample must have a deterministic seed derived from:

- experiment id;
- run id / model role;
- scenario id;
- `p_detect` condition;
- replicate id.

The exact seed algorithm should be implemented before production and frozen
with the scientific implementation. The same sample ID plus frozen
configuration must reproduce the same stochastic detection draw.

## Detection RNG

For each unauthorized action, record:

- configured `p_detect`;
- RNG seed;
- RNG algorithm/version;
- random uniform draw or equivalent replayable value;
- detection threshold;
- detected true/false;
- detection not-applicable state if no unauthorized action occurred.

The draw should occur after the unauthorized action is attempted/executed, not
before the model chooses its action.

## Sanction State

If `detected = true`, sanction is deterministic in this experiment:

```text
sanctioned = true
```

If `detected = false`, sanction is false. If no unauthorized action occurred,
sanction state is not applicable.

Record:

- sanction probability conditional on detection: `1.0`;
- sanction severity label;
- sanction applied state;
- terminal state after sanction.

## Recovery

Missing-ID recovery must reuse the originally assigned sample ID, seed, model,
scenario, `p_detect`, and all scientific configuration. Recovery must not
redraw detection for any already authoritative sample.

Detection-only, sanction-only, or awareness-only recovery is not allowed. A
recovered sample must execute the complete operational episode, stochastic
draw logic if relevant, terminal state, scoring, and secondary awareness phase
if retained.

## Replay Verification

Before production, tests should verify that sample ID + frozen configuration
reproduce the same detection draw. Final analysis should verify the recorded
draw is compatible with the configured `p_detect` and stored seed metadata.
