# How Hindsight is used

The agent uses Hindsight as its operational memory store. During incident analysis, the application submits a query derived from the service, symptoms, logs, and deployment context. Recalled memories are passed to the analysis step as historical context. After an engineer confirms an incident's root cause, resolution, and runbook, the application retains that confirmed outcome for future retrieval.

## Why it matters
A later incident can retrieve a prior, similar incident and use its verified resolution as a starting point. This makes memory part of the workflow rather than a decorative chat transcript.

## Trust boundaries
- Recalled information is historical context, not proof that the current incident has the same cause.
- The engineer supplies/approves the confirmed root cause and resolution.
- The agent recommends diagnostic steps; it does not execute commands or modify infrastructure.
- Demo mode uses local process memory and is not evidence of Hindsight integration.

## Demo proof
Show Hindsight mode in health/status, retain a confirmed incident, then recall it during a separate incident request. Capture the changed plan and identify which recalled memory informed it.
