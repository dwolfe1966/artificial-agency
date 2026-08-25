from __future__ import annotations

RUNNER_LABELS = ("self-hosted", "macOS", "artificial-agency")
SUPPORTED_ACTIONS = ("start", "status", "health", "stop", "resume", "finalize")


def runner_command(action: str, run_id: str) -> list[str]:
    if action not in SUPPORTED_ACTIONS:
        raise ValueError(f"Unsupported action: {action}")
    if run_id != "002A":
        raise ValueError(f"Unsupported run_id: {run_id}")
    return [
        ".venv/bin/python",
        "-m",
        "artificial_agency.runner",
        action,
        run_id,
    ]
