#!/bin/bash
set -e

# 1. Sync local main branch to rebase merge updates
git switch main
git pull origin main

# 2. Sync local develop branch to fast-forward updates
git switch develop
git pull origin develop