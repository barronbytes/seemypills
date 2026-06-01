#!/bin/bash
# Exit immediately if any command exits with a non-zero (failure) status
set -e

echo "🔄 Syncing remote main branch into local main branch..."
git switch main
git pull origin main
echo "✅ Local main branch is perfectly up to date!"