#!/bin/bash
# Exit immediately if any command exits with a non-zero (failure) status
set -e

echo "🛑 WARNING: This script manually fast-forwards 'main' to match 'develop' and pushes directly to GitHub."
echo "⚠️  Ensure you have temporarily disabled GitHub branch protection rules for 'main' before continuing!"
echo "--------------------------------------------------------"

# 1. Switch over to main branch
echo "🔄 Step 1: Switching to main branch..."
git switch main

# 2. Fast-forward main to match develop exactly
echo "⚡ Step 2: Fast-forwarding main to match develop..."
git merge develop --ff-only

# 3. Push the updates directly to remote main
echo "📤 Step 3: Pushing updates directly to remote main..."
git push origin main

echo "--------------------------------------------------------"
echo "✅ Success! Remote and local main branches are now perfectly aligned with develop."
echo "🔒 Remember to turn your GitHub branch protection rules back ON!"