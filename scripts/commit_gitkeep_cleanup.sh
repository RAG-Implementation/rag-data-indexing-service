#!/usr/bin/env bash
set -euo pipefail
cd /home/max/projects/RAG-Implementation/rag-data-indexing-service
LOG="$(dirname "$0")/git_cleanup.log"
exec >"$LOG" 2>&1

commit_deleted() {
  local msg="$1"
  local path="$2"
  if ! git ls-files --error-unmatch "$path" >/dev/null 2>&1; then
    echo "SKIP (not tracked): $path"
    return 0
  fi
  if [ -e "$path" ]; then
    echo "SKIP (still exists): $path"
    return 0
  fi
  git add -u -- "$path"
  if git diff --cached --quiet; then
    echo "SKIP (nothing staged): $msg"
    return 0
  fi
  git commit -m "$msg"
  echo "OK: $msg"
}

echo "=== before ==="
git status --short

commit_deleted "chore: remove app root placeholder after package scaffolding" app/.gitkeep
commit_deleted "chore: remove app/api placeholder after API module added" app/api/.gitkeep
commit_deleted "chore: remove app/pipeline placeholder after pipeline modules added" app/pipeline/.gitkeep
commit_deleted "chore: remove data root placeholder after README added" data/.gitkeep
commit_deleted "chore: remove docs placeholder after documentation added" docs/.gitkeep
commit_deleted "chore: remove scripts placeholder after README added" scripts/.gitkeep
commit_deleted "chore: remove temporary per-folder commit helper script" scripts/run_per_folder_commits.sh
commit_deleted "chore: remove tests placeholder after test suite added" tests/.gitkeep

echo "=== push ==="
git push

echo "=== after ==="
git status -sb
git log --oneline -10
echo "DONE"
