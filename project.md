# Project Plan

Excellent. From now on, we'll build this exactly like a real startup engineering team.

## Sprint 1: Project Foundation (Week 1)

**Sprint Goal:** Build a production-ready development foundation. At the end of this sprint, anyone on the team should be able to clone the repository, run one command, and have the entire development environment up and running.

---

## Sprint 1 Deliverables

| Task | Status |
| --- | --- |
| Project structure | ⬜ |
| GitHub repository configuration | ⬜ |
| Python backend setup | ⬜ |
| React frontend setup | ⬜ |
| Docker Compose | ⬜ |
| PostgreSQL | ⬜ |
| Redis | ⬜ |
| Environment variables | ⬜ |
| FastAPI skeleton | ⬜ |
| React skeleton | ⬜ |
| Development tooling (Black, Ruff, ESLint, Prettier) | ⬜ |
| Pre-commit hooks | ⬜ |
| README | ⬜ |

---

## Step 1 — Create the Project Structure

Inside your GitHub repository, create the following folders.

```text
crypto-agility-scanner/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── workers/
│   │   ├── scanners/
│   │   ├── cbom/
│   │   └── main.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── scanner-engine/
│   ├── rules/
│   │   ├── python/
│   │   ├── javascript/
│   │   ├── java/
│   │   └── go/
│   │
│   ├── samples/
│   ├── scripts/
│   └── README.md
│
├── github-action/
│
├── infrastructure/
│   ├── terraform/
│   ├── kubernetes/
│   └── aws/
│
├── docker/
│
├── docs/
│
├── scripts/
│
├── .github/
│   └── workflows/
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Makefile
├── README.md
└── LICENSE
```

This structure is scalable and aligns with the architecture described in your project plan.

---

## Step 2 — Branch Strategy

We'll follow a simple Git workflow:

```text
main
│
develop
│
feature/backend-api
feature/frontend-dashboard
feature/scanner-python
feature/cbom-generator
feature/github-action
```

**Rules:**

* `main` → always stable and releasable.
* `develop` → integration branch.
* Each feature gets its own branch.
* Merge features into `develop` via pull requests.
* Merge `develop` into `main` for releases.

---

## Step 3 — Development Stack

### Backend

* Python 3.12
* FastAPI
* SQLAlchemy 2
* Alembic
* PostgreSQL
* Redis
* RQ
* Pydantic v2

## Frontend

* React
* TypeScript
* Vite
* Tailwind CSS
* shadcn/ui
* React Query
* React Router

## Database

* PostgreSQL 16

## Cache

* Redis 7

## Scanner

* Semgrep

## Containerization

* Docker
* Docker Compose

---

## Step 4 — Development Standards

### Python

* Black
* Ruff
* isort
* mypy

### Frontend tooling

* ESLint
* Prettier
* TypeScript strict mode

---

## Step 5 — Docker Architecture

We'll run the following containers locally:

```text
┌────────────────────────────┐
│ React Frontend             │
│ localhost:3000             │
└──────────────┬─────────────┘
               │
               ▼
┌────────────────────────────┐
│ FastAPI Backend            │
│ localhost:8000             │
└──────────────┬─────────────┘
               │
      ┌────────┴────────┐
      ▼                 ▼
 PostgreSQL         Redis
```

Later sprints will add scanner workers and background jobs.

---

## Step 6 — Environment Variables

Create a `.env.example` with entries like:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=crypto_scanner

DATABASE_URL=postgresql://postgres:postgres@db:5432/crypto_scanner

REDIS_URL=redis://redis:6379

SECRET_KEY=replace_with_secure_random_key

ENVIRONMENT=development
```

---

## Step 7 — Definition of Done

Sprint 1 is complete when:

* Repository structure exists.
* Backend starts successfully.
* Frontend starts successfully.
* PostgreSQL is running.
* Redis is running.
* Docker Compose launches all services with one command.
* API responds on `http://localhost:8000`.
* Frontend loads on `http://localhost:3000`.
* All code passes formatting and linting.
* Initial documentation is in place.

---

## Immediate Next Task

We'll start with the **repository scaffolding**. Create the folder structure above, commit it, and push it to your GitHub repository with a commit message such as:

```bash
git add .
git commit -m "Initialize project structure"
git push origin main
```

Once that's done, we'll move to **Sprint 1 – Step 2**, where we'll build the Docker-based development environment with FastAPI, React, PostgreSQL, and Redis.
