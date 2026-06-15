#!/bin/bash
set -e

echo "🚀 Starting automated deployment for SeeMyPills..."

# ========================================
# 1. Deploy frontend
# ========================================
echo "📦 Processing frontend deployment..."
cd ~/seemypills/frontend
pnpm install
pnpm build
aws s3 sync dist/ s3://seemypills-frontend --delete

echo "🌐 Invalidating CloudFront cache..."
aws cloudfront create-invalidation --distribution-id E21GVE2MB4NAJK --paths "/*" > /dev/null

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