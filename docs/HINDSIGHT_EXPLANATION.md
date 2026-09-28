# How Sentinel uses Hindsight

Hindsight is the long-term operational memory layer.

### Recall

For every new incident, Sentinel sends Hindsight a query containing the service, symptom, environment, logs, and deployment context. Returned memories are rendered as **confirmed operational experience** and passed to the investigation layer as historical context.

### Retain

Sentinel does **not** retain every AI response. Retention happens only after an engineer confirms the incident outcome. The retained record contains:

- incident/service/environment context
- evidence supplied during the incident
- confirmed root cause
- confirmed resolution steps
- recurrence runbook
- outcome and verification notes

This is deliberately different from storing a chat transcript.

### Learning loop

```text
Incident A
   ↓
Generic investigation
   ↓
Engineer confirms cause + fix
   ↓
Hindsight RETAIN
   ↓
Incident B
   ↓
Hindsight RECALL
   ↓
Memory-informed investigation
```

### Trust boundary

A memory match is **not proof** that the current incident has the same root cause. Sentinel shows historical evidence separately from AI hypotheses and requires engineer verification before learning from the incident.
