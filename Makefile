.PHONY: build up down logs shell download-data ingest test lint reset-index

# ── Docker ────────────────────────────────────────────────────────────────────

## Build the Docker image (re-runs when requirements.txt changes)
build:
	docker compose build

## Start JupyterLab + Qdrant in the background, then open the browser
up:
	docker compose up --build -d jupyter qdrant
	@echo ""
	@echo "  JupyterLab  →  http://localhost:8888"
	@echo "  Qdrant      →  http://localhost:6333"
	@echo ""
	@echo "  Stop with: make down"

## Stop all running containers
down:
	docker compose down

## Follow logs from all running containers
logs:
	docker compose logs -f

## Open a bash shell inside the running jupyter container
shell:
	docker compose exec jupyter bash

# ── Data ──────────────────────────────────────────────────────────────────────

## Run notebook 01 inside Docker to download and normalize the SciFact corpus
download-data:
	docker compose run --rm jupyter jupyter nbconvert \
		--to notebook --execute --inplace \
		notebooks/01_download_scifact_corpus.ipynb

# ── Pipeline (run these inside the container or after pip install) ─────────────

## Run the ingestion pipeline via CLI
ingest:
	docker compose exec jupyter python -m app.cli ingest \
		--input-dir ./data/raw --collection rag_scifact

## Reset the Qdrant collection
reset-index:
	docker compose exec jupyter python -m app.cli reset \
		--collection rag_scifact

# ── Quality ───────────────────────────────────────────────────────────────────

## Run the test suite inside the jupyter container
test:
	docker compose exec jupyter pytest

## Run the linter inside the jupyter container
lint:
	docker compose exec jupyter ruff check .
	docker compose exec jupyter black --check .
