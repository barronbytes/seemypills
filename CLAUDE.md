# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Full-stack healthcare web application for visually impaired users to photograph prescription labels and receive audio-visual medication dosage information.

Primary users: visually impaired and elderly individuals. They rely heavily on screen readers and high-contrast visuals. Total accessibility and absolute accuracy are everything.

The product optimises for:
- strict accessible design (WCAG AAA contrast and screen-reader standards)
- robust OCR text-extraction from real-world photos
- instant audio-visual playback of dosage instructions

Avoid over-engineering. If a simpler solution exists, use it.

## Architecture

Monorepo combining a vanilla TypeScript frontend and a Python FastAPI backend.

### Rules

- The `.env` and `.env.* files store environmental variables Never hardcode secrets, credentials, or API keys.
- Read `frontend/README.md` and `backend-python/README.md` before creating or modifying files.
- The README files are the source of truth for project structure and design patterns.

### App Entry Points
- Frontend: `index.html` → `src/app.ts`
- Backend: `backend-python/main.py` → `app/main.py`

### Project Structure

- Frontend
  - `core/` — infrastructure (API client, routing, stores)
  - `features/` — domain modules
  - `pages/` — application screens
  - `shared/` — reusable UI, utilities, types, styles

- Backend
  - `core/` — configuration, logging, security
  - `db/` — database layer
  - `features/` — models, schemas, services, routers
  - `utils/` — shared utilities

### Tech Stack

- **Frontend:** Vanilla TypeScript (strict mode), Vite (build tool), HTML5, CSS3
- **Backend:** Python 3.11+, FastAPI, SQLAlchemy 2.0, Pydantic v2, PostgreSQL (AWS RDS)
- **CI/CD:** AWS Deployment pipelines

**DO NOT introduce:**

- **Frontend:** SPA frameworks (React, Vue, Angular); MPA frameworks (Next.js, Astro); State management libraries (Redux, Zustand); Third-party UI/CSS frameworks (Tailwind, Material UI, styled-components)
- **Backend:** Alternative ORMs (Tortoise, SQLModel, or legacy `declarative_base()`); Horizontal layering (global controllers/routers folders); Direct raw SQL queries where SQLAlchemy ORM models apply