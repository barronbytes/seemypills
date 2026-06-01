# SeeMyPills

SeeMyPills is an accessible, full-stack healthcare web application designed to help visually impaired individuals medicate with confidence. Patients photograph or upload prescription labels to receive audio-visual dosage information.

## Tech Stack

**Frontend:** Vanilla TypeScript (HTML/CSS/TS)
**Backend:** FastAPI (Python)
**Infrastructure:** AWS

## Project Structure

Monorepo combining a feature-based frontend and a vertically-sliced backend:

```bash
seemypills/
├── .github/            # CI/CD workflows and GitHub Actions
├── frontend/           # Vanilla TypeScript client (feature-based)
├── backend-python/     # Python FastAPI service (vertical slices)
├── scripts/            # Shared automation scripts
└── README.md
```

Further sub-project descriptions:

- [Frontend README](./frontend/README.md)
- [Backend README](./backend-python/README.md)

## Quick Start

## Usage

### 🚀 Production Release Workflow & Scripts

To protect the production codebase on `main` branch, all features are developed on isolated branches and merged into `develop` branch first. GitHub branch protection rules, standard workflows, and fallbacks have been thought of to safely align feature branch changes into production.

#### 🔒 Branch Protection Rules

Select the following GitHub protection rules for the `main` and `develop` branches:

[x] Require a pull request before merging
[x] Dismiss stale pull request approvals when new commits are pushed
[x] Require a linear history
[x] Do not allow bypassing the above settings
[x] Allow force pushes (everyone)

#### 🔄 Standard Release Workflow

When branch protections are active, follow these steps to move a feature to production:

1. **GitHub UI:** Open PR from `feature` to `develop` branch; select **squash and merge**
2. **Local Terminal:** Manually run: `./scripts/git-pr-synced-pull.sh`
3. **GitHub UI:** Open PR from `develop` to `main` branch; select **rebase and merge**
4. **GitHub Action:** Automated run: `./.github/workflows/git-pr-sync.yml`
5. **Local Terminal:** Upate local branches: `./scripts/git-pr-synced-pull.sh`

#### 🛠️ Emergency & Manual Fallback Scripts

If the `main` branch ever says it is both "ahead and behind" of the `develop` branch, then do either of these:

1. **Option A:** Keep `develop` branch intact. Temporarily turn off protection rules for `main` and use the `./scripts/git-unprotected-force-align-main.sh` file to fast-forward sync `main` branch directly.
2. **Option B:** Keep `main` branch intact. Use the `./scripts/git-diverged-force-align-develop.sh` file to hard-reset and force-push the `develop` branch back into perfect alignment with `main`.

## System Design