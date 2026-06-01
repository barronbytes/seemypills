# SeeMyPills ➔ Backend (Python)

This backend is a Python FastAPI service deployed on AWS that accepts image uploads, runs OCR and computer vision to extract medication label text, and returns structured data to the frontend.

## Tech Stack

**Backend:** FastAPI (Python)
**Runtime:** Uvicorn (ASGI server)
**Tooling:** uv, pytest

## Project Structure

```bash
seemypills/backend-python/
├── app/
│   ├── core/               # Global setup (config, logging, security)
│   ├── db/                 # Database layer (base, session, mixins)
│   ├── features/           # Domain modules (vertical slices)
│   │   └── auth/           # Auth feature (models, router, schemas, services)
│   ├── utils/              # Shared utilities
│   └── main.py             # FastAPI application entry point
├── tests/
├── main.py                 # Application runner
├── pyproject.toml          # Dependencies (managed via uv)
└── README.md
```

## Prerequisite Installations

- IDE (VS Code, Cursor, etc.)
- Python v3.13 or higher
- uv (Package Manager)
- PostgreSQL (database)

## Dev Dependencies
- pytest >=9.0.3: testing framework

## Dependencies
- FastAPI >=0.136.1: web framework for building REST APIs
- uvicorn >=0.46.0: ASGI server to run the FastAPI application
- SQLAlchemy >=2.0.49: ORM for database modeling and queries
- alembic >=1.18.4: database schema migration tool
- pydantic-settings >=2.14.0: settings management via environment variables
- psycopg2-binary >=2.9.12: PostgreSQL driver
- easyocr >=1.7.2: OCR engine for reading text from medication images
- opencv-python >=4.13.0.92: image preprocessing and computer vision
- httpx >=0.28.1: async-capable HTTP client
- python-dotenv >=1.2.2: `.env` file loading

## Quick Start

## Usage

## System Design