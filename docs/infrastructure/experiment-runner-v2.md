# Experiment Runner v2

Experiment Runner v2 is a lightweight remote-first supervisor around Inspect. Inspect remains the scientific execution engine; the runner handles lifecycle, preflight, operational status, durable logging, interruption, recovery, and finalization.

## Architecture
Remote Codex or GitHub Actions acts as the control plane:

`iPad / ChatGPT -> Remote Codex / GitHub -> self-hosted macOS runner -> Experiment Runner -> Inspect`

The runner writes per-run operational files under `results/<experiment>/<run>/`:

- `RUN_STATUS.json`
- `operational.log`
- `RUN_LOCK.json`
- `RUNNER.pid`
- raw Inspect logs under ignored `inspect/`
- canary Inspect logs under ignored `canary/`

Runtime-only Inspect state is written under ignored `results/.runner-runtime/`.

## Commands
```bash
python -m artificial_agency.runner start 002A
python -m artificial_agency.runner status 002A
python -m artificial_agency.runner health 002A
python -m artificial_agency.runner stop 002A
python -m artificial_agency.runner resume 002A
python -m artificial_agency.runner finalize 002A
```

`start` launches a detached supervisor process using `subprocess.Popen(..., start_new_session=True)`. The run does not depend on the initiating Codex session remaining alive.

## GitHub Actions Remote Dispatch
Production runs can be dispatched through `.github/workflows/experiment-runner.yml`.

The workflow is manual-only (`workflow_dispatch`) and accepts:

- `run_id`: currently `002A`
- `action`: `start`, `status`, `health`, `stop`, `resume`, or `finalize`

The job requires a self-hosted macOS runner with all labels:

- `self-hosted`
- `macOS`
- `artificial-agency`

There is no GitHub-hosted fallback. The workflow checks out the repository, creates `.venv`, installs the package editable with dev dependencies, verifies `OPENAI_API_KEY` is present without printing it, and dispatches the corresponding runner command.

The workflow is a command dispatcher. Runner v2 remains responsible for scientific integrity, preflight, canary, process locking, detached execution, status, and finalization.

### iPad-First Operation
From an iPad, open the GitHub Actions tab, select **Experiment Runner**, choose **Run workflow**, then select:

- `run_id=002A`
- one of `start`, `status`, `health`, `stop`, `resume`, or `finalize`

Remote Codex or GitHub API tooling can trigger the same `workflow_dispatch` inputs later.

### One-Time Mac Setup
Configure a repository-scoped self-hosted GitHub Actions runner on the Mac and assign the `artificial-agency` label. Use a private/trusted repository and trusted workflow sources only. Prefer running the self-hosted runner under a dedicated non-admin user or otherwise limiting host permissions.

Configure `OPENAI_API_KEY` either as a repository secret named `OPENAI_API_KEY` or through a secure host-level environment available to the self-hosted runner. The workflow never echoes the key.

### Persistence Caveat
Runner v2 starts its supervisor with `start_new_session=True`. This is intended to survive the workflow step. This must be verified on the actual self-hosted runner without production model execution before first production use. If GitHub Actions job cleanup terminates detached descendants on that host, use a persistent host service handoff such as a macOS `launchd` agent and keep the GitHub workflow as a command dispatcher.

## State Model
Typical states:

- `STARTING`
- `PREFLIGHT`
- `RUNNING`
- `STOPPING`
- `STOPPED`
- `FAILED`
- `COMPLETED`

Duplicate starts are blocked by `RUN_LOCK.json` and process liveness checks. Stale locks are detected when the recorded supervisor PID no longer exists.

## Preflight
Before production samples, the runner checks:

- frozen scientific commit
- clean worktree
- expected sample counts
- package import and writable paths
- Inspect dry-load with `limit=0`
- DNS resolution for `api.openai.com`
- outbound HTTPS reachability
- authenticated OpenAI request
- nonexperimental Inspect canary

The canary is operational only, uses `artificial_agency/runner/canary.py@operational_canary`, and is not part of Experiment 002 analysis.

## Fail-Fast Defaults
Production Inspect runs add operational reliability flags:

- `--max-retries 3`
- `--timeout 60`
- `--attempt-timeout 45`
- `--log-buffer 1`
- `--checkpoint turn:1`

The previous default Inspect behavior retried connectivity failures indefinitely. Runner v2 bounds retries and checks DNS/API health before production execution.

## Incremental Flushing
`--log-buffer 1` asks Inspect to flush completed samples sample-by-sample. This favors recoverability over marginal throughput.

## Blinding Policy
During execution, runner status and health expose only operational metadata:

- process state
- completed sample count
- raw log size
- token usage when available
- API health
- elapsed time

They must not expose trajectories, model decisions, tool calls, scores, policy violations, condition outcomes, or qualitative behavior.

## Stop and Resume
`stop` sends `SIGTERM` to the supervisor process group and preserves raw logs/status. Forceful termination is not the default.

`resume` records recovery provenance and starts a new detached supervisor. The selected Inspect recovery mechanism is checkpoint-aware `inspect eval`/`eval retry`; completed sample reuse depends on Inspect's supported retry semantics for the raw log/checkpoint state. The runner records completed counts before resume and does not silently inspect outcomes.

## Raw-Log Security
Raw Inspect logs remain outside Git. They are ignored by `.gitignore` and treated as sensitive because provider/runtime logs may contain credential-bearing metadata. Finalization computes SHA-256 and byte size without committing raw logs.

## Registering Future Runs
Add a `RunSpec` entry in `artificial_agency/runner/config.py` with:

- run ID
- experiment ID
- frozen commit
- Inspect task
- model and generation settings
- expected sample counts
- results paths
- prior technical attempts, if any

Do not encode scientific condition changes in runner infrastructure.
