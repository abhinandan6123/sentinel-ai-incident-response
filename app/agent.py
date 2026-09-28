import json
from openai import OpenAI
from app import config
from app.schemas import IncidentInput

def fallback(incident: IncidentInput, memories: list[str]) -> dict:
    text = f"{incident.symptom} {incident.logs} {incident.deployment}".lower()
    if "502" in text or "gateway" in text:
        causes = ["Upstream service unavailable or timing out", "Recent deployment introduced an incompatible change", "Connection pool or proxy saturation"]
        steps = ["Check gateway and upstream service logs for the same timestamp.", "Compare error rate and latency before and after deployment.", "Check upstream health, connection-pool saturation, and timeout configuration.", "If evidence supports a regression, follow the approved rollback/runbook process."]
    elif "timeout" in text or "latency" in text:
        causes = ["Dependency latency or timeout mismatch", "Resource saturation", "A recent change increased request cost"]
        steps = ["Correlate latency with dependency and resource metrics.", "Inspect recent changes and logs for the affected request path.", "Check configured timeouts across service boundaries.", "Validate a proposed mitigation in staging before production."]
    else:
        causes = ["Recent code/configuration change", "Dependency failure", "Resource or capacity issue"]
        steps = ["Establish incident start time and affected scope.", "Inspect service logs and health checks around the start time.", "Compare recent deployments/configuration changes.", "Check dependencies and resource saturation before changing production."]
    if memories: steps.insert(0, "Compare this incident with recalled prior incident(s); verify whether the same signature is present.")
    return {"summary":f"Investigation plan for {incident.service}: {incident.symptom}","likely_causes":causes,"investigation_steps":steps}

def analyze(incident: IncidentInput, memories: list[str]) -> dict:
    if not config.GROQ_API_KEY: return fallback(incident, memories)
    client = OpenAI(api_key=config.GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
    payload = {"incident":incident.model_dump(),"recalled_hindsight_memories":memories,
      "instructions":"Return ONLY JSON with summary, likely_causes (array), investigation_steps (array). Treat memories as historical context, not proof. Do not invent logs or claim a fix is verified. Suggest safe diagnostics only; never execute actions."}
    response = client.chat.completions.create(model=config.GROQ_MODEL, messages=[{"role":"system","content":"Return concise valid JSON only."},{"role":"user","content":json.dumps(payload)}],temperature=0.2)
    try:
        data=json.loads(response.choices[0].message.content or "{}")
        return {"summary":str(data.get("summary","Incident investigation")),"likely_causes":[str(x) for x in data.get("likely_causes",[])][:5],"investigation_steps":[str(x) for x in data.get("investigation_steps",[])][:8]}
    except (json.JSONDecodeError, TypeError): return fallback(incident, memories)
