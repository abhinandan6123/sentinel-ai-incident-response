# Submission notes

**Official problem statement:** Incident Response Agent (Engineering & DevOps).

**Approach:** Build an incident-response assistant for on-call engineers that remembers previous incidents, confirmed root causes, resolution steps, and runbooks using Hindsight. For a new incident, it recalls related experience and suggests evidence-driven investigation steps. After an engineer confirms the actual cause and successful resolution, the outcome is retained. A later similar incident demonstrates how recalled experience informs the next investigation.

**Memory explanation:** Hindsight is the persistent memory layer. The app calls recall during incident analysis and retain only after a human confirms the outcome. Retrieved memories are displayed separately from generated hypotheses.

**Scope/safety:** One incident workflow; synthetic scenarios; human-confirmed outcomes; recommendations only; no production actions or live monitoring integrations.

Before submitting: verify real Hindsight mode, run tests, remove secrets, push code, add actual screenshots/video URL, and confirm portal fields/deadline.
