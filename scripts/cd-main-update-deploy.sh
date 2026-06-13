#!/bin/bash
set -e

# 1. Sync repository with latest main
BEFORE_SHA=$(git rev-parse HEAD)
git stash
git pull origin main
AFTER_SHA=$(git rev-parse HEAD)

# Skip deploy if main has no new commits
if [ "$BEFORE_SHA" = "$AFTER_SHA" ]; then
  echo "No new changes on main. Skipping deploy."
  exit 0
fi

# 2. Deploy frontend
cd frontend
pnpm install
pnpm build
aws s3 sync dist/ s3://seemypills-frontend --delete
cd ..

# 3. Deploy backend
cd backend-python
uv sync
ENV=production uv run alembic upgrade head
sudo pkill -f uvicorn || true
ENV=production nohup uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 > ~/uvicorn.log 2>&1 &
cd ..
