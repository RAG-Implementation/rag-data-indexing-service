#!/usr/bin/env bash
# One commit per folder/file. Run from repo root: bash scripts/run_per_folder_commits.sh
set -euo pipefail
cd "$(dirname "$0")/.."
LOG="scripts/commit_run.log"
exec > >(tee -a "$LOG") 2>&1

commit_paths() {
  local msg="$1"
  shift
  echo ""
  echo ">>> $msg"
  git add -A -- "$@"
  if git diff --cached --quiet; then
    echo "SKIP (no staged changes)"
    return 0
  fi
  git commit -m "$msg"
}

commit_paths "build(docker): update Dockerfile for service dependencies" Dockerfile

commit_paths "build(docker): update Docker Compose services and profiles" docker-compose.yml

commit_paths "build: update Python dependencies" requirements.txt

commit_paths "docs: update root README with pipeline and usage guide" README.md

commit_paths "feat(app): add FastAPI application entry point" \
  app/__init__.py app/main.py app/README.md

commit_paths "feat(core): add configuration and structured logging" app/core/

commit_paths "feat(cli): add Typer CLI for ingest, status, and reset" app/cli/

commit_paths "feat(api): add API package and shared dependencies" \
  app/api/__init__.py app/api/deps.py app/api/README.md

commit_paths "feat(api): add health, ingest, and collections routes" app/api/routes/

commit_paths "feat(api): add ingest request and response schemas" app/api/schemas/

commit_paths "feat(pipeline): add pipeline package root" \
  app/pipeline/__init__.py app/pipeline/README.md \
  app/pipeline/cleaning.py app/pipeline/embedding.py app/pipeline/metadata.py

commit_paths "feat(pipeline): add document loaders for JSONL and text files" app/pipeline/loaders/

commit_paths "feat(pipeline): add recursive character chunking" app/pipeline/chunking/

commit_paths "feat(pipeline): add Qdrant vector indexer" app/pipeline/indexing/

commit_paths "feat(services): add ingestion orchestration service" app/services/

commit_paths "docs: add config directory README" config/

commit_paths "docs: update data directory README and samples guide" data/

commit_paths "docs: add docker directory README" docker/

commit_paths "docs: add implementation plan and docs index" docs/

commit_paths "feat(notebooks): update corpus download notebook" notebooks/01_download_scifact_corpus.ipynb

commit_paths "feat(notebooks): update corpus cleaning notebook" notebooks/02_clean_corpus.ipynb

commit_paths "feat(notebooks): add corpus chunking notebook" notebooks/03_chunk_corpus.ipynb

commit_paths "feat(notebooks): add metadata enrichment notebook" notebooks/04_enrich_metadata.ipynb

commit_paths "feat(notebooks): add embedding generation notebook" notebooks/05_generate_embeddings.ipynb

commit_paths "feat(notebooks): add Qdrant indexing notebook" notebooks/06_index_qdrant.ipynb

commit_paths "feat(notebooks): add index health report notebook" notebooks/07_index_health_report.ipynb

commit_paths "docs: update notebooks README" notebooks/README.md

commit_paths "docs: add scripts directory README" scripts/

commit_paths "test: add pytest configuration and tests README" tests/README.md tests/conftest.py

commit_paths "test(unit): add unit tests for pipeline modules" tests/unit/

commit_paths "test(integration): add Qdrant indexing smoke test" tests/integration/

commit_paths "docs: add test fixtures README" tests/fixtures/

echo ""
echo "=== git log ==="
git log --oneline -30

echo ""
echo "=== git push ==="
git push

echo ""
echo "=== final status ==="
git status -sb

echo "DONE"
