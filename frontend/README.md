# SeeMyPills ➔ Frontend (TypeScript)

This frontend is a vanilla TypeScript application built using a feature-based project structure, deployed on AWS and integrated with a Python backend. Users submit or take a photo for the backend to analyze, presenting patients with medication information readings.

## Tech Stack

**Frontend:** Vanilla TypeScript (HTML/CSS/TS)
**Runtime:** Web Browser (Client-side)
**Tooling:** pnpm, Vite, Vitest

## Project Structure

```bash
seemypills/frontend/
├── public/                 # Uncompiled, static assets (favicon, icons, etc.)
├── src/
│   ├── assets/             # All UI fonts/photos/media
│   ├── core/               # Global setup (API client, routing, global stores)
│   │   ├── lib/
│   │   ├── store/
│   │   ├── shared/
│   │   ├── api-client.ts
│   │   └── router.ts
│   ├── features/           # Domain pages/modules
│   ├── shared/             # Reusable components, hooks, lib, styles, types, utils
│   └── app.ts              # Main application entry point
├── tests/
├── .env
├── index.html              # Main HTML entry point
├── package.json            # Dependencies (managed via pnpm)
├── tsconfig.json           # TypeScript configuration
└── README.md

## Prerequisite Installations

- IDE (VS Code, Cursor, etc.)
- Node.js v22.15.0 or higher
- pnpm v9.x or higher (Package Manager)

## Dev Dependencies
- TypeScript version 5.9+: static typing and compilation, provided by pnpm
- @types/node: Node.js type definitions for TypeScript
- Vitest: testing framework

## Dependencies
- Vite: built-in environmental variable Loading
- zod: runtime schema validation and type-safe data parsing for backend API responses
```

## Quick Start

## Usage

## System Design