#!/bin/bash
# Exit immediately if any command exits with a non-zero (failure) status
set -e

echo "🛑 WARNING: This script forcefully aligns local and remote 'develop' to match 'main'."
echo "⚠️ Ensure you have temporarily disabled GitHub branch protection rules for 'develop' before continuing!"
echo "--------------------------------------------------------"

# 1. Sync local branches to pull the latest remote history
echo "📥 Step 1: Running remote to local sync pull..."
./scripts/git-pr-synced-pull.sh

# 2. Move to local develop branch
echo "🔄 Step 2: Switching to develop branch..."
git switch develop

# 3. Hard reset local develop to mirror local main exactly
echo "⚡ Step 3: Hard resetting local develop to mirror main..."
git reset --hard main

# 4. Force push the clean alignment back to GitHub
echo "📤 Step 4: Force-pushing aligned history to remote develop..."
git push origin develop --force

echo "--------------------------------------------------------"
echo "✅ Success! Remote and local develop branches are now perfectly aligned with local & remote main branches."
echo "🔒 Remember to turn your GitHub branch protection rules back ON!"