# Judge demo runbook (3–4 minutes)

## Before recording
- Start the app with `DEMO_MODE=false` and verify `/api/health` reports Hindsight mode.
- Confirm the configured Hindsight bank is reachable. Never show API keys on screen.
- Use synthetic incidents only. Keep a second terminal ready for logs.

## Story
1. **Problem (20s):** A payments API is returning 502s after a deployment. A stateless assistant has no incident history.
2. **First incident (45s):** Enter service, symptoms, logs, and deployment. Show the investigation plan. Do not present likely causes as established facts.
3. **Human confirmation (30s):** Enter the verified root cause, resolution, and runbook. Submit the resolution so it is retained in Hindsight.
4. **Second incident (60s):** Submit a similar 502 incident. Show the recalled prior incident and explain exactly which investigation steps changed because of it.
5. **Trust & safety (20s):** Explain that memory is historical evidence, not proof; an engineer verifies findings and approves actions. The agent never executes production changes.
6. **Close (15s):** Summarize the value: reuse verified operational knowledge rather than starting from zero.

## Evidence to capture
- Health response indicating Hindsight mode (redact secrets).
- Recalled memory visible in the UI or logs.
- Before/after investigation plans.
- Successful retain followed by recall in a fresh interaction.

Do not claim persistence or live Hindsight use unless the above was observed with `DEMO_MODE=false`.
