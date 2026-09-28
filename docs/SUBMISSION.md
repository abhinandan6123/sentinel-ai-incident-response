# Submission notes

**Official problem:** Incident Response Agent (Engineering & DevOps).

**Product:** Sentinel — Memory-Driven Incident Response.

Sentinel recalls prior engineer-confirmed incidents through Hindsight, uses that experience to prioritize a new investigation, and retains only verified root causes, resolutions and recurrence runbooks. The core demo is a before/after learning loop: a cold investigation starts generically; a later similar incident changes because Hindsight recalls the earlier confirmed experience.

## What judges should see

1. A realistic synthetic production incident.
2. A cold investigation with generic diagnostics.
3. Engineer confirmation of the root cause, resolution and runbook.
4. Hindsight retain.
5. A similar incident with recalled experience.
6. A visibly memory-informed investigation plan.
7. Clear separation of evidence, hypotheses and historical memory.

## Trust boundary

Memory is historical context, not proof. The engineer verifies the current incident. Sentinel does not execute commands or production changes.

## Release gate

Before submission, verify the live Hindsight flow with `DEMO_MODE=false`, run the full test suite, restart the application, and confirm the retained memory is still retrievable. Replace all draft content placeholders with observed screenshots, measured results and the actual public repository/live/demo links.
