# Use the official Debian-hosted Python image
FROM python:3.10-slim-buster

ENV GOOGLE_APPLICATION_CREDENTIALS="/app/secrets/mega-pipeline.json"

# Ensure we have an up to date baseline, install dependencies 
RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends build-essential git ffmpeg && \
    pip install --no-cache-dir --upgrade pip && \
    pip install pipenv && \
    mkdir -p /app

WORKDIR /app

# Add Pipfile, Pipfile.lock
COPY Pipfile Pipfile.lock /app/

RUN pipenv sync

COPY secrets /app/secrets

# Source code
COPY . /app

# run the entire pipeline non-interactively (the script mega_clip.py will automatically run once the image is run)
CMD ["pipenv", "run", "python", "/app/mega_cli.py"]
