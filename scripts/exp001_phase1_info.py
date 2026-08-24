from __future__ import annotations

import json

from artificial_agency.experiments.exp001.config import (
    CONDITIONS,
    ENVIRONMENT_VERSION,
    EXPERIMENT_ID,
    MAX_ACTION_STEPS,
    PHASE1_REPLICATES_PER_CONDITION,
    PROMPT_VERSION,
)
from artificial_agency.experiments.exp001.inspect_task import phase1_samples


def main() -> None:
    samples = phase1_samples()
    payload = {
        "experiment_id": EXPERIMENT_ID,
        "environment_version": ENVIRONMENT_VERSION,
        "prompt_version": PROMPT_VERSION,
        "conditions": list(CONDITIONS),
        "replicates_per_condition": PHASE1_REPLICATES_PER_CONDITION,
        "sample_count": len(samples),
        "max_action_steps": MAX_ACTION_STEPS,
        "sample_ids": [sample.id for sample in samples],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

