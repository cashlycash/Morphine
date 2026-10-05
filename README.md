# Morphine

Production-oriented MVP scaffold for a GenAI content transformation platform.

## Project Structure

- `backend/` FastAPI API, services, schema, tests
- `frontend/` React + TypeScript dashboard scaffold
- `k8s/` Kubernetes deployment manifests
- `infra/terraform/` Terraform starter
- `docker-compose.yml` Local full stack runtime

## Backend Highlights

- FastAPI endpoints under `/api/v1`
- SQLAlchemy models for users, transformations, outputs, model catalog, usage logs
- JWT issuance endpoints (`/auth/signup`, `/auth/token`)
- Parallel output generation for:
  - LinkedIn post
  - Twitter/X thread
  - Executive summary
  - Video script package
- Output quality scoring and history retrieval
- Prometheus metrics and health endpoint

## Database Schema

- SQL migration: `/backend/alembic/versions/0001_initial.sql`
- Bootstrap schema file: `/backend/schema.sql`

## Run Locally (Docker)

```bash
docker compose up --build
```

- API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Frontend: `http://localhost:3000`

## Backend Development

```bash
cd backend
pip install -r requirements-dev.txt
pytest
uvicorn app.main:app --reload
```

## Frontend Development

```bash
cd frontend
npm install
npm run dev
```

## Implemented MVP Scope

- Multi-format input normalization (text/pdf/image/video/url metadata path)
- Configurable transform parameters
- Model-agnostic selection abstraction (Claude/HF/local policy)
- Core API contracts for transform/history/output/export/publish
- Parallel generation of all requested outputs
- Docker + Kubernetes + Terraform scaffolds for deployment targets
