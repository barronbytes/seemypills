#!/bin/bash
# Exit immediately if any command exits with a non-zero (failure) status
set -e

echo "⚡ Fast-forwarding local develop branch to match local main branch..."
git switch develop
git merge main --ff-only

echo "📤 Pushing clean linear history from local develop branch back to remote develop branch..."
git push origin develop
echo "✅ Remote & local develop branches now align with production branches!"