from uuid import uuid4
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.schemas import IncidentInput, IncidentAnalysis, ResolutionInput
from app.memory import MemoryService
from app.agent import analyze
app=FastAPI(title="Incident Response Agent",version="0.1.0")
memory=MemoryService(); STATIC=Path(__file__).parent/"static"
app.mount("/static",StaticFiles(directory=STATIC),name="static")
@app.get("/",response_class=HTMLResponse)
def home(): return (STATIC/"index.html").read_text(encoding="utf-8")
@app.get("/api/health")
def health(): return {"status":"ok","memory_mode":memory.mode}
@app.post("/api/analyze",response_model=IncidentAnalysis)
def analyze_incident(incident:IncidentInput):
    incident_id=str(uuid4()); query=f"Past incidents, root causes, resolutions, runbooks: service {incident.service}; symptom {incident.symptom}; environment {incident.environment}; logs {incident.logs}; deployment {incident.deployment}"
    try: recalled=memory.recall(query); result=analyze(incident,recalled)
    except Exception as exc: raise HTTPException(status_code=502,detail=f"Memory/analysis failed: {type(exc).__name__}: {exc}")
    return IncidentAnalysis(incident_id=incident_id,summary=result["summary"],likely_causes=result["likely_causes"],investigation_steps=result["investigation_steps"],recalled_memories=recalled,memory_used=bool(recalled) and memory.mode=="hindsight")
@app.post("/api/resolve")
def resolve_incident(resolution:ResolutionInput):
    content=(f"Incident {resolution.incident_id}. Service: {resolution.service}. Environment: {resolution.environment}. Symptom: {resolution.symptom}. Logs: {resolution.logs or 'not provided'}. Deployment: {resolution.deployment or 'not provided'}. CONFIRMED root cause by engineer: {resolution.confirmed_root_cause}. Confirmed resolution steps: {resolution.resolution_steps}. Outcome: {resolution.outcome}. Engineer-confirmed historical context, not a universal rule.")
    try: memory.retain(content)
    except Exception as exc: raise HTTPException(status_code=502,detail=f"Could not retain incident: {type(exc).__name__}: {exc}")
    return {"status":"retained","memory_mode":memory.mode,"message":"Confirmed incident outcome sent to memory."}
@app.post("/api/demo/reset")
def reset_demo():
    if memory.mode!="demo": raise HTTPException(status_code=400,detail="Reset is available only in DEMO_MODE.")
    memory.demo_memories.clear(); return {"status":"reset"}
@app.on_event("shutdown")
def shutdown(): memory.close()
