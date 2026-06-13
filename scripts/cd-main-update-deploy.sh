#!/bin/bash
set -e

echo "🚀 Starting automated deployment for SeeMyPills..."

# Ensure in root repository directory
cd ~/seemypills

# ==========================================
# 1. Sync repository with latest main
# ==========================================
BEFORE_SHA=$(git rev-parse HEAD)

echo "📥 Stashing local markers and pulling remote main..."
git stash
git pull origin main

AFTER_SHA=$(git rev-parse HEAD)

# Skip deploy if main has no new commits
if [ "$BEFORE_SHA" = "$AFTER_SHA" ]; then
  echo "No new changes on main. Skipping deployment pipeline."
  exit 0
fi

# ==========================================
# 2. Deploy frontend
# ==========================================
echo "📦 Processing frontend deployment..."
cd ~/seemypills/frontend
pnpm install
pnpm build
aws s3 sync dist/ s3://seemypills-frontend --delete
cd ..

# ==========================================
# 3. Deploy backend
# ==========================================
echo "📦 Processing backend deployment..."
cd ~/seemypills/backend-python
uv sync

echo "🗄️ Running database migrations via Alembic..."
ENV=production uv run alembic upgrade head

echo "🔄 Cycling application services via Systemd..."

# Let systemd cleanly restart the designated server daemon with the fresh code
sudo systemctl restart seemypills

echo "✅ Continuous deployment pipeline completed successfully!"