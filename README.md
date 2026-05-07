# CommitVigil

[![CI](https://github.com/daretechie/CommitVigil/actions/workflows/ci.yml/badge.svg)](https://github.com/daretechie/CommitVigil/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)

> FastAPI lab for extracting commitments from chat and Git commit text, with Slack/reporting components, PostgreSQL, Redis, background workers, and Prometheus metrics.

## Problem

Teams often make commitments in chat, commit messages, or review comments, but those commitments are hard to track later. This project explores a small service that extracts structured commitment records and connects them to reporting and feedback workflows.

This is an application/backend lab, not a lead DevOps portfolio project.

## Current Scope

Implemented or represented in the repo:

- FastAPI app with versioned API routing.
- `/ingest/raw` endpoint for extracting commitments from raw text.
- `/ingest/git` endpoint for extracting commitments from Git commit messages.
- API-key protection and request rate limiting.
- PostgreSQL, Redis, worker, and Prometheus services in Docker Compose.
- Structured logging and basic health checks.
- Tests for API, worker, database, Slack, reports, safety, and performance paths.

Not currently proven in this README:

- GitHub webhook HMAC validation.
- Direct-push detection.
- Large-diff analysis from real GitHub payloads.
- Production Slack alert screenshots.
- End-to-end deployment evidence.

Those should be added before presenting this as a GitHub security or DevOps control.

## Architecture

```text
Client / script
  -> CommitVigil API (FastAPI)
  -> ingestion endpoint
  -> commitment extraction
  -> database / reporting paths
  -> optional Slack or report output

Docker Compose
  -> api
  -> worker
  -> redis
  -> postgres
  -> prometheus
```

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI, Python 3.12 |
| Background jobs | ARQ, Redis |
| Database | PostgreSQL, SQLModel/Alembic |
| Reporting / templates | Jinja2 |
| Observability | Prometheus, structured logging |
| Testing | pytest, pytest-asyncio, httpx |

## Quick Start

```bash
git clone https://github.com/darestack/CommitVigil.git
cd CommitVigil
cp .env.example .env
docker compose up -d
```

API:

```text
http://localhost:8000
http://localhost:8000/docs
http://localhost:8000/health
```

## Main Endpoints

| Endpoint | Purpose |
|---|---|
| `POST /api/v1/ingest/raw` | Extract a structured commitment from raw chat-style text |
| `POST /api/v1/ingest/git` | Extract a structured commitment from a Git commit message |
| `GET /health` | Check API, database, and Redis status |
| `GET /metrics` | Prometheus metrics, protected by API key |

## Evidence To Add

| Evidence | Status |
|---|---|
| CI run screenshot | Needed |
| Example request and response | Needed |
| Prometheus metrics screenshot | Needed |
| Worker log showing async processing | Needed |
| Slack/report output screenshot | Needed before alerting claims |
| GitHub webhook fixture and HMAC test | Needed before webhook/security claims |

## Portfolio Note

This repo should stay unpinned until the README, product scope, and proof artifacts are tighter. If it is kept public, frame it as a backend/automation lab rather than a production DevOps security system.
