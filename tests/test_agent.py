from app.agent import fallback, relevance_score
from app.memory import MemoryItem
from app.schemas import IncidentInput


def test_fallback_has_structured_hypotheses_and_steps():
    incident = IncidentInput(service="Checkout API", symptom="Intermittent 502 Bad Gateway", logs="upstream timeout")
    result = fallback(incident, [])
    assert result["hypotheses"]
    assert result["investigation_steps"]
    assert result["investigation_steps"][0]["order"] == 1


def test_memory_changes_investigation_plan():
    incident = IncidentInput(service="Checkout API", symptom="Intermittent 502 Bad Gateway", logs="upstream timeout")
    memory = MemoryItem(text="Service: Checkout API. Confirmed root cause: connection pool saturation. Resolution: restored pool configuration.", memory_id="INC-42")
    cold = fallback(incident, [])
    informed = fallback(incident, [memory])
    assert informed["investigation_steps"][0]["memory_informed"] is True
    assert len(informed["investigation_steps"]) == len(cold["investigation_steps"]) + 1
    assert informed["memory_impact"] != cold["memory_impact"]


def test_relevance_prefers_matching_service_and_signature():
    incident = IncidentInput(service="payments-api", symptom="HTTP 502 after deployment", logs="connection pool at 100%")
    match = MemoryItem(text="Service: payments-api. Confirmed root cause: connection pool saturation after deployment.")
    unrelated = MemoryItem(text="Service: search-api. Confirmed root cause: index corruption.")
    assert relevance_score(incident, match) > relevance_score(incident, unrelated)
