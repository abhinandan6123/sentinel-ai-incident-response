from app.agent import fallback
from app.schemas import IncidentInput

def test_fallback_has_causes_and_steps():
    i=IncidentInput(service="Checkout API",symptom="Intermittent 502 Bad Gateway",logs="upstream timeout")
    r=fallback(i,[])
    assert r["likely_causes"] and r["investigation_steps"]

def test_memory_is_reflected_in_plan():
    i=IncidentInput(service="Checkout API",symptom="Intermittent 502 Bad Gateway",logs="upstream timeout")
    a=fallback(i,[]); b=fallback(i,["Prior confirmed incident: timeout configuration caused 502s"])
    assert len(b["investigation_steps"]) == len(a["investigation_steps"])+1
    assert "recalled prior" in b["investigation_steps"][0].lower()
