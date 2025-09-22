# --- BASE STAGE ---
FROM python:3.12-slim-bookworm AS base

# Port used by this container to serve HTTP.
EXPOSE $PORT

ENV PYTHONUNBUFFERED=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VIRTUAL_ENV="/opt/pysetup/.venv" \
    PORT=$PORT

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# Install the project requirements.
WORKDIR $PYSETUP_PATH
COPY ./requirements.txt ./
RUN --mount=type=cache,mode=0777,target=/root/.cache/pip pip install -r ./requirements.txt


# --- DEVELOPMENT STAGE ---
FROM base AS development

COPY --from=base $PYSETUP_PATH $PYSETUP_PATH

WORKDIR $PYSETUP_PATH
RUN --mount=type=cache,mode=0777,target=/root/.cache/pip pip install -r ./requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /app


# --- PRODUCTION STAGE ---
FROM base AS production

ARG GIT_COMMIT=none
ARG GIT_BRANCH=none
ENV GIT_COMMIT=$GIT_COMMIT GIT_BRANCH=$GIT_BRANCH

# Add user that will be used in the container.
ARG USER_ID=1030  # On ikso.net: compose
ARG GROUP_ID=33  # On ikso.net: www-data
RUN grep :$GROUP_ID: /etc/group || groupadd $GROUP_ID -g $GROUP_ID
RUN useradd appuser -u $USER_ID -g $GROUP_ID

WORKDIR $PYSETUP_PATH
RUN --mount=type=cache,mode=0777,target=/root/.cache/pip pip install "gunicorn==23.0.0"

WORKDIR /app

COPY --chmod=755 <<EOT /entrypoint.sh
#!/usr/bin/env bash
set -xe
python manage.py migrate --noinput &
gunicorn config.wsgi:application
EOT

ENTRYPOINT ["/entrypoint.sh"]

