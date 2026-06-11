#!/usr/bin/env bash
set -euo pipefail
cd /home/max/projects/RAG-Implementation/rag-data-indexing-service
LOG="$(dirname "$0")/make_commits.log"
exec >"$LOG" 2>&1

commit_paths() {
  local msg="$1"
  shift
  for p in "$@"; do
    git add -A -- "$p" 2>/dev/null || true
    git add -u -- "$p" 2>/dev/null || true
  done
  if git diff --cached --quiet; then
    echo "SKIP: $msg"
    return 0
  fi
  git commit -m "$msg"
  echo "OK: $msg"
}

echo "=== start ==="
git status --short

commit_paths "chore: update Python dependencies" requirements.txt
commit_paths "feat(docker): update Dockerfile image build" Dockerfile
commit_paths "feat(docker): update Docker Compose services" docker-compose.yml
commit_paths "docs: add config directory README" config/
commit_paths "docs: add docker directory README" docker/
commit_paths "docs: add scripts directory README" scripts/README.md
commit_paths "docs: add docs index README" docs/README.md
commit_paths "docs: add implementation plan" docs/Implementation_Plan.md
commit_paths "docs: update data directory README" data/README.md
commit_paths "docs: add data samples README" data/samples/
commit_paths "feat(core): add configuration and logging" app/core/
commit_paths "feat(pipeline): add document loaders" app/pipeline/loaders/
commit_paths "feat(pipeline): add text chunking" app/pipeline/chunking/
commit_paths "feat(pipeline): add Qdrant indexing" app/pipeline/indexing/
commit_paths "feat(pipeline): add cleaning, embedding, and metadata modules" \
  app/pipeline/README.md app/pipeline/__init__.py \
  app/pipeline/cleaning.py app/pipeline/embedding.py app/pipeline/metadata.py
commit_paths "feat(services): add ingestion service" app/services/
commit_paths "feat(api): add request/response schemas" app/api/schemas/
commit_paths "feat(api): add health, ingest, and collections routes" app/api/routes/
commit_paths "feat(api): add API dependencies and package init" \
  app/api/README.md app/api/__init__.py app/api/deps.py
commit_paths "feat(cli): add Typer CLI for ingest and reset" app/cli/
commit_paths "feat(app): add FastAPI application entry point" \
  app/README.md app/__init__.py app/main.py
commit_paths "docs: update notebooks index README" notebooks/README.md
commit_paths "feat(notebooks): update corpus download notebook" notebooks/01_download_scifact_corpus.ipynb
commit_paths "feat(notebooks): update corpus cleaning notebook" notebooks/02_clean_corpus.ipynb
commit_paths "feat(notebooks): update corpus chunking notebook" notebooks/03_chunk_corpus.ipynb
commit_paths "feat(notebooks): update metadata enrichment notebook" notebooks/04_enrich_metadata.ipynb
commit_paths "feat(notebooks): add embedding generation notebook" notebooks/05_generate_embeddings.ipynb
commit_paths "feat(notebooks): add Qdrant indexing notebook" notebooks/06_index_qdrant.ipynb
commit_paths "feat(notebooks): add index health report notebook" notebooks/07_index_health_report.ipynb
commit_paths "test: add pytest configuration" tests/README.md tests/conftest.py
commit_paths "docs: add test fixtures README" tests/fixtures/
commit_paths "test: add unit tests for pipeline modules" tests/unit/
commit_paths "test: add Qdrant integration smoke test" tests/integration/
commit_paths "docs: update project README with full pipeline guide" README.md
commit_paths "chore(scripts): add per-folder batch commit helper" scripts/make_commits.sh

echo "=== log ==="
git log --oneline -40
echo "=== status ==="
git status -sb
echo "DONE"
