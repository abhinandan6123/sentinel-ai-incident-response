# Sentinel architecture

```text
                         ┌──────────────────────────┐
                         │      Sentinel Console    │
                         │ incident + evidence UX  │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │      FastAPI API         │
                         │ validation + orchestration│
                         └────────────┬─────────────┘
                                      │
                   ┌──────────────────┴──────────────────┐
                   ▼                                     ▼
        ┌────────────────────┐                 ┌────────────────────┐
        │ Hindsight Recall   │                 │ Evidence / Agent   │
        │ prior confirmed    │───────────────►│ hypotheses + plan  │
        │ experiences        │                 └─────────┬──────────┘
        └────────────────────┘                           │
                                                         ▼
                                               ┌───────────────────┐
                                               │ Engineer review   │
                                               │ confirm outcome   │
                                               └─────────┬─────────┘
                                                         │
                                                         ▼
                                               ┌───────────────────┐
                                               │ Hindsight Retain  │
                                               │ cause + resolution│
                                               │ + recurrence runbook│
                                               └───────────────────┘
```

## Design principle

Sentinel separates three kinds of information:

1. **Current evidence** — supplied by the engineer for the active incident.
2. **AI hypotheses** — generated suggestions that must be verified.
3. **Confirmed experience** — outcomes an engineer explicitly verified and chose to retain.

Hindsight is therefore part of the decision workflow, not a transcript archive. A recalled experience changes investigation prioritization, but it never authorizes a production action.

## Reliability

- If Groq is unavailable, Sentinel falls back to deterministic incident heuristics.
- If the app is in `DEMO_MODE=true`, memory is local and clearly labelled.
- A submission claiming live Hindsight integration must be demonstrated with `DEMO_MODE=false` and a real Hindsight bank.
- No endpoint executes shell commands, rollbacks, deployments, or infrastructure changes.
