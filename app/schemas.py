from pydantic import BaseModel, Field
class IncidentInput(BaseModel):
    service: str = Field(min_length=2, max_length=100)
    symptom: str = Field(min_length=5, max_length=500)
    environment: str = Field(default="staging", max_length=100)
    logs: str = Field(default="", max_length=5000)
    deployment: str = Field(default="", max_length=500)
class IncidentAnalysis(BaseModel):
    incident_id: str
    summary: str
    likely_causes: list[str]
    investigation_steps: list[str]
    recalled_memories: list[str]
    memory_used: bool
    disclaimer: str = "Suggestions only. Verify evidence before taking action."
class ResolutionInput(BaseModel):
    incident_id: str
    service: str
    symptom: str
    environment: str = "staging"
    logs: str = ""
    deployment: str = ""
    confirmed_root_cause: str = Field(min_length=5, max_length=1000)
    resolution_steps: str = Field(min_length=5, max_length=2000)
    outcome: str = Field(default="resolved", max_length=100)
