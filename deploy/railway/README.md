# EvidaraOS Railway Deployment

This is the recommended MVP deployment path for EvidaraOS when using the existing Dockerfiles and keeping the public product site separate from the backend gateway.

Railway does not run `docker-compose.yml` directly. Create separate Railway services from the same GitHub repo:

1. `evidaraos-frontend`
2. `evidaraos-gateway`
3. Optional managed Postgres later, when persistence is moved from local SQLite/files to Postgres.

## Current Architecture

```text
Browser
  -> evidaraos-frontend
      -> NEXT_PUBLIC_BACKEND_BASE_URL
      -> NEXT_PUBLIC_LANGGRAPH_BASE_URL
  -> evidaraos-gateway
      -> /api/models
      -> /api/skills
      -> /api/threads/*
      -> /api/langgraph-equivalent paths through gateway /api/*
```

For production, prefer same-domain reverse proxy later. For MVP, separate frontend and gateway domains are acceptable if CORS, trusted origins, and cookies are configured carefully.

## Service 1: Frontend

Create a Railway service from the repo.

Settings:

- Builder: Dockerfile
- Dockerfile path: `frontend/Dockerfile`
- Docker target: `prod`
- Public domain: enabled
- Port: Railway should detect `3000`

Variables:

Use `frontend.env.example` as the starting point.

Important:

- `NEXT_PUBLIC_BACKEND_BASE_URL` should point to the public gateway URL.
- `NEXT_PUBLIC_LANGGRAPH_BASE_URL` should point to the gateway LangGraph-compatible API base. With this gateway, use `<gateway-url>/api`.
- `DEER_FLOW_INTERNAL_GATEWAY_BASE_URL` should point to the private Railway gateway URL if using Railway private networking, otherwise the public gateway URL.

## Service 2: Gateway

Create a second Railway service from the same repo.

Settings:

- Builder: Dockerfile
- Dockerfile path: `deploy/railway/backend.Dockerfile`
- Docker target: runtime/default
- Public domain: enabled
- Port: Railway should inject `$PORT`; the image defaults to `8001` locally
- Volume: mount at `/app/backend/.deer-flow`

Variables:

Use `gateway.env.example` as the starting point.

Important:

- `ANTHROPIC_API_KEY` or another configured model key is required for real agent runs.
- `BETTER_AUTH_SECRET` must be a long random secret.
- `DEER_FLOW_HOME` should be `/app/backend/.deer-flow`.
- `DEER_FLOW_PROJECT_ROOT` should be `/app`.
- `DEER_FLOW_CONFIG_PATH` should be `/app/backend/config.yaml`.
- `DEER_FLOW_EXTENSIONS_CONFIG_PATH` should be `/app/backend/extensions_config.json`.
- `DEER_FLOW_SKILLS_PATH` should be `/app/skills`.
- `GATEWAY_CORS_ORIGINS` and `DEER_FLOW_TRUSTED_ORIGINS` should include the frontend public URL.

## Sandbox Note

The current `config.yaml` uses `LocalSandboxProvider`, which is simpler for MVP deployment but is not the preferred isolation model for untrusted production workloads.

For a serious multi-user production launch, use a VM/Kubernetes deployment with isolated sandbox execution rather than a generic PaaS container without Docker socket access.

## Verification

After deployment:

```bash
curl -I https://<frontend-domain>/
curl -I https://<gateway-domain>/health
curl -I https://<gateway-domain>/api/models
```

Then open:

```text
https://<frontend-domain>/workspace/modules
```

The product pages can render without backend. Real chat/workspace execution requires the gateway to be healthy and model credentials to be valid.

## Known Constraints

- Fixture demo cards are not live execution.
- Local macOS backend startup can fail on `onnxruntime` wheel resolution; Linux Docker deployment avoids that platform issue.
- Railway services should be configured separately; do not upload the compose file expecting Railway to run it directly.
- Full production sandbox isolation may require Fly.io, a VPS, or Kubernetes.
