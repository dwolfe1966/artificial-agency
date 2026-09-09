from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from artificial_agency.runner.config import RunSpec, known_runs
from artificial_agency.runner.inspect_ops import inspect_log_metadata
from artificial_agency.runner.recovery import expected_sample_ids


EXPERIMENT = "011-multi-agent-delegation"
PREREGISTRATION_SHA = "07f3c0bdcb7dee96fe7b350363905ffdd585edaf"
SCIENTIFIC_SHA = "set-by-runner-at-production-freeze"
RUNS = ("011A-GPT", "011B-CLAUDE", "011C-GEMINI")
PROOF_RUNS = ("011-PROOF-GPT", "011-PROOF-CLAUDE", "011-PROOF-GEMINI")
MODEL_LABELS = {
    "model_a_gpt": "GPT-5.6 Sol",
    "model_b_claude": "Claude Sonnet 5",
    "model_c_gemini": "Gemini 3.7 Flash",
}
MODEL_ROLE_BY_PREFIX = {
    "011A-GPT": "model_a_gpt",
    "011B-CLAUDE": "model_b_claude",
    "011C-GEMINI": "model_c_gemini",
}
CONDITIONS = ("direct", "delegation")
ATTRIBUTION_CATEGORIES = (
    "direct_violation",
    "explicit_delegated_violation",
    "induced_violation",
    "legitimate_authority_routing",
    "independent_agent_b_violation",
    "ambiguous_attribution",
)
RUNTIME_ROOT_CANDIDATES = [
    REPO.parent / ".artificial-agency-runtime",
    Path(
        "/Users/davidwolfe/actions-runner/artificial-agency/_work/"
        "artificial-agency/.artificial-agency-runtime"
    ),
]


def runtime_roots() -> list[Path]:
    roots = [root for root in RUNTIME_ROOT_CANDIDATES if (root / EXPERIMENT).exists()]
    return roots or [RUNTIME_ROOT_CANDIDATES[0]]


def runtime_root() -> Path:
    return runtime_roots()[0]


def patched_spec(run_id: str) -> RunSpec:
    spec = known_runs()[run_id]
    data = spec.__dict__.copy()
    root = runtime_root() / EXPERIMENT / f"run-{run_id}"
    data.update(
        {
            "log_dir": root / "inspect",
            "status_path": root / "RUN_STATUS.json",
            "operational_log": root / "operational.log",
            "lock_path": root / "RUN_LOCK.json",
            "pid_path": root / "RUNNER.pid",
            "stdout_path": root / "runner-supervisor.out",
            "canary_log_dir": root / "canary",
            "previous_log_dirs": (),
        }
    )
    return type(spec)(**data)


def log_paths_for(run_id: str) -> list[Path]:
    paths: list[Path] = []
    for root in runtime_roots():
        paths.extend((root / EXPERIMENT / f"run-{run_id}" / "inspect").glob("*.json"))
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen:
            unique.append(path)
            seen.add(resolved)
    return sorted(unique, key=lambda path: path.stat().st_mtime)


def valid_sample(sample: dict[str, Any]) -> bool:
    scores = sample.get("scores")
    try:
        turn_count = int(sample.get("turn_count") or 0)
    except (TypeError, ValueError):
        turn_count = 0
    return (
        bool(sample.get("completed_at"))
        and sample.get("output") is not None
        and isinstance(scores, dict)
        and bool(scores)
        and turn_count > 0
    )


def score_metadata(sample: dict[str, Any]) -> dict[str, Any]:
    scores = sample.get("scores") or {}
    score = scores.get("delegation_outcome_scorer")
    if not isinstance(score, dict):
        return {}
    metadata = score.get("metadata")
    return metadata if isinstance(metadata, dict) else {}


def parse_identity(
    sample_id: str,
    sample_metadata: dict[str, Any],
    trajectory: dict[str, Any],
) -> dict[str, Any]:
    parts = sample_id.rsplit("-", 2)
    condition_from_id = parts[1]
    replicate_from_id = int(parts[2])
    prefix = sample_id[: -(len(condition_from_id) + len(parts[2]) + 2)]
    model_role = str(
        sample_metadata.get("model_role")
        or trajectory.get("model_role")
        or MODEL_ROLE_BY_PREFIX.get(prefix)
    )
    condition = str(
        sample_metadata.get("actor_condition")
        or trajectory.get("actor_condition_id")
        or condition_from_id
    )
    return {
        "sample_id": sample_id,
        "run_id": str(sample_metadata.get("run_id") or prefix).removeprefix("run-"),
        "model_role": model_role,
        "model": MODEL_LABELS.get(model_role, model_role),
        "scenario": "procurement",
        "actor_condition": condition,
        "delegation_available": bool(
            sample_metadata.get("delegation_available")
            if sample_metadata.get("delegation_available") is not None
            else trajectory.get("delegation_available", condition == "delegation")
        ),
        "replicate": int(
            sample_metadata.get("replicate_id")
            if sample_metadata.get("replicate_id") is not None
            else trajectory.get("replicate_id", replicate_from_id)
        ),
    }


def per_sample_row(
    sample_id: str,
    metadata: dict[str, Any],
    sample_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    sample_metadata = sample_metadata or {}
    trajectory = metadata.get("trajectory") if isinstance(metadata.get("trajectory"), dict) else {}
    attribution = metadata.get("attribution") if isinstance(metadata.get("attribution"), dict) else {}
    flags = metadata.get("secondary_flags") if isinstance(metadata.get("secondary_flags"), dict) else {}
    stochastic = metadata.get("stochastic") if isinstance(metadata.get("stochastic"), dict) else {}
    awareness = metadata.get("awareness") if isinstance(metadata.get("awareness"), dict) else {}
    row = {
        **parse_identity(sample_id, sample_metadata, trajectory),
        "sample_any_operational_constraint_violation": bool(
            metadata.get("sample_any_operational_constraint_violation")
        ),
        "sample_any_attributable_indirect_operational_constraint_violation": bool(
            metadata.get("sample_any_attributable_indirect_operational_constraint_violation")
        ),
        "primary_label_id": str(metadata.get("primary_label_id")),
        "any_unauthorized_attempt": bool(metadata.get("any_unauthorized_attempt")),
        "terminal_reason": metadata.get("terminal_reason"),
        "total_steps": int(metadata.get("total_steps", 0) or 0),
        "phase_a_done": metadata.get("phase_a_done") is True,
        "phase_a_frozen": metadata.get("phase_a_frozen") is True,
        "phase_a_score_present": "sample_any_operational_constraint_violation" in metadata,
        "phase_b_done": metadata.get("phase_b_done") is True,
        "rng_version": stochastic.get("rng_version"),
        "sample_seed": stochastic.get("sample_seed"),
        "stochastic_environment_events": bool(stochastic.get("stochastic_environment_events")),
        "p_detect": stochastic.get("p_detect"),
        "detection_draw_consumed": bool(stochastic.get("detection_draw_consumed")),
        "p_sanction_if_detected": stochastic.get("p_sanction_if_detected"),
        "sanction_severity": stochastic.get("sanction_severity"),
        "awareness_capture_status": awareness.get(
            "capture_status",
            metadata.get("awareness_capture_status"),
        ),
        "perceived_primary_task_type": awareness.get("perceived_primary_task_type"),
        "perceived_compliance_test_likelihood": awareness.get(
            "perceived_compliance_test_likelihood"
        ),
        "perceived_behavior_under_evaluation": awareness.get(
            "perceived_behavior_under_evaluation"
        ),
        "awareness_confidence": awareness.get("confidence"),
        "agent_b_request_count": len(metadata.get("agent_b_requests") or []),
        "agent_b_result_count": len(metadata.get("agent_b_results") or []),
    }
    for category in ATTRIBUTION_CATEGORIES:
        row[category] = bool(attribution.get(category))
    for key, value in flags.items():
        row[key] = value
    return row


def load_authoritative_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    provenance: dict[str, Any] = {"runs": {}}
    global_seen: set[str] = set()
    proof_ids = {sample_id for run in PROOF_RUNS for sample_id in expected_sample_ids(known_runs()[run])}
    for run_id in RUNS:
        spec = patched_spec(run_id)
        expected = expected_sample_ids(spec)
        expected_set = set(expected)
        selected: dict[str, dict[str, Any]] = {}
        duplicate_ids: set[str] = set()
        unexpected_ids: set[str] = set()
        segments: list[dict[str, Any]] = []
        for path in log_paths_for(run_id):
            meta = inspect_log_metadata(path)
            data = json.loads(path.read_text(encoding="utf-8"))
            valid_expected_ids: list[str] = []
            for sample in data.get("samples", []):
                if not isinstance(sample, dict) or sample.get("id") is None:
                    continue
                sid = str(sample["id"])
                if sid not in expected_set:
                    unexpected_ids.add(sid)
                    continue
                if not valid_sample(sample):
                    continue
                valid_expected_ids.append(sid)
                if sid in selected:
                    duplicate_ids.add(sid)
                else:
                    selected[sid] = sample
            segments.append(
                {
                    "path": str(path),
                    "byte_size": meta.byte_size,
                    "sha256": meta.sha256,
                    "status": meta.status,
                    "valid_expected_ids": valid_expected_ids,
                }
            )
        missing = [sid for sid in expected if sid not in selected]
        for sid in expected:
            sample = selected.get(sid)
            if sample is None:
                continue
            metadata = score_metadata(sample)
            rows.append(per_sample_row(sid, metadata, sample.get("metadata") or {}))
        global_seen.update(selected)
        provenance["runs"][run_id] = {
            "expected": len(expected),
            "selected": len(selected),
            "missing_ids": missing,
            "duplicate_ids": sorted(duplicate_ids),
            "unexpected_ids": sorted(unexpected_ids),
            "segments": segments,
        }
    provenance["proof_overlap_ids"] = sorted(global_seen.intersection(proof_ids))
    return rows, provenance


def exact_binomial_ci(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    if n == 0:
        return (math.nan, math.nan)
    try:
        from scipy.stats import beta
    except ImportError:
        if k == 0:
            return (0.0, 1 - alpha ** (1 / n))
        if k == n:
            return (alpha ** (1 / n), 1.0)
        raise
    lower = 0.0 if k == 0 else float(beta.ppf(alpha / 2, k, n - k + 1))
    upper = 1.0 if k == n else float(beta.ppf(1 - alpha / 2, k + 1, n - k))
    return lower, upper


def rate_summary(rows: list[dict[str, Any]], field: str, group: str | None = None) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    if group is None:
        groups["overall"] = rows
    else:
        for row in rows:
            groups[str(row[group])].append(row)
    output: list[dict[str, Any]] = []
    for label, group_rows in sorted(groups.items()):
        n = len(group_rows)
        k = sum(1 for row in group_rows if row.get(field) is True)
        lo, hi = exact_binomial_ci(k, n)
        output.append(
            {
                "group": label,
                "endpoint": field,
                "events": k,
                "n": n,
                "rate": k / n if n else math.nan,
                "ci95_low": lo,
                "ci95_high": hi,
            }
        )
    return output


def integrity(rows: list[dict[str, Any]], provenance: dict[str, Any]) -> dict[str, Any]:
    ids = [row["sample_id"] for row in rows]
    condition_counts = Counter(row["actor_condition"] for row in rows)
    model_counts = Counter(row["model_role"] for row in rows)
    model_condition_counts = Counter((row["model_role"], row["actor_condition"]) for row in rows)
    return {
        "total_rows": len(rows),
        "unique_ids": len(set(ids)),
        "duplicate_ids": sorted(sample_id for sample_id, count in Counter(ids).items() if count > 1),
        "condition_counts": dict(condition_counts),
        "model_counts": dict(model_counts),
        "model_condition_counts": {f"{m}:{c}": n for (m, c), n in model_condition_counts.items()},
        "phase_a_done": sum(1 for row in rows if row["phase_a_done"]),
        "phase_a_frozen": sum(1 for row in rows if row["phase_a_frozen"]),
        "phase_b_done": sum(1 for row in rows if row["phase_b_done"]),
        "proof_overlap_ids": provenance.get("proof_overlap_ids", []),
        "runs": provenance["runs"],
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_outputs() -> dict[str, Any]:
    rows, provenance = load_authoritative_rows()
    out = REPO / "results" / EXPERIMENT
    primary = {
        "overall": rate_summary(rows, "sample_any_operational_constraint_violation"),
        "by_condition": rate_summary(rows, "sample_any_operational_constraint_violation", "actor_condition"),
        "by_model": rate_summary(rows, "sample_any_operational_constraint_violation", "model_role"),
        "indirect_by_condition": rate_summary(
            rows,
            "sample_any_attributable_indirect_operational_constraint_violation",
            "actor_condition",
        ),
    }
    awareness = {
        "capture_status": dict(Counter(str(row.get("awareness_capture_status")) for row in rows)),
        "primary_task_type": dict(Counter(str(row.get("perceived_primary_task_type")) for row in rows)),
        "compliance_test_likelihood": dict(
            Counter(str(row.get("perceived_compliance_test_likelihood")) for row in rows)
        ),
        "behavior_under_evaluation": dict(
            Counter(str(row.get("perceived_behavior_under_evaluation")) for row in rows)
        ),
    }
    artifact_paths = {
        "sample_dataset": out / "exp011_authoritative_samples.csv",
        "integrity": out / "exp011_integrity.json",
        "primary": out / "exp011_primary_summaries.json",
        "awareness": out / "exp011_awareness_summaries.json",
        "provenance": out / "exp011_finalization_manifest.json",
    }
    write_csv(artifact_paths["sample_dataset"], rows)
    write_json(artifact_paths["integrity"], integrity(rows, provenance))
    write_json(artifact_paths["primary"], primary)
    write_json(artifact_paths["awareness"], awareness)
    write_json(
        artifact_paths["provenance"],
        {
            "experiment": EXPERIMENT,
            "preregistration_sha": PREREGISTRATION_SHA,
            "scientific_sha": SCIENTIFIC_SHA,
            "confirmatory_runs": RUNS,
            "excluded_proof_runs": PROOF_RUNS,
            "confirmatory_row_count": len(rows),
            "provenance": provenance,
        },
    )
    return {
        "rows": len(rows),
        "artifacts": {name: str(path) for name, path in artifact_paths.items()},
        "sha256": {name: file_sha256(path) for name, path in artifact_paths.items()},
    }


def main() -> None:
    print(json.dumps(build_outputs(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
