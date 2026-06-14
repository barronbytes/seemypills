#!/bin/bash
set -e

echo "🚀 Starting automated deployment for SeeMyPills..."

# Ensure in root repository directory
cd ~/seemypills

# ========================================
# 1. Deploy frontend
# ========================================
echo "📦 Processing frontend deployment..."
cd ~/seemypills/frontend
pnpm install
pnpm build
aws s3 sync dist/ s3://seemypills-frontend --delete

# ========================================
# 2. Deploy backend
# ========================================
echo "📦 Processing backend deployment..."
cd ~/seemypills/backend-python
uv sync

echo "🗄️ Running database migrations via Alembic..."
ENV=production uv run alembic upgrade head

echo "🔄 Cycling application services via Systemd..."
# Let systemd cleanly restart the designated server daemon with the fresh code
sudo systemctl restart seemypills

echo "✅ Continuous deployment pipeline completed successfully!"