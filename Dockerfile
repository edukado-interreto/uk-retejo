# --- BASE STAGE ---
FROM python:3.12-slim-bookworm AS base

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH" \
    UV_PROJECT_ENVIRONMENT=$VIRTUAL_ENV



# --- BUILDER STAGE ---
FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim AS builder

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Use a different virtual environment from /app/.venv
ENV UV_PROJECT_ENVIRONMENT=/opt/venv

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=.docker/pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev



# --- DEVELOPMENT STAGE ---
FROM base AS development


COPY --from=builder --chown=appuser:appuser $VIRTUAL_ENV $VIRTUAL_ENV
 
RUN \
--mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
--mount=type=cache,target=/root/.cache/uv \
--mount=type=bind,source=uv.lock,target=uv.lock \
--mount=type=bind,source=pyproject.toml,target=pyproject.toml \
UV_SYSTEM_PYTHON=1 uv sync --frozen

RUN chmod +x $VIRTUAL_ENV/bin/activate; $VIRTUAL_ENV/bin/activate
RUN type python

# Use /app folder as a directory where the source code is stored.
WORKDIR /app



# --- PRODUCTION STAGE ---
FROM base AS production

ARG USER_ID=1030  # On ikso.net: compose
ARG GROUP_ID=33  # On ikso.net: www-data
ARG GIT_COMMIT=none
ARG GIT_BRANCH=none

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    USER=appuser \
    USER_ID=$USER_ID \
    GROUP_ID=$GROUP_ID \
    GIT_COMMIT=$GIT_COMMIT \
    GIT_BRANCH=$GIT_BRANCH \
    UV_CACHE_DIR=/root/.cache/uv \
    PORT=8000 

EXPOSE $PORT

# Add user that will be used in the container.
RUN grep :$GROUP_ID: /etc/group || groupadd $GROUP_ID -g $GROUP_ID && \
    useradd $USER -u $USER_ID -g $GROUP_ID

COPY --from=builder --chown=$USER_ID:$GROUP_ID $VIRTUAL_ENV $VIRTUAL_ENV

# Add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD --chown=$USER:$GROUP_ID . /app
WORKDIR /app

RUN \
--mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
--mount=type=cache,target=$UV_CACHE_DIR \
    uv sync --frozen --no-dev --group production

USER $USER

COPY --chmod=755 <<EOT /entrypoint.sh
#!/usr/bin/env bash
set -xe

export GRANIAN_INTERFACE=wsgi
export GRANIAN_HOST=0.0.0.0
export GRANIAN_PORT=$PORT
export GRANIAN_BLOCKING_THREADS=3

python manage.py migrate --noinput &
granian config.wsgi:application
EOT

ENTRYPOINT ["/entrypoint.sh"]

