#!/bin/bash
set -e

# 1. Sync local main branch
git switch main
git pull origin main

# 2. Sync local develop branch
git switch develop
git fetch origin
git reset --hard origin/develop
