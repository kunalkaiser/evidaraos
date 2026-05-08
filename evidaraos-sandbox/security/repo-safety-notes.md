# Repo Safety Notes

## Diana Hu File

Found:

`frontend/public/demo/threads/d3e5adaf-084c-4dd5-9d29-94f1d6bccd98/user-data/outputs/diana_hu_research.md`

Assessment:

- Appears to be a checked-in DeerFlow demo artifact.
- Paired with a demo `thread.json`.
- Not a hidden installer.
- Not evidence of background tracking by itself.
- Should be excluded from EvidaraOS production/demo surfaces unless intentionally curated.

## Hidden / Operational Folders

Found:

- `.agent/skills/smoke-test/`
- `backend/.deer-flow/data/deerflow.db`
- `frontend/.vscode/`
- `backend/.vscode/`

Assessment:

- `.agent/skills/smoke-test/` contains deployment/smoke-test automation. It can run install/start/check commands and should not be treated as product code.
- `backend/.deer-flow/data/deerflow.db` is local runtime state.
- `.vscode` folders contain editor settings only.

## Credential / Runtime Notes

Docker compose references host credential directories:

- `~/.claude`
- `~/.codex`
- `~/.kube/config`

This may be intentional for local DeerFlow runtime operation, but EvidaraOS packaging should make credential access explicit and minimal.

## Telemetry / Tracing Notes

The repo documents optional LangSmith/Langfuse tracing. Keep disabled unless explicitly configured by the operator.

## EvidaraOS Safety Rule

No EvidenceOS product build should:

- silently read host credentials
- install global agents or launch services without approval
- write outside the approved workspace
- enable telemetry by default
- publish bundled generic demo outputs as customer-facing proof

