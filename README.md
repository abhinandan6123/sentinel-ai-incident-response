# Sentinel — Memory-Driven Incident Response

**Incident intelligence that remembers what engineers actually confirmed.**

Sentinel is an AI-assisted incident investigation workflow built around **Hindsight agent memory**. It recalls relevant historical incidents, keeps historical evidence separate from AI hypotheses, helps an engineer prioritize diagnostics, and retains only engineer-confirmed outcomes for future incidents.

> **Safety boundary:** Sentinel provides investigation suggestions only. It does not execute commands, roll back deployments, modify infrastructure, or treat memory as proof.

## Why Sentinel

A generic incident assistant starts from the current prompt. An experienced on-call engineer starts with the current evidence **and what the team already learned**.

Sentinel makes that learning loop explicit:

```text
Incident → Recall → Investigate → Engineer verifies → Retain → Future incident improves
```

The key demo is a before/after:

- **Cold investigation:** generic diagnostics when no relevant experience exists.
- **Memory-informed investigation:** a prior confirmed incident is recalled and changes investigation prioritization.

## Stack

- **FastAPI + Pydantic** — API and validation
- **Hindsight** — persistent operational memory
- **Groq / OpenAI-compatible API** — optional structured reasoning layer
- **Deterministic fallback** — keeps the workflow usable when an LLM is unavailable
- **Vanilla HTML/CSS/JS** — zero-build professional incident console
- **Pytest** — automated checks

## Local setup

Python 3.11+ is recommended.

```bash
python -m venv .venv
source .venv/Scripts/activate  # Git Bash on Windows
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

For a UI-only rehearsal:

```bash
DEMO_MODE=true uvicorn app.main:app --reload
```

For the actual Hindsight integration, configure `HINDSIGHT_API_KEY` and `HINDSIGHT_BANK_ID`, set `DEMO_MODE=false`, then run:

```bash
uvicorn app.main:app --reload
```

Open:

- App: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Health: `http://127.0.0.1:8000/api/health`

## Environment variables

| Variable | Purpose |
|---|---|
| `DEMO_MODE` | Local memory fallback when `true`; set `false` for real Hindsight |
| `HINDSIGHT_BASE_URL` | Hindsight API base URL |
| `HINDSIGHT_API_KEY` | Hindsight credential; never commit it |
| `HINDSIGHT_BANK_ID` | Persistent incident memory bank |
| `HINDSIGHT_AUTO_CREATE_BANK` | Optional bank creation attempt |
| `GROQ_API_KEY` | Optional model credential |
| `GROQ_MODEL` | Model used through Groq's OpenAI-compatible API |

## API surface

### System

`GET /api/health` — service, version, memory provider and LLM configuration.

`GET /api/memory/status` — explicit memory-provider status.

### Incident intelligence

`POST /api/incidents/analyze` — recalls relevant experience and generates hypotheses, evidence signals and an investigation plan.

### Learning

`POST /api/incidents/{incident_id}/resolve` — retains an engineer-confirmed root cause, resolution and recurrence runbook.

### Demo

`POST /api/demo/reset` — clears only local demo memory.

## Hindsight design

Hindsight is not used as a decorative chat-history store. Sentinel retains structured **confirmed incident experience** and recalls it during a later investigation.

The retained record includes:

```text
Service / environment
Current evidence
Confirmed root cause
Confirmed resolution
Recurrence runbook
Outcome
Verification notes
```

See [`docs/HINDSIGHT_EXPLANATION.md`](docs/HINDSIGHT_EXPLANATION.md) and [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Testing

```bash
pytest -q
python -m compileall app
```

The tests specifically verify that recalled memory changes the investigation plan and that matching incident context receives a stronger relevance signal.

## Deployment on Render

A `render.yaml` is included. Set these secrets in Render:

- `HINDSIGHT_API_KEY`
- `GROQ_API_KEY` (optional)

For a submission claiming Hindsight integration, set `DEMO_MODE=false` and verify a real retain → recall cycle before recording the demo.

## Submission evidence

The official judging model emphasizes innovation, Hindsight memory, technical implementation, UX and real-world impact. The strongest evidence in this repository is therefore the **memory learning loop**, not a generic chatbot response.

Before publishing, add observed screenshots, the live URL, demo video and measured results only if they were actually tested.

## Project docs

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- [`docs/HINDSIGHT_EXPLANATION.md`](docs/HINDSIGHT_EXPLANATION.md)
- [`docs/DEMO_RUNBOOK.md`](docs/DEMO_RUNBOOK.md)
- [`docs/RELEASE_CHECKLIST.md`](docs/RELEASE_CHECKLIST.md)
- [`docs/SUBMISSION.md`](docs/SUBMISSION.md)

## Official references

- Hindsight: https://hindsight.vectorize.io/
- Hindsight GitHub: https://github.com/vectorize-io/hindsight
- Groq: https://groq.com/
