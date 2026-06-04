# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SeeMyPills is a full-stack healthcare web application for visually impaired users to photograph prescription labels and receive audio-visual medication dosage information. Monorepo with a feature-based vanilla TypeScript frontend and a vertically-sliced Python FastAPI backend, deployed on AWS with PostgreSQL (AWS RDS).

## Commands

### Frontend (`frontend/`)

```bash
pnpm dev          # start Vite dev server at http://localhost:5173
pnpm build        # type-check then bundle for production (tsc && vite build)
pnpm preview      # preview the production build locally
```

### Backend (`backend-python/`)

```bash
uv run uvicorn app.main:app --reload    # start FastAPI dev server
uv run pytest                           # run all tests
uv run pytest tests/db/                 # run a specific test folder
uv add <package>                        # add a dependency
```

Environment is selected via the `ENV` variable (defaults to `development`), which loads `.env.development` or `.env.production` via pydantic-settings.

## Architecture

### Frontend

Entry point: `index.html` → `src/app.ts`

**Asset locations:**
- `public/` — static assets served at runtime with stable URLs; used by dynamically injected HTML not processed by Vite
- `src/assets/` — static assets processed by Vite at build time; only for files referenced in `index.html` or imported directly in TypeScript

**Structure:**
- `src/core/` — app infrastructure: API client, router, global lib/store
- `src/features/` — domain pages/modules (vertical slices)
- `src/pages/` — standalone HTML pages (e.g. 404)
- `src/shared/` — reusable components, scripts, styles, types, utils

### Backend

Entry point: `backend-python/main.py` → `app/main.py` (FastAPI app)

**Database initialization:** `setup_database()` in `app/db/database.py` must be called once at startup before any `get_db()` call. `get_db()` is a FastAPI dependency injected per request that yields a SQLAlchemy session and closes it after the request.

**Settings:** `app/core/config.py` uses pydantic-settings with nested delimiter `__` to map env vars into `AppSettings`, `DatabaseSettings`, and `AWSSettings` model groups. Loaded from `.env.development` or `.env.production` based on the `ENV` env var.

**Structure:**
- `app/core/` — global config, logging, security
- `app/db/` — SQLAlchemy engine, session factory, base model, mixins
- `app/features/` — vertical slices, each containing models, schemas, services, router
- `app/utils/` — shared utilities
