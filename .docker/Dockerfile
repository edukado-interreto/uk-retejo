# Use an official Python runtime based on Debian 12 "bookworm" as a parent image.
FROM python:3.12-slim-bookworm

# Add user that will be used in the container.
RUN groupadd www-data -g 33
RUN useradd wagtail -u 1029 -g 33  # baptiste:www-data on ikso.net

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# Install the application server.
RUN --mount=type=cache,mode=0777,target=/root/.cache/pip pip install "gunicorn==23.0.0"

# Install the project requirements.
COPY requirements.txt /
RUN --mount=type=cache,mode=0777,target=/root/.cache/pip pip install -r /requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "wagtail" user. This Wagtail project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown wagtail:www-data /app

# Copy the source code of the project into the container.
COPY --chown=wagtail:www-data . .

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

COPY --chmod=755 <<EOT /entrypoint.sh
#!/usr/bin/env bash
set -xe
python manage.py collectstatic --noinput &
python manage.py migrate --noinput &
gunicorn config.wsgi:application
EOT

ENTRYPOINT ["/entrypoint.sh"]
