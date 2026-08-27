from __future__ import annotations

import argparse
import sys

from .config import known_runs
from .supervisor import (
    finalize_run,
    health_report,
    launch_detached,
    preflight_run,
    resume_run,
    status_report,
    stop_run,
    supervise,
)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="python -m artificial_agency.runner")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("start", "resume", "preflight"):
        p = sub.add_parser(name)
        p.add_argument("run_id")
        p.add_argument("--mock", action="store_true")
    for name in ("status", "health", "stop", "finalize"):
        p = sub.add_parser(name)
        p.add_argument("run_id")
    p = sub.add_parser("_supervise")
    p.add_argument("run_id")
    p.add_argument("--mock", action="store_true")
    p.add_argument("--recovery", action="store_true")

    args = parser.parse_args(argv)
    if args.command != "_supervise" and args.run_id not in known_runs():
        raise SystemExit(f"Unknown run: {args.run_id}")

    if args.command == "start":
        result = launch_detached(args.run_id, mock=args.mock)
        if result.get("already_active"):
            print(f"Run {args.run_id} is already active.")
            print(status_report(args.run_id))
        else:
            print(f"Run {args.run_id} supervisor started: PID {result['supervisor_pid']}")
    elif args.command == "status":
        print(status_report(args.run_id))
    elif args.command == "preflight":
        result = preflight_run(args.run_id, mock=args.mock)
        print(f"Run {args.run_id} preflight: {result.get('state', 'UNKNOWN')}")
    elif args.command == "health":
        print(health_report(args.run_id))
    elif args.command == "stop":
        print(stop_run(args.run_id))
    elif args.command == "resume":
        result = resume_run(args.run_id, mock=args.mock)
        if result.get("already_active"):
            print(f"Run {args.run_id} is already active.")
        else:
            print(f"Run {args.run_id} resume supervisor started: PID {result['supervisor_pid']}")
    elif args.command == "finalize":
        result = finalize_run(args.run_id)
        print(f"Run {args.run_id} finalized: {result.get('state', 'UNKNOWN')}")
        if result.get("raw_log_sha256"):
            print(f"Raw log SHA-256: {result['raw_log_sha256']}")
    elif args.command == "_supervise":
        raise SystemExit(supervise(args.run_id, mock=args.mock, recovery=args.recovery))
    else:
        raise SystemExit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
