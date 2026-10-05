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

## Deploy on Vercel (One-Click)

This repository is Vercel-ready with:
- Frontend static build from `frontend/`
- FastAPI backend exposed as a Vercel Python function at `/api/*`

### Deploy

1. Import this repository in Vercel.
2. Keep the default root directory (repository root).
3. Add environment variables in Vercel project settings:
   - `DATABASE_URL`
   - `JWT_SECRET_KEY`
   - Optional: `REDIS_URL`, `VITE_API_URL`

If `VITE_API_URL` is not set, the frontend uses same-origin `/api/v1` automatically.

## Implemented MVP Scope

- Multi-format input normalization (text/pdf/image/video/url metadata path)
- Configurable transform parameters
- Model-agnostic selection abstraction (Claude/HF/local policy)
- Core API contracts for transform/history/output/export/publish
- Parallel generation of all requested outputs
- Docker + Kubernetes + Terraform scaffolds for deployment targets
