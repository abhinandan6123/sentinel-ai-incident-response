from pydantic import BaseModel, Field, field_validator


class IncidentInput(BaseModel):
    service: str = Field(min_length=2, max_length=100)
    symptom: str = Field(min_length=5, max_length=500)
    environment: str = Field(default="production", max_length=100)
    logs: str = Field(default="", max_length=8000)
    deployment: str = Field(default="", max_length=1000)

    @field_validator("service", "symptom", "environment", mode="before")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip() if isinstance(value, str) else value


class MemoryEvidence(BaseModel):
    id: str = ""
    service: str = ""
    title: str = "Prior confirmed incident"
    text: str
    relevance: int = Field(default=0, ge=0, le=100)
    source: str = "hindsight"
    confirmed: bool = True


class InvestigationHypothesis(BaseModel):
    title: str
    rationale: str
    priority: str = Field(default="medium")


class InvestigationStep(BaseModel):
    order: int
    action: str
    why: str = ""
    memory_informed: bool = False


class IncidentAnalysis(BaseModel):
    incident_id: str
    summary: str
    severity: str = "medium"
    hypotheses: list[InvestigationHypothesis]
    investigation_steps: list[InvestigationStep]
    evidence_signals: list[str]
    recalled_memories: list[MemoryEvidence]
    memory_used: bool
    memory_impact: str
    next_best_question: str
    disclaimer: str = "Historical memory is context, not proof. Verify current evidence before taking action."


class ResolutionInput(BaseModel):
    incident_id: str
    service: str
    symptom: str
    environment: str = "production"
    logs: str = Field(default="", max_length=8000)
    deployment: str = Field(default="", max_length=1000)
    confirmed_root_cause: str = Field(min_length=5, max_length=1500)
    resolution_steps: str = Field(min_length=5, max_length=3000)
    runbook: str = Field(default="", max_length=4000)
    outcome: str = Field(default="resolved", min_length=2, max_length=100)
    verification_notes: str = Field(default="", max_length=1500)


class ResolveResponse(BaseModel):
    status: str
    memory_mode: str
    memory_id: str
    message: str


class MemoryStatus(BaseModel):
    mode: str
    provider: str
    bank_id: str
    configured: bool
    demo_warning: str | None = None


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    memory: MemoryStatus
    llm_configured: bool
