#!/bin/bash
# Exit immediately if any command exits with a non-zero (failure) status
set -e

echo "🔄 Syncing remote develop branch into local develop branch..."
git switch develop
git pull origin develop
echo "✅ Local develop branch is now up to date!"