# EvidaraOS Railway backend image.
#
# This keeps the upstream DeerFlow Dockerfile untouched while packaging the
# EvidenceOS skill catalog and explicit deployment config into the gateway
# service image.

ARG UV_IMAGE=ghcr.io/astral-sh/uv:0.7.20
FROM ${UV_IMAGE} AS uv-source

FROM python:3.12-slim-bookworm AS builder

ARG NODE_MAJOR=22
ARG APT_MIRROR
ARG UV_INDEX_URL
ARG UV_EXTRAS

RUN if [ -n "${APT_MIRROR}" ]; then \
      sed -i "s|deb.debian.org|${APT_MIRROR}|g" /etc/apt/sources.list.d/debian.sources 2>/dev/null || true; \
      sed -i "s|deb.debian.org|${APT_MIRROR}|g" /etc/apt/sources.list 2>/dev/null || true; \
    fi

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    gnupg \
    ca-certificates \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" > /etc/apt/sources.list.d/nodesource.list \
    && apt-get update \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

COPY --from=uv-source /uv /uvx /usr/local/bin/

WORKDIR /app

COPY backend ./backend
COPY skills ./skills
COPY deploy/railway/config.yaml ./backend/config.yaml
COPY deploy/railway/extensions_config.json ./backend/extensions_config.json

RUN sh -c "cd backend && UV_INDEX_URL=${UV_INDEX_URL:-https://pypi.org/simple} uv sync ${UV_EXTRAS:+--extra $UV_EXTRAS}"

FROM python:3.12-slim-bookworm

COPY --from=builder /usr/bin/node /usr/bin/node
COPY --from=builder /usr/lib/node_modules /usr/lib/node_modules
RUN ln -s ../lib/node_modules/npm/bin/npm-cli.js /usr/bin/npm \
    && ln -s ../lib/node_modules/npm/bin/npx-cli.js /usr/bin/npx

COPY --from=uv-source /uv /uvx /usr/local/bin/

WORKDIR /app

COPY --from=builder /app/backend ./backend
COPY --from=builder /app/skills ./skills

ENV DEER_FLOW_PROJECT_ROOT=/app
ENV DEER_FLOW_HOME=/app/backend/.deer-flow
ENV DEER_FLOW_CONFIG_PATH=/app/backend/config.yaml
ENV DEER_FLOW_EXTENSIONS_CONFIG_PATH=/app/backend/extensions_config.json
ENV DEER_FLOW_SKILLS_PATH=/app/skills

EXPOSE 8001

CMD ["sh", "-c", "cd /app/backend && PYTHONPATH=. uv run --no-sync uvicorn app.gateway.app:app --host 0.0.0.0 --port ${PORT:-8001}"]
