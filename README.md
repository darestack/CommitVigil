# CommitVigil

[![CI](https://github.com/daretechie/CommitVigil/actions/workflows/ci.yml/badge.svg)](https://github.com/daretechie/CommitVigil/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)

> GitHub webhook listener that monitors commits and pull requests for risky patterns,
> evaluates developer commitments against actual delivery, and sends Slack alerts on violations.

---

## What It Does

CommitVigil sits between your GitHub repository and your team's Slack channel. It:

1. **Receives GitHub webhook events** — push, pull_request, commit comment
2. **Scans for risky patterns**:
   - Direct pushes to `main`/`master` without a PR
   - Unusually large diffs (configurable threshold)
   - Commit messages containing secret-like strings
   - Soft commitments ("I'll fix this later", "TODO: refactor") tracked against follow-through
3. **Scores and classifies** the event using structured LLM extraction (Instructor + Pydantic)
4. **Sends a Slack alert** with the violation type, commit author, and diff link

---

## Architecture

```
GitHub Repository
  └── Webhook (push / pull_request events)
        └── CommitVigil API (FastAPI)
              ├── Ingest: validates HMAC signature → queues job (ARQ + Redis)
              ├── Worker: pattern scan → LLM evaluation → risk score
              │     ├── Direct-push detector
              │     ├── Large-diff detector (threshold: configurable)
              │     └── Secret-pattern regex scan
              └── Alert dispatcher → Slack Incoming Webhook
```

**Async processing:** Events are acknowledged immediately (200 OK) and processed by an ARQ background worker — GitHub's 10-second timeout is never a concern.

---

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI (Python 3.12+) |
| Background jobs | ARQ (async Redis queue) |
| LLM extraction | Instructor + Pydantic |
| Database | PostgreSQL |
| Cache / queue | Redis |
| Observability | Prometheus + Structlog |

---

## Quick Start

```bash
git clone https://github.com/darestack/CommitVigil.git
cd CommitVigil
cp .env.example .env     # add GITHUB_WEBHOOK_SECRET and SLACK_WEBHOOK_URL
docker compose up -d
```

**Configure GitHub webhook:**
1. Repo → Settings → Webhooks → Add webhook
2. Payload URL: `https://your-domain/api/v1/ingest/raw`
3. Content type: `application/json`
4. Secret: the value from your `.env`
5. Events: Push + Pull requests

---

## Example Alert

```
⚠️  CommitVigil Alert
Repo:    darestack/my-service
Author:  daretechie
Event:   Direct push to main (no PR)
Commit:  a3f9c12 — "hotfix: temp disable auth check"
Risk:    HIGH — bypassed code review + suspicious message pattern
Link:    https://github.com/darestack/my-service/commit/a3f9c12
```

---

## Configuration

| Variable | Purpose |
|---|---|
| `GITHUB_WEBHOOK_SECRET` | HMAC secret for validating GitHub payloads |
| `SLACK_WEBHOOK_URL` | Incoming webhook URL for Slack alerts |
| `LARGE_DIFF_THRESHOLD` | Line count triggering large-diff alert (default: 500) |
| `DATABASE_URL` | PostgreSQL connection string |
| `REDIS_URL` | Redis connection string |
| `GROQ_API_KEY` / `OPENAI_API_KEY` | LLM provider key |
