# Incident Response Agent (Hindsight)

A focused prototype for the official **Incident Response Agent** problem statement. It helps an on-call engineer investigate a recurring incident by recalling prior confirmed incidents from Hindsight.

## What it demonstrates
1. Submit an incident.
2. Recall related memories from Hindsight.
3. Generate investigation steps (Groq is optional; a deterministic fallback is included).
4. Confirm the actual root cause and resolution.
5. Retain that confirmed outcome in Hindsight.
6. Submit a similar incident and inspect recalled experience.

**Safety:** recommendations only. It does not execute commands or change production systems. Use synthetic/demo data only.

## Requirements
Python 3.11+, Hindsight Cloud credentials or reachable server, optional Groq API key.

## Windows PowerShell setup
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```
Edit `.env`. For local UI testing, keep `DEMO_MODE=true`. For actual Hindsight integration, create a bank in Hindsight Cloud, set `HINDSIGHT_API_KEY`, `HINDSIGHT_BANK_ID`, and `DEMO_MODE=false`.
```powershell
python -m app.seed_demo
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000

## Environment
- `HINDSIGHT_BASE_URL`: defaults to `https://api.hindsight.vectorize.io`
- `HINDSIGHT_API_KEY`: required when `DEMO_MODE=false`
- `HINDSIGHT_BANK_ID`: bank ID created in Hindsight
- `HINDSIGHT_AUTO_CREATE_BANK`: optional attempt to create bank
- `GROQ_API_KEY`: optional
- `GROQ_MODEL`: defaults to `openai/gpt-oss-120b`
- `DEMO_MODE`: `true` uses local in-memory demo memory; **do not claim this is live Hindsight**

## API
`GET /api/health`, `POST /api/analyze`, `POST /api/resolve`, `POST /api/demo/reset`.

## Tests
```powershell
pytest -q
```

## Architecture
Browser UI → FastAPI → Hindsight recall → analysis → human-confirmed resolution → Hindsight retain.

## Official resources
- https://hindsight.vectorize.io/
- https://docs.hindsight.vectorize.io/python-sdk/
- https://github.com/vectorize-io/hindsight
- https://groq.com/

The Hindsight SDK evolves; use the current official docs for setup and API changes. The app uses the documented `hindsight-client` interface (`Hindsight`, `create_bank`, `retain`, `recall`).

## Submission-grade workflow assets
- `docs/HINDSIGHT_EXPLANATION.md` — concise memory architecture and trust boundaries.
- `docs/DEMO_RUNBOOK.md` — judge demo story and evidence checklist.
- `docs/RELEASE_CHECKLIST.md` — local QA and submission checklist.
- `docs/content/` — editable article, social-post, and video-script drafts. Replace placeholders and claims with observed results before publishing.
- `data/demo_incidents.json` — realistic synthetic incident examples for a repeatable demo.
- `.github/workflows/tests.yml` — CI test workflow.
- `Dockerfile` — container build entry point.

## Important release gate
This repository is a production-oriented hackathon deliverable, **not a claim of production deployment or verified live integration**. Before submitting, run the application, run `pytest -q`, and prove a real Hindsight retain → recall cycle with `DEMO_MODE=false`. Keep credentials in `.env` or your deployment secret store; never commit them. The local demo mode is process-local and resets when the process restarts.

## Suggested judge evidence
Capture (1) health/status showing Hindsight mode, (2) the confirmed incident being retained, (3) a later incident retrieving it, and (4) the memory-informed change to the investigation plan. Do not present synthetic data as a real production incident or claim measured time savings without a measured evaluation.
