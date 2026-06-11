# docker

Reserved directory for additional Docker-related configuration files. The main Docker setup lives at the project root (`Dockerfile`, `docker-compose.yml`). This directory is the intended home for supplementary files such as custom Nginx configurations, init scripts, or multi-stage build helpers if the Docker setup grows more complex.

## Table of Contents

- [1. Current State](#1-current-state)
- [2. Main Docker Files](#2-main-docker-files)
- [3. Planned Use](#3-planned-use)

## 1. Current State

This directory is empty. The `.gitkeep` file preserves it in git. All Docker configuration currently lives at the project root.

## 2. Main Docker Files

The active Docker configuration is at the project root:

| File | Purpose |
|---|---|
| `Dockerfile` | Multi-stage image definition. Installs Python dependencies and copies the `app/` package. |
| `docker-compose.yml` | Defines the `jupyter`, `qdrant`, and `api` services. The `jupyter` service runs JupyterLab and is used for notebooks and `make test`. The `api` service starts with `--profile api`. |

## 3. Planned Use

Files that may be placed here in the future:

| File | Purpose |
|---|---|
| `nginx.conf` | Reverse proxy configuration if the API is placed behind Nginx |
| `qdrant_config.yaml` | Custom Qdrant server configuration (log level, collection defaults, GRPC settings) |
| `entrypoint.sh` | Custom container entrypoint script for initialization tasks |
