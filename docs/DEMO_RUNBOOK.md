# Sentinel judge demo — 3 minutes

## Demo objective

Show one thing clearly: **the second investigation is different because Sentinel remembered a verified first investigation.**

## 0:00–0:25 — The problem

Say: "Production incidents repeat, but the useful details of the last fix often stay trapped in tickets and post-mortems. Sentinel turns confirmed incident outcomes into reusable operational memory."

## 0:25–0:55 — Cold investigation

Use `payments-api` with HTTP 502s after a deployment. Analyze with an empty memory state. Point out that the plan is generic and the hypotheses are explicitly unverified.

## 0:55–1:25 — Teach the agent

Confirm:
- Root cause: connection-pool limit was reduced by the deployment.
- Resolution: restore the approved pool limit and verify recovery.
- Runbook: compare deploy diff, pool saturation and error rate before rollback.

Retain the outcome. Explain that only the engineer-confirmed result becomes memory.

## 1:25–2:15 — The memory moment

Submit a similar `payments-api` 502 incident. Show the **Memory Intelligence** panel first. Highlight the prior confirmed incident and its relevance.

Then show the investigation plan. The first step should explicitly reference comparing the current evidence with the recalled experience.

Say: "This is the difference between remembering text and remembering operational experience."

## 2:15–2:40 — Trust boundary

Show the Evidence / Hypotheses / Memory separation. Explain that similar symptoms can have different causes and Sentinel never executes a rollback or other production action.

## 2:40–3:00 — Close

"Sentinel makes every engineer-confirmed incident useful to the next on-call engineer. Hindsight supplies the memory; the engineer remains the authority."

## Required evidence before submission

- `/api/health` reports `memory.mode=hindsight` for the live integration.
- A real retain → recall cycle succeeds with `DEMO_MODE=false`.
- Restarting the app does not erase the retained Hindsight memory.
- The second investigation visibly changes because of recalled memory.
- Synthetic incidents are labelled as synthetic; no unmeasured time-saving claim is made.
