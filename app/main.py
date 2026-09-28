from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app import config
from app.agent import analyze, relevance_score
from app.memory import MemoryService
from app.schemas import (
    HealthResponse,
    IncidentAnalysis,
    IncidentInput,
    MemoryEvidence,
    MemoryStatus,
    ResolveResponse,
    ResolutionInput,
)

STATIC = Path(__file__).parent / "static"
memory = MemoryService()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    memory.close()


app = FastAPI(
    title=config.APP_NAME,
    version=config.APP_VERSION,
    description=(
        "Memory-driven incident investigation. Sentinel recalls confirmed operational experience "
        "from Hindsight, uses it to prioritize diagnostics, and retains only engineer-verified outcomes."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)
app.mount("/static", StaticFiles(directory=STATIC), name="static")


def build_query(incident: IncidentInput) -> str:
    return (
        f"Confirmed production incidents for service {incident.service}. "
        f"Symptoms: {incident.symptom}. Environment: {incident.environment}. "
        f"Logs: {incident.logs}. Deployment: {incident.deployment}. "
        "Prior root causes, resolution steps, runbooks and verified outcomes."
    )


def memory_evidence(incident: IncidentInput, recalled) -> list[MemoryEvidence]:
    evidence = []
    for idx, item in enumerate(recalled):
        score = relevance_score(incident, item)
        evidence.append(
            MemoryEvidence(
                id=item.memory_id or f"memory-{idx + 1}",
                service=incident.service,
                title="Confirmed operational experience",
                text=item.text,
                relevance=score,
                source="hindsight" if memory.mode == "hindsight" else "local-demo",
                confirmed=item.confirmed,
            )
        )
    return sorted(evidence, key=lambda x: x.relevance, reverse=True)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home():
    return (STATIC / "index.html").read_text(encoding="utf-8")


@app.get("/api/health", response_model=HealthResponse, tags=["System"], summary="Service and memory configuration status")
def health():
    return {
        "status": "ok",
        "service": config.APP_NAME,
        "version": config.APP_VERSION,
        "memory": memory.status(),
        "llm_configured": bool(config.GROQ_API_KEY),
    }


@app.get("/api/memory/status", response_model=MemoryStatus, tags=["Memory"], summary="Show which memory provider is active")
def memory_status():
    return memory.status()


@app.post(
    "/api/incidents/analyze",
    response_model=IncidentAnalysis,
    tags=["Incident Intelligence"],
    summary="Analyze an incident using current evidence and recalled experience",
)
def analyze_incident(incident: IncidentInput):
    incident_id = str(uuid4())
    try:
        recalled = memory.recall(build_query(incident), limit=5)
        result = analyze(incident, recalled)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Incident analysis failed: {type(exc).__name__}: {exc}") from exc

    evidence = memory_evidence(incident, recalled)
    result["recalled_memories"] = evidence
    result["memory_used"] = bool(evidence)
    return IncidentAnalysis(incident_id=incident_id, **result)


@app.post("/api/analyze", response_model=IncidentAnalysis, tags=["Compatibility"], include_in_schema=False)
def analyze_legacy(incident: IncidentInput):
    return analyze_incident(incident)


@app.post("/api/resolve", response_model=ResolveResponse, tags=["Compatibility"], include_in_schema=False)
def resolve_legacy(resolution: ResolutionInput):
    return resolve_incident(resolution.incident_id, resolution)


@app.post(
    "/api/incidents/{incident_id}/resolve",
    response_model=ResolveResponse,
    tags=["Incident Learning"],
    summary="Retain an engineer-confirmed incident outcome",
)
def resolve_incident(incident_id: str, resolution: ResolutionInput):
    if resolution.incident_id != incident_id:
        raise HTTPException(status_code=400, detail="incident_id in the path must match the request body")

    content = f"""CONFIRMED INCIDENT EXPERIENCE
Incident ID: {resolution.incident_id}
Service: {resolution.service}
Environment: {resolution.environment}
Symptom: {resolution.symptom}
Logs/evidence: {resolution.logs or 'not provided'}
Deployment/change: {resolution.deployment or 'not provided'}

CONFIRMED ROOT CAUSE BY ENGINEER:
{resolution.confirmed_root_cause}

CONFIRMED RESOLUTION STEPS:
{resolution.resolution_steps}

APPROVED RUNBOOK FOR RECURRENCE:
{resolution.runbook or 'No explicit runbook supplied; use the confirmed resolution steps as historical context.'}

OUTCOME:
{resolution.outcome}

VERIFICATION NOTES:
{resolution.verification_notes or 'Engineer confirmed the outcome in the incident workflow.'}

TRUST BOUNDARY: This is a historical, engineer-confirmed experience. It is not proof that a future incident has the same cause.
"""
    try:
        memory_id = memory.retain(
            content,
            context="Engineer-confirmed incident resolution and recurrence runbook",
            metadata={
                "source": "sentinel",
                "kind": "confirmed-incident",
                "service": resolution.service,
                "environment": resolution.environment,
                "incident_id": resolution.incident_id,
            },
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Could not retain incident: {type(exc).__name__}: {exc}") from exc

    return {
        "status": "retained",
        "memory_mode": memory.mode,
        "memory_id": memory_id,
        "message": "Engineer-confirmed outcome retained. Run the next incident to see memory change the investigation.",
    }


@app.post("/api/demo/reset", tags=["Demo"], summary="Clear local demo memory")
def reset_demo():
    if memory.mode != "demo":
        raise HTTPException(status_code=400, detail="Reset is available only in DEMO_MODE.")
    memory.demo_memories.clear()
    return {"status": "reset", "message": "Local demo memory cleared."}
