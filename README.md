# See My Pills: Medicate Safely

SeeMyPills is an accessible, full-stack healthcare web application designed to help visually impaired individuals medicate with confidence. Patients photograph or upload prescription labels to receive audio-visual dosage information.

## Tech Stack

- **Frontend:** Vanilla TypeScript (HTML/CSS/TS)
- **Backend:** FastAPI (Python)
- **Infrastructure:** AWS

## Project Structure

Monorepo combining a feature-based frontend and a vertically-sliced backend:

```bash
seemypills/
├── .claude/            # Claude Code configurations and workflows
├── .github/            # CI/CD workflows and GitHub Actions
├── .vscode/            # Project level editor settings
├── frontend/           # Vanilla TypeScript client (feature-based)
├── backend-python/     # Python FastAPI service (vertical slices)
├── scripts/            # Shared automation scripts
├── CLAUDE.md
└── README.md
```

Further sub-project descriptions:

- [Frontend README](./frontend/README.md)
- [Backend README](./backend-python/README.md)

## Quick Start

## Usage

### 🧪 Testing

Run the following commands from their respective subdirectory (`frontend/` or `backend-python/`):

- Frontend Checks
  - Type Checking: `pnpm typecheck`
  - Linting: `pnpm lint`
  - Tests (frontend): `pnpm test`
  - Build: `pnpm build`
- Backend Checks
  - Pytests (backend): `uv run pytest tests/folder/ -m "not integration"`
  - Pytests (backend): `uv run pytest tests/<filepath>.py -m "not integration"`
  - Pytests (backend): `uv run pytest tests/<filepath>.py -m integration`

### 🚀 Production Release Workflow & Scripts

To protect the production codebase on `main` branch, all features are developed on isolated branches and merged into `develop` branch first. GitHub branch protection rules, standard workflows, and fallbacks have been thought of to safely align feature branch changes into production.

#### 🔒 Branch Protection Rules

Select the following GitHub protection rules for the `main` branch:

- Require a pull request before merging
- Dismiss stale pull request approvals when new commits are pushed
- Require a linear history
- Do not allow bypassing the above settings
- Allow force pushes (everyone)

Select the following GitHub protection rules for the `develop` branch:

- Require a pull request before merging
- Dismiss stale pull request approvals when new commits are pushed
- Require a linear history
- Allow force pushes (everyone)

#### 🔄 Standard Release Workflow

When branch protections are active, follow these steps to move a feature to production:

1. **GitHub UI:** Open PR from `feature` to `develop` branch; select **squash and merge**
2. **Local Terminal:** Manually run: `./scripts/git-pr-sync-develop.sh`
3. **GitHub UI:** Open PR from `develop` to `main` branch; select **rebase and merge**
4. **GitHub Action:** Automated run: `./.github/workflows/git-pr-develop-to-main-sync-branches.yml`
5. **Local Terminal:** Upate local branches: `./scripts/git-action-sync-local.sh`

#### 🛠️ Emergency & Manual Fallback Scripts

If the `main` branch ever says it is both "ahead and behind" of the `develop` branch, then do either of these:

1. **Option A:** Keep `develop` branch intact. Temporarily turn off protection rules for `main` and use the `./scripts/git-unprotected-force-align-main.sh` file to fast-forward sync `main` branch directly.
2. **Option B:** Keep `main` branch intact. Temporarily turn off protection rules for `develop` and use the `./scripts/git-unprotected-force-align-develop.sh` file to hard-reset and force-push the `develop` branch.

## System Design