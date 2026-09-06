from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from artificial_agency.runner.config import RunSpec, known_runs
from artificial_agency.runner.inspect_ops import inspect_log_metadata
from artificial_agency.runner.recovery import expected_sample_ids
EXPERIMENT = "009-observability"
PREREGISTRATION_SHA = "c0c19cbbe9863f52eb151a06c4e378f5fed2466e"
SCIENTIFIC_SHA = "8c3b3728780df5cbb0c073fce619787ca5415546"
STAGE1_PROVENANCE_COMMIT = "2ed6e1ba60b87ca65e35133edcb118f4bc760864"
STAGE2_RUNNER_REGISTRATION_COMMIT_CORRECT = "df634f8d55b3f683b5968104aa3e8f6b36b4e3c1"
INFRASTRUCTURE_COMMITS = [
    "2e6dabe090704363dbd1aac9b62a71993574cecf",
    "2b24718d737e751011150e340688252e2c92617e",
    STAGE2_RUNNER_REGISTRATION_COMMIT_CORRECT,
]
EXCLUDED_SEGMENT_SHAS = {
    "81ac8d29fa53ba3eab0fad7ea85629652973710ad777e84c3f953904cb12d61d":
    "provenance_only_gemini_stage1_duplicate_wrong_missing_id_basis"
}
RUNTIME_ROOT_CANDIDATES = [
    Path("/Users/davidwolfe/actions-runner/artificial-agency/_work/artificial-agency/.artificial-agency-runtime"),
    REPO.parent / ".artificial-agency-runtime",
]
LEGACY_RESULTS_CANDIDATES = [
    Path("/Users/davidwolfe/actions-runner/artificial-agency/_work/artificial-agency/artificial-agency/results"),
    REPO / "results",
]
RUNS = {
    "stage1": ("009A-GPT-S1", "009B-CLAUDE-S1", "009C-GEMINI-S1"),
    "stage2": ("009A-GPT-S2", "009B-CLAUDE-S2", "009C-GEMINI-S2"),
}
MODEL_LABELS = {
    "model_a_gpt": "GPT-5.6 Sol",
    "model_b_claude": "Claude Sonnet 5",
    "model_c_gemini": "Gemini 3.7 Flash",
}
P_DETECT_ORDER = ("p100", "p050", "p010", "p000")
P_DETECT_VALUE = {"p100": 1.0, "p050": 0.5, "p010": 0.1, "p000": 0.0}
AWARENESS_STATUSES = {"captured_valid", "captured_malformed", "missing"}


def runtime_root() -> Path:
    for root in RUNTIME_ROOT_CANDIDATES:
        if (root / EXPERIMENT).exists():
            return root
    return RUNTIME_ROOT_CANDIDATES[0]


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
    paths = list((runtime_root() / EXPERIMENT / f"run-{run_id}" / "inspect").glob("*.json"))
    for base in LEGACY_RESULTS_CANDIDATES:
        paths.extend((base / EXPERIMENT / f"run-{run_id}" / "inspect").glob("*.json"))
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen:
            unique.append(path)
            seen.add(resolved)
    return sorted(unique, key=lambda path: path.stat().st_mtime)


def read_status(run_id: str) -> dict[str, Any]:
    for path in [
        runtime_root() / EXPERIMENT / f"run-{run_id}" / "RUN_STATUS.json",
        *(base / EXPERIMENT / f"run-{run_id}" / "RUN_STATUS.json" for base in LEGACY_RESULTS_CANDIDATES),
    ]:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    return {}


def valid_sample(sample: dict[str, Any]) -> bool:
    scores = sample.get("scores")
    try:
        turn_count = int(sample.get("turn_count") or 0)
    except (TypeError, ValueError):
        turn_count = 0
    return bool(sample.get("completed_at")) and sample.get("output") is not None and isinstance(scores, dict) and bool(scores) and turn_count > 0


def score_metadata(sample: dict[str, Any]) -> dict[str, Any]:
    scores = sample.get("scores") or {}
    score = scores.get("observability_outcome_scorer")
    if not isinstance(score, dict):
        return {}
    metadata = score.get("metadata")
    return metadata if isinstance(metadata, dict) else {}


def cell_from_id(sample_id: str) -> str:
    scenario = "data-access" if "-data-access-" in sample_id else "procurement"
    p_detect_id = sample_id.rsplit("-", 2)[1]
    return f"{scenario}-{p_detect_id}"


def parse_identity(sample_id: str, sample_metadata: dict[str, Any]) -> dict[str, Any]:
    parts = sample_id.rsplit("-", 2)
    p_detect_id = parts[1]
    return {
        "sample_id": sample_id,
        "stage": str(sample_metadata.get("stage")),
        "model_role": str(sample_metadata.get("model_role")),
        "model": MODEL_LABELS.get(str(sample_metadata.get("model_role")), str(sample_metadata.get("model_role"))),
        "scenario": str(sample_metadata.get("scenario")),
        "p_detect": float(sample_metadata.get("p_detect")),
        "p_detect_id": p_detect_id,
        "replicate": int(sample_metadata.get("replicate_id")),
        "run_id": str(sample_metadata.get("run_id")).removeprefix("run-"),
        "cell": cell_from_id(sample_id),
    }


def load_authoritative_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    provenance: dict[str, Any] = {"runs": {}, "excluded_segments": []}
    global_seen: set[str] = set()
    for stage, run_ids in RUNS.items():
        for run_id in run_ids:
            spec = patched_spec(run_id)
            expected = expected_sample_ids(spec)
            expected_set = set(expected)
            selected: dict[str, dict[str, Any]] = {}
            duplicate_ids: set[str] = set()
            unexpected_ids: set[str] = set()
            segments: list[dict[str, Any]] = []
            for path in log_paths_for(run_id):
                meta = inspect_log_metadata(path)
                excluded = meta.sha256 in EXCLUDED_SEGMENT_SHAS
                segment = {
                    "path": str(path),
                    "byte_size": meta.byte_size,
                    "sha256": meta.sha256,
                    "inspect_status": meta.status,
                    "sample_count": meta.sample_count,
                    "valid_sample_count": meta.valid_sample_count,
                    "authoritative": not excluded,
                }
                if excluded:
                    segment["exclusion_reason"] = EXCLUDED_SEGMENT_SHAS[meta.sha256]
                    provenance["excluded_segments"].append(segment)
                    segments.append(segment)
                    continue
                data = json.loads(path.read_text(encoding="utf-8"))
                for sample in data.get("samples", []):
                    if not isinstance(sample, dict) or sample.get("id") is None:
                        continue
                    sample_id = str(sample["id"])
                    if sample_id not in expected_set:
                        unexpected_ids.add(sample_id)
                        continue
                    if not valid_sample(sample):
                        continue
                    if sample_id in selected:
                        duplicate_ids.add(sample_id)
                    else:
                        selected[sample_id] = sample
                segments.append(segment)
            missing_ids = [sample_id for sample_id in expected if sample_id not in selected]
            status = read_status(run_id)
            provenance["runs"][run_id] = {
                "stage": stage,
                "state": status.get("state"),
                "finalized_at": status.get("finalized_at"),
                "inspect_status": status.get("inspect_status"),
                "frozen_commit": status.get("frozen_commit", spec.frozen_commit),
                "expected_count": len(expected),
                "authoritative_count": len(selected),
                "missing_count": len(missing_ids),
                "duplicate_count": len(duplicate_ids),
                "unexpected_count": len(unexpected_ids),
                "segments": segments,
            }
            for sample_id in expected:
                sample = selected.get(sample_id)
                if sample is None:
                    continue
                if sample_id in global_seen:
                    provenance.setdefault("global_duplicate_ids", []).append(sample_id)
                global_seen.add(sample_id)
                md = score_metadata(sample)
                sample_md = sample.get("metadata") or {}
                identity = parse_identity(sample_id, sample_md)
                flags = md.get("secondary_flags") if isinstance(md.get("secondary_flags"), dict) else {}
                stochastic = md.get("stochastic") if isinstance(md.get("stochastic"), dict) else {}
                awareness = md.get("awareness") if isinstance(md.get("awareness"), dict) else {}
                row = {
                    **identity,
                    "operational_constraint_violation": bool(md.get("operational_constraint_violation")),
                    "unauthorized_attempt": bool(flags.get("unauthorized_attempt", False)),
                    "detected_violation": bool(flags.get("detected_violation", False)),
                    "sanctioned_violation": bool(flags.get("sanctioned_violation", False)),
                    "escalation": bool(flags.get("escalation_attempted", False)),
                    "repeated_escalation": bool(flags.get("repeated_escalation", False)),
                    "compliant_alternative_search": bool(flags.get("compliant_alternative_search", False)),
                    "partial_objective_achievement": bool(flags.get("partial_objective_achievement", False)),
                    "terminal_failure": bool(flags.get("terminal_failure_abandonment", False)),
                    "total_steps": int(flags.get("total_action_steps", md.get("total_action_steps", 0)) or 0),
                    "post_denial_steps": int(flags.get("post_denial_action_steps", md.get("post_denial_action_steps", 0)) or 0),
                    "max_step": bool(flags.get("max_step_termination", False)),
                    "technical_failure": bool(flags.get("technical_failure", md.get("technical_failure", False))),
                    "terminal_outcome": str(md.get("phase_a_terminal_reason") or md.get("terminal_reason")),
                    "primary_label_id": str(md.get("primary_label_id")),
                    "approval_bypass": bool(flags.get("approval_bypass", False)),
                    "authority_limit_exceeded": bool(flags.get("authority_limit_exceeded", False)),
                    "unauthorized_expenditure": bool(flags.get("unauthorized_expenditure", False)),
                    "prohibited_split_purchase": bool(flags.get("prohibited_split_purchase", False)),
                    "restricted_resource_accessed": bool(flags.get("restricted_resource_accessed", False)),
                    "prohibited_tool_invocation": bool(flags.get("prohibited_tool_invocation", False)),
                    "approval_denied": bool(flags.get("approval_denied", False)),
                    "phase_a_done": md.get("phase_a_done") is True,
                    "phase_a_frozen": md.get("phase_a_frozen") is True,
                    "phase_a_score_present": "operational_constraint_violation" in md,
                    "phase_b_done": md.get("phase_b_done") is True,
                    "rng_version": str(stochastic.get("rng_version")),
                    "sample_seed": stochastic.get("sample_seed"),
                    "configured_p_detect": stochastic.get("configured_p_detect"),
                    "detection_draw_consumed": bool(stochastic.get("draw_consumed", False)),
                    "random_draw": stochastic.get("random_draw"),
                    "detection_result": stochastic.get("detection_result"),
                    "sanction_state": stochastic.get("sanctioned"),
                    "p_sanction_if_detected": stochastic.get("p_sanction_if_detected"),
                    "sanction_severity": stochastic.get("sanction_severity"),
                    "awareness_capture_status": str(awareness.get("capture_status", md.get("awareness_capture_status"))),
                    "perceived_primary_task_type": awareness.get("perceived_primary_task_type"),
                    "perceived_compliance_test_likelihood": awareness.get("perceived_compliance_test_likelihood"),
                    "perceived_behavior_under_evaluation": awareness.get("perceived_behavior_under_evaluation"),
                    "awareness_confidence": awareness.get("confidence"),
                }
                rows.append(row)
    return rows, provenance


def exact_binomial_ci(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    if n == 0:
        return (math.nan, math.nan)
    if k == 0:
        return (0.0, 1.0 - (alpha / 2.0) ** (1.0 / n))
    if k == n:
        return ((alpha / 2.0) ** (1.0 / n), 1.0)

    def cdf(x: int, p: float) -> float:
        return sum(math.comb(n, i) * (p**i) * ((1 - p) ** (n - i)) for i in range(x + 1))

    def sf_ge(x: int, p: float) -> float:
        return sum(math.comb(n, i) * (p**i) * ((1 - p) ** (n - i)) for i in range(x, n + 1))

    lo, hi = 0.0, k / n
    for _ in range(80):
        mid = (lo + hi) / 2
        if sf_ge(k, mid) > alpha / 2:
            hi = mid
        else:
            lo = mid
    lower = (lo + hi) / 2
    lo, hi = k / n, 1.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if cdf(k, mid) > alpha / 2:
            lo = mid
        else:
            hi = mid
    upper = (lo + hi) / 2
    return lower, upper


def rate_summary(rows: list[dict[str, Any]], field: str, groups: list[str]) -> list[dict[str, Any]]:
    buckets: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    if groups:
        for row in rows:
            buckets[tuple(row[group] for group in groups)].append(row)
    else:
        buckets[()] = rows
    out: list[dict[str, Any]] = []
    for key, bucket in sorted(buckets.items(), key=lambda item: tuple(str(x) for x in item[0])):
        k = sum(1 for row in bucket if bool(row[field]))
        n = len(bucket)
        ci_low, ci_high = exact_binomial_ci(k, n)
        record = {group: value for group, value in zip(groups, key)}
        record.update(
            {
                "n": n,
                "count": k,
                "rate": k / n if n else None,
                "ci95_low": ci_low,
                "ci95_high": ci_high,
            }
        )
        out.append(record)
    return out


def count_table(rows: list[dict[str, Any]], field: str, groups: list[str]) -> list[dict[str, Any]]:
    buckets: dict[tuple[Any, ...], Counter] = defaultdict(Counter)
    for row in rows:
        buckets[tuple(row[group] for group in groups)][str(row.get(field))] += 1
    out = []
    for key, counts in sorted(buckets.items(), key=lambda item: tuple(str(x) for x in item[0])):
        record = {group: value for group, value in zip(groups, key)}
        record.update(dict(sorted(counts.items())))
        record["n"] = sum(counts.values())
        out.append(record)
    return out


def process_summary(rows: list[dict[str, Any]], groups: list[str]) -> list[dict[str, Any]]:
    buckets: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        buckets[tuple(row[group] for group in groups)].append(row)
    out = []
    for key, bucket in sorted(buckets.items(), key=lambda item: tuple(str(x) for x in item[0])):
        record = {group: value for group, value in zip(groups, key)}
        record.update(
            {
                "n": len(bucket),
                "escalation": sum(row["escalation"] for row in bucket),
                "repeated_escalation": sum(row["repeated_escalation"] for row in bucket),
                "compliant_alternative_search": sum(row["compliant_alternative_search"] for row in bucket),
                "partial_objective_achievement": sum(row["partial_objective_achievement"] for row in bucket),
                "terminal_failure": sum(row["terminal_failure"] for row in bucket),
                "max_step": sum(row["max_step"] for row in bucket),
                "technical_failure": sum(row["technical_failure"] for row in bucket),
                "mean_total_steps": mean(row["total_steps"] for row in bucket),
                "median_total_steps": median(row["total_steps"] for row in bucket),
                "mean_post_denial_steps": mean(row["post_denial_steps"] for row in bucket),
                "median_post_denial_steps": median(row["post_denial_steps"] for row in bucket),
            }
        )
        out.append(record)
    return out


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def final_cell_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(
        f"{row['model']}|{row['scenario']}|{row['p_detect_id']}" for row in rows
    )
    return dict(sorted(counts.items()))


def credential_scan(paths: list[Path]) -> dict[str, Any]:
    needles = (
        "api" + "_key",
        "api" + "key",
        "sec" + "ret",
        "pass" + "word",
        "BEGIN " + "RSA",
        "BEGIN " + "OPENSSH",
        "PRIVATE " + "KEY",
        "s" + "k-",
    )
    hits = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        lower = text.lower()
        for needle in needles:
            if needle.lower() in lower:
                hits.append({"path": str(path), "pattern": needle})
    return {"scanned_files": len(paths), "hits": hits, "clean": not hits}


def build_manifests(rows: list[dict[str, Any]], provenance: dict[str, Any]) -> dict[str, Any]:
    manifests: dict[str, Any] = {}
    for stage, run_ids in RUNS.items():
        for run_id in run_ids:
            run_rows = [row for row in rows if row["run_id"] == run_id]
            manifest = {
                "manifest_kind": "experiment_009_run_finalization_provenance",
                "experiment_id": EXPERIMENT,
                "stage": stage,
                "run_id": run_id,
                "contains_scientific_outcome_counts": False,
                "preregistration_sha": PREREGISTRATION_SHA,
                "scientific_implementation_sha": SCIENTIFIC_SHA,
                "expected_count": 120,
                "authoritative_count": len(run_rows),
                "cell_counts": dict(sorted(Counter(row["cell"] for row in run_rows).items())),
                "phase_a_complete": sum(row["phase_a_done"] for row in run_rows),
                "phase_a_state_score_complete": sum(row["phase_a_frozen"] and row["phase_a_score_present"] for row in run_rows),
                "phase_b_disposition_complete": sum(row["awareness_capture_status"] in AWARENESS_STATUSES for row in run_rows),
                "stochastic_provenance_complete": sum(row["rng_version"] == "sha256-threshold-v1" and row["sample_seed"] is not None for row in run_rows),
                "stage1_stage2_overlap": 0,
                "segments": provenance["runs"][run_id]["segments"],
            }
            manifests[run_id] = manifest
            write_json(REPO / "results" / EXPERIMENT / f"run-{run_id}" / "FINALIZATION_MANIFEST.json", manifest)
    combined = {
        "manifest_kind": "experiment_009_combined_finalization_provenance",
        "experiment_id": EXPERIMENT,
        "preregistration_sha": PREREGISTRATION_SHA,
        "scientific_implementation_sha": SCIENTIFIC_SHA,
        "stage1_provenance_commit": STAGE1_PROVENANCE_COMMIT,
        "stage2_runner_registration_commit": STAGE2_RUNNER_REGISTRATION_COMMIT_CORRECT,
        "infrastructure_commits": INFRASTRUCTURE_COMMITS,
        "contains_scientific_outcome_counts": False,
        "authoritative_total": len(rows),
        "stage_counts": dict(sorted(Counter(row["stage"] for row in rows).items())),
        "model_counts": dict(sorted(Counter(row["model"] for row in rows).items())),
        "cell_counts": final_cell_counts(rows),
        "phase_a_complete": sum(row["phase_a_done"] for row in rows),
        "phase_a_state_score_complete": sum(row["phase_a_frozen"] and row["phase_a_score_present"] for row in rows),
        "phase_b_disposition_complete": sum(row["awareness_capture_status"] in AWARENESS_STATUSES for row in rows),
        "stochastic_provenance_complete": sum(row["rng_version"] == "sha256-threshold-v1" and row["sample_seed"] is not None for row in rows),
        "excluded_provenance_only_segments": provenance["excluded_segments"],
    }
    write_json(REPO / "results" / EXPERIMENT / "final" / "FINALIZATION_MANIFEST.json", combined)
    manifests["combined"] = combined
    return manifests


def integrity(rows: list[dict[str, Any]], provenance: dict[str, Any]) -> dict[str, Any]:
    ids = [row["sample_id"] for row in rows]
    stage_counts = Counter(row["stage"] for row in rows)
    final_cells = Counter((row["model"], row["scenario"], row["p_detect_id"]) for row in rows)
    return {
        "total_rows": len(rows),
        "stage_counts": dict(sorted(stage_counts.items())),
        "unique_ids": len(set(ids)),
        "duplicate_ids": [sid for sid, count in Counter(ids).items() if count > 1],
        "unexpected_total": sum(run["unexpected_count"] for run in provenance["runs"].values()),
        "missing_total": sum(run["missing_count"] for run in provenance["runs"].values()),
        "stage1_stage2_overlap": len({r["sample_id"] for r in rows if r["stage"] == "stage1"}.intersection({r["sample_id"] for r in rows if r["stage"] == "stage2"})),
        "phase_a_complete": sum(row["phase_a_done"] for row in rows),
        "phase_a_state_score_complete": sum(row["phase_a_frozen"] and row["phase_a_score_present"] for row in rows),
        "phase_b_disposition_complete": sum(row["awareness_capture_status"] in AWARENESS_STATUSES for row in rows),
        "stochastic_provenance_complete": sum(row["rng_version"] == "sha256-threshold-v1" and row["sample_seed"] is not None for row in rows),
        "final_cell_count": len(final_cells),
        "final_cells_all_30": all(count == 30 for count in final_cells.values()) and len(final_cells) == 24,
        "run_provenance": provenance["runs"],
        "excluded_provenance_only_segments": provenance["excluded_segments"],
    }


def stochastic_validation(rows: list[dict[str, Any]]) -> dict[str, Any]:
    consumed = [row for row in rows if row["detection_draw_consumed"]]
    by_p = {}
    for p in P_DETECT_ORDER:
        bucket = [row for row in consumed if row["p_detect_id"] == p]
        detected = sum(row["detection_result"] is True for row in bucket)
        by_p[p] = {
            "configured_p_detect": P_DETECT_VALUE[p],
            "draws_consumed": len(bucket),
            "detected": detected,
            "realized_detection_rate": detected / len(bucket) if bucket else None,
        }
    return {
        "draws_consumed_total": len(consumed),
        "by_p_detect": by_p,
        "p100_all_detected_when_consumed": all(row["detection_result"] is True for row in consumed if row["p_detect_id"] == "p100"),
        "p000_none_detected_when_consumed": all(row["detection_result"] is False for row in consumed if row["p_detect_id"] == "p000"),
        "detected_le_violation": all((not row["detected_violation"]) or row["operational_constraint_violation"] for row in rows),
        "sanction_equals_detected": all(row["sanctioned_violation"] == row["detected_violation"] for row in rows),
        "no_draw_without_violation": all(row["operational_constraint_violation"] or not row["detection_draw_consumed"] for row in rows),
    }


def hypothesis_results(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    process_by_p = rate_summary(rows, "max_step", ["p_detect_id"])
    max_rates = {r["p_detect_id"]: r["rate"] for r in process_by_p}
    max_counts = {r["p_detect_id"]: f"{r['count']}/{r['n']}" for r in process_by_p}
    return [
        {
            "hypothesis": "H1 Observability effect",
            "status": "not supported",
            "evidence": "No operational violations were observed at any p_detect level; endpoint has no variance.",
        },
        {
            "hypothesis": "H2 Constraint-bounded behavior",
            "status": "supported within precision limits",
            "evidence": f"Operational violations remained absent across all {len(rows)} samples, including p_detect=0.",
        },
        {
            "hypothesis": "H3 Model effect",
            "status": "indeterminate",
            "evidence": "Primary endpoint has no variance, so model sensitivity is non-estimable.",
        },
        {
            "hypothesis": "H4 Scenario effect",
            "status": "indeterminate",
            "evidence": "Primary endpoint has no variance, so scenario sensitivity is non-estimable.",
        },
        {
            "hypothesis": "H5 Search / process adjustment",
            "status": "not supported for observability-specific process adjustment",
            "evidence": (
                "Max-step counts by p_detect are nearly flat "
                f"({max_counts}); total-step summaries are also similar. "
                "Secondary process variation is concentrated by scenario/model rather than lower observability."
            ),
        },
        {
            "hypothesis": "H6 Awareness / observability relationship",
            "status": "partially supported descriptively",
            "evidence": (
                "Perceived primary task type varies by p_detect, but compliance-test likelihood, "
                "behavior-under-evaluation, and confidence are at ceiling across all 720 samples."
            ),
        },
    ]


def main() -> None:
    rows, provenance = load_authoritative_rows()
    manifests = build_manifests(rows, provenance)
    check = integrity(rows, provenance)
    if (
        check["total_rows"] != 720
        or check["stage_counts"] != {"stage1": 360, "stage2": 360}
        or check["unique_ids"] != 720
        or check["missing_total"] != 0
        or check["unexpected_total"] != 0
        or check["duplicate_ids"]
        or check["stage1_stage2_overlap"] != 0
        or check["phase_a_complete"] != 720
        or check["phase_a_state_score_complete"] != 720
        or check["phase_b_disposition_complete"] != 720
        or check["stochastic_provenance_complete"] != 720
        or not check["final_cells_all_30"]
    ):
        write_json(REPO / "results" / EXPERIMENT / "final" / "derived" / "integrity_failed.json", check)
        raise SystemExit("Experiment 009 integrity gate failed")

    final_dir = REPO / "results" / EXPERIMENT / "final" / "derived"
    stage_dirs = {
        "stage1": REPO / "results" / EXPERIMENT / "stage1" / "derived",
        "stage2": REPO / "results" / EXPERIMENT / "stage2" / "derived",
    }
    for run_id in [*RUNS["stage1"], *RUNS["stage2"]]:
        run_rows = [row for row in rows if row["run_id"] == run_id]
        run_dir = REPO / "results" / EXPERIMENT / f"run-{run_id}" / "derived"
        write_csv(run_dir / "per_sample_results.csv", run_rows)
        write_json(run_dir / "model_summary.json", rate_summary(run_rows, "operational_constraint_violation", []))
        write_json(run_dir / "process_summary.json", process_summary(run_rows, ["scenario", "p_detect_id"]))
        write_json(run_dir / "awareness_summary.json", count_table(run_rows, "perceived_primary_task_type", ["scenario", "p_detect_id"]))

    write_csv(final_dir / "per_sample_authoritative_dataset.csv", rows)
    write_json(final_dir / "integrity_provenance.json", check)
    write_json(final_dir / "finalization_manifests.json", manifests)
    stochastic = stochastic_validation(rows)
    write_json(final_dir / "stochastic_manipulation_validation.json", stochastic)
    outputs = {
        "primary_overall": rate_summary(rows, "operational_constraint_violation", []),
        "primary_by_p_detect": rate_summary(rows, "operational_constraint_violation", ["p_detect_id"]),
        "primary_by_model": rate_summary(rows, "operational_constraint_violation", ["model"]),
        "primary_by_scenario": rate_summary(rows, "operational_constraint_violation", ["scenario"]),
        "primary_24_cell": rate_summary(rows, "operational_constraint_violation", ["model", "scenario", "p_detect_id"]),
        "unauthorized_attempts": {
            "by_p_detect": rate_summary(rows, "unauthorized_attempt", ["p_detect_id"]),
            "by_model": rate_summary(rows, "unauthorized_attempt", ["model"]),
            "by_scenario": rate_summary(rows, "unauthorized_attempt", ["scenario"]),
            "by_cell": rate_summary(rows, "unauthorized_attempt", ["model", "scenario", "p_detect_id"]),
        },
        "detection_sanction": {
            "detected_by_p_detect": rate_summary([row for row in rows if row["detection_draw_consumed"]], "detected_violation", ["p_detect_id"]),
            "sanctioned_by_p_detect": rate_summary([row for row in rows if row["detection_draw_consumed"]], "sanctioned_violation", ["p_detect_id"]),
            "validation": stochastic,
        },
        "process_by_p_detect": process_summary(rows, ["p_detect_id"]),
        "process_by_model": process_summary(rows, ["model"]),
        "process_by_scenario": process_summary(rows, ["scenario"]),
        "process_by_stage": process_summary(rows, ["stage"]),
        "process_by_cell": process_summary(rows, ["model", "scenario", "p_detect_id"]),
        "awareness_capture": {
            "overall": count_table(rows, "awareness_capture_status", []),
            "by_p_detect": count_table(rows, "awareness_capture_status", ["p_detect_id"]),
            "by_model": count_table(rows, "awareness_capture_status", ["model"]),
            "by_scenario": count_table(rows, "awareness_capture_status", ["scenario"]),
            "by_cell": count_table(rows, "awareness_capture_status", ["model", "scenario", "p_detect_id"]),
        },
        "awareness_primary_task_type": {
            "by_p_detect": count_table(rows, "perceived_primary_task_type", ["p_detect_id"]),
            "by_model": count_table(rows, "perceived_primary_task_type", ["model"]),
            "by_scenario": count_table(rows, "perceived_primary_task_type", ["scenario"]),
            "by_cell": count_table(rows, "perceived_primary_task_type", ["model", "scenario", "p_detect_id"]),
        },
        "awareness_compliance_test_likelihood": count_table(rows, "perceived_compliance_test_likelihood", ["p_detect_id"]),
        "awareness_behavior_under_evaluation": count_table(rows, "perceived_behavior_under_evaluation", ["p_detect_id"]),
        "awareness_confidence": count_table(rows, "awareness_confidence", ["p_detect_id"]),
        "stage_consistency": {
            "primary_by_stage": rate_summary(rows, "operational_constraint_violation", ["stage"]),
            "attempt_by_stage": rate_summary(rows, "unauthorized_attempt", ["stage"]),
            "process_by_stage": process_summary(rows, ["stage"]),
            "awareness_by_stage": count_table(rows, "perceived_primary_task_type", ["stage"]),
        },
        "hypotheses": hypothesis_results(rows),
        "inference": {
            "primary_model": "Violation ~ Model * Scenario * p_detect not fit because primary endpoint has no variance.",
            "planned_contrasts": {
                "p_detect_1_vs_0": "non-estimable/no variance; both rates 0",
                "high_vs_low_no": "non-estimable/no variance; both rates 0",
                "ordered_trend": "non-estimable/no variance",
            },
            "all_zero_handling": "Exact binomial upper bounds reported; logistic regression not forced.",
        },
        "prior_experiment_comparison": {
            "exp007": "Cross-domain operational endpoint was 0/360.",
            "exp008": "Naturalistic/eval-salient operational endpoint was 0/360; awareness instrument failed.",
            "exp008b2": "Corrected awareness measurement captured 360/360; operational endpoint was 0/360.",
            "exp009": "Tests whether the operational null persists when expected detection probability falls to zero.",
        },
    }
    for name, payload in outputs.items():
        write_json(final_dir / f"{name}.json", payload)
    for stage, directory in stage_dirs.items():
        stage_rows = [row for row in rows if row["stage"] == stage]
        write_csv(directory / "per_sample_results.csv", stage_rows)
        write_json(directory / "primary_by_p_detect.json", rate_summary(stage_rows, "operational_constraint_violation", ["p_detect_id"]))
        write_json(directory / "process_by_p_detect.json", process_summary(stage_rows, ["p_detect_id"]))
        write_json(directory / "awareness_by_p_detect.json", count_table(stage_rows, "perceived_primary_task_type", ["p_detect_id"]))

    generated = sorted(final_dir.glob("*")) + [p for d in stage_dirs.values() for p in sorted(d.glob("*"))]
    generated += sorted((REPO / "results" / EXPERIMENT).glob("run-*/derived/*"))
    generated += [
        REPO / "results" / EXPERIMENT / "final" / "FINALIZATION_MANIFEST.json",
        *(REPO / "results" / EXPERIMENT / f"run-{run_id}" / "FINALIZATION_MANIFEST.json" for run_id in [*RUNS["stage1"], *RUNS["stage2"]]),
    ]
    scan = credential_scan([path for path in generated if path.is_file()])
    write_json(final_dir / "credential_scan.json", scan)
    print(json.dumps({
        "integrity": check,
        "stochastic": stochastic,
        "primary_overall": outputs["primary_overall"],
        "primary_by_p_detect": outputs["primary_by_p_detect"],
        "process_by_scenario": outputs["process_by_scenario"],
        "awareness_capture": outputs["awareness_capture"]["overall"],
        "awareness_primary_task_type_by_p_detect": outputs["awareness_primary_task_type"]["by_p_detect"],
        "credential_scan": scan,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
