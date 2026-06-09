# SeeMyPills ➔ Frontend (TypeScript)

This frontend is a vanilla TypeScript application deployed on AWS, built using a feature-based project structure and integrated with a Python backend. Users submit or take a photo for the backend to analyze, presenting patients with medication information readings.

## Tech Stack

**Frontend:** Vanilla TypeScript (HTML/CSS/TS)
**Runtime:** Web Browser (Client-side)
**Tooling:** pnpm, Vite, Vitest, ESLint

## Project Structure

```bash
seemypills/frontend/
├── public/                 # Static runtime assets not processed by Vite for dynamically injected HTML
├── src/
│   ├── assets/             # Static build time assets processed by Vite for index.html or imported by TypeScript
│   ├── core/               # App infrastructure (API client, routing, global stores)
│   │   ├── lib/
│   │   ├── store/
│   │   ├── shared/
│   │   ├── api-client.ts
│   │   └── router.ts
│   ├── features/           # Domain pages/modules
│   ├── pages/              # Individual app pages
│   ├── shared/             # Reusable UI components, scripts, styles, typs, util, etc.
│   └── app.ts              # Main application entry point
├── tests/
├── .env
├── .gitignore
├── 404.html
├── index.html              # Main HTML entry point
├── eslint.config.js        # Static anaysis to catch errors and enforce code styles
├── package.json            # Dependencies (managed via pnpm)
├── tsconfig.json           # TypeScript configuration
├── vite-env.d.ts
└── README.md

## Prerequisite Installations

- IDE (VS Code, Cursor, etc.)
- Node.js v22.15.0 or higher
- pnpm v9.x or higher (Package Manager)

## Dev Dependencies
- TypeScript version 5.9+: static typing and compilation, provided by pnpm
- @types/node: Node.js type definitions for TypeScript
- Vitest: testing framework
- ESLint (`eslint`, `@eslint/js`, `typescript-eslint`): linting with TypeScript-aware rules

## Dependencies
- Vite: built-in environmental variable Loading
- zod: runtime schema validation and type-safe data parsing for backend API responses
```

## Quick Start

## Usage

**Local Development**

```bash
pnpm dev          # start Vite dev server at http://localhost:5173
pnpm typecheck    # run TypeScript type checking without emitting files
pnpm lint         # run ESLint across all source files
pnpm test         # run Vitest in watch mode for local development
pnpm build        # type-check then bundle for production (tsc && vite build)
pnpm preview      # preview the production build locally
```

## System Design