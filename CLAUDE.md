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

## Tech Stack

### Technology Used

- **Frontend:** Vanilla TypeScript (strict mode), Vite (build tool), HTML5, CSS3
- **Backend:** Python 3.11+, FastAPI, SQLAlchemy 2.0, Pydantic v2, PostgreSQL (AWS RDS)
- **CI/CD:** AWS Deployment pipelines

### DO NOT introduce

- **Frontend:** SPA frameworks (React, Vue, Angular); MPA frameworks (Next.js, Astro); State management libraries (Redux, Zustand); Third-party UI/CSS frameworks (Tailwind, Material UI, styled-components)
- **Backend:** Alternative ORMs (Tortoise, SQLModel, or legacy `declarative_base()`); Horizontal layering (global controllers/routers folders); Direct raw SQL queries where SQLAlchemy ORM models apply

## System Architecture

Monorepo combining a vanilla TypeScript frontend and a Python FastAPI backend.

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

## Development Rules

### General

- The `.env` and `.env.* files store environmental variables Never hardcode secrets, credentials, or API keys.
- Read `frontend/README.md` and `backend-python/README.md` before creating or modifying files.
- The README files are the source of truth for project structure and design patterns.

### Frontend Rules

- **Layout Engines:** Use exclusively Flexbox and CSS Grid for layout structure; do not use legacy floats, positioning hacks, or external CSS grid frameworks.
- **Semantic Tags:** Lean heavily on native HTML5 primitives; do not reinvent what the browser natively handles. DO NOT rely on `<div>` tag when other semantic tags can group related context better for accessiblility.
- **Color System (60-30-10):** Structure the interface using a strict surface-area distribution: 60% dominant neutral canvas (backgrounds), 30% structural text and secondary containers (typography, borders, cards), and 10% high-contrast accent color reserved exclusively for primary action elements, active interactive states, and critical system feedback.
- **Spacing System:** Maintain exactly 16px of total combined spacing between vertically stacked elements, and exactly 10px between horizontally adjacent elements (inclusive of all padding, margin, and borders).
- **Element States:** Every interactive element must feature a distinct primary/secondary visual hierarchy and explicitly implement hover, focus, and disabled states.
- **Action Hierarchy:** Enforce a strict visual distinction between primary and secondary actions (e.g., solid fill vs. subtle outline) to map out clear user intent.
- **Pseudoclass States:** Every actionable element must explicitly implement distinct, high-contrast visual styles for its `:hover`, `:focus`, and `:disabled` states.
- **Accessibility (WCAG AAA Baseline):** Deliver maximum screen-reader readability and high-contrast compliance as non-negotiable defaults.
- **Zero Layout Shifts (CLS):** Use structural skeletons or explicit dimensional placeholders for all asynchronous, dynamic content.

### Backend

...

## Coding Conventions

- General
  - Descriptive variable names always — `userSessionData` not `usd`
  - Comments only when intent is non-obvious; don't comment the obvious
  - No dead code, no commented-out blocks in commits
  - Error handling must be explicit — no silent catches
- Frontend
  - TypeScript strict mode; avoid `any` entirely
  - Named exports for all shared modules (default exports only for route files)
  - async/await only — no chained `.then()` patterns
  - Components stay under 200 lines; extract when they grow beyond this
- Backend
- CI/CD

## Workflows