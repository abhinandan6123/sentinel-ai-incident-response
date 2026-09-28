# Architecture

```text
Incident form
  -> FastAPI /api/analyze
      -> Hindsight recall (prior incident facts)
      -> Optional Groq analysis / deterministic fallback
  -> Investigation plan + recalled memory evidence
  -> Engineer verifies actual root cause and fix
  -> FastAPI /api/resolve -> Hindsight retain
  -> A later similar incident can recall this experience
```

Memory is historical context, not proof. The engineer confirms the actual resolution before retention.
