# SeeMyPills ➔ Backend (Python)

This backend is a Python FastAPI service deployed on AWS, built using a vertically-sliced project structure and integrated with a TypeScript frontend. It operates as a concurrent, request-response processing pipeline that handles image ingestion, computer vision extraction (OCR), and database persistence (AWS RDS PostgreSQL) within a single API lifecycle.

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
│   ├── features/           # Domain modules (models, schemas, servics, routers)
│   ├── utils/              # Shared utilities
│   └── main.py             # FastAPI application entry point
├── tests/
├── .env.development        # Local environmental variables
├── .env.production         # AWS enviornmental variables
├── pyproject.toml          # Dependencies (managed via uv)
├── uv.lock
└── README.md

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
- python-multipart >=0.0.32: parses multipart form data for file uploads
```

## Quick Start

## Usage

**Local Development**

```bash
uv run uvicorn app.main:app --reload    # start FastAPI dev server
uv run pytest -m "not integration"      # run unit tests only (excludes DB connection tests)
uv run pytest                           # run all tests including integration tests
uv run pytest tests/folder/             # run tests on speciic folder
uv run pytest tests/folder/file.py -v   # run tests on specific file (-v flag is optional)
uv add <package>                        # add a dependency
```

### Database Workflow

Terminal PostgreSQL:

```bash
sudo psql -U <db_user> -d <db_name>     # enter the database console
\l                                      # list all databases (run inside psql)
\dt                                     # list tables in the current database (run inside psql)
```

Alembic Workflow: When a model in `app/features/<feature>/models.py` changes, track it with a migration:

1. Edit the model: Update the SQLAlchemy model in `models.py`
2. Generate the migration: Run `uv run alembic revision --autogenerate -m "describe the change"`
3. Review the file: Check the generated `upgrade()`/`downgrade()` in the new `alembic/versions/` file
4. Commit together: Commit the migration file alongside the model change in the same PR
5. Apply the migration: Run `uv run alembic upgrade head`

## System Design