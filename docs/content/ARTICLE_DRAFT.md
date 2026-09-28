# I Built an Incident Agent That Reuses Past Fixes

Production incidents rarely arrive as clean textbook problems. An alert says a service is returning errors, logs show a partial symptom, and the on-call engineer has to reconstruct what changed while time is passing. Teams often have already solved similar incidents—but the useful details are buried in tickets, chat threads, and post-mortems.

I built an Incident Response Agent around one narrow workflow: take an incident report, retrieve relevant operational history, suggest safe investigation steps, and retain the outcome after a human confirms it. The goal is not to replace an incident commander. It is to help the next investigation start with evidence from the last one.

## The workflow

The engineer enters a service, symptom, relevant logs, and deployment context. The application asks Hindsight for related memories. Those memories are passed to the analysis layer alongside the current incident. The agent returns a concise summary, possible causes, and investigation steps.

The distinction between a hypothesis and a confirmed cause matters. The agent does not mark a suspected cause as fact, and it does not run commands or change production systems. After the engineer verifies the root cause and resolution, that outcome can be retained for future incidents.

## Why memory changes the interaction

Imagine `payments-api` begins returning HTTP 502 errors. A previous incident showed that a configuration change reduced the upstream connection-pool limit. That history does not prove the current incident has the same cause. It does, however, give the engineer a concrete comparison: inspect the deployment diff, pool utilization, and timing before trying unrelated mitigations.

Without relevant memory, the investigation begins with general diagnostics. With relevant memory, the agent can surface a specific prior incident and its verified resolution. The engineer still checks whether the current evidence matches.

## The architecture

The browser UI sends requests to a FastAPI service. The service validates the incident input, retrieves memory through the Hindsight client, and passes the current incident plus recalled context to the analysis layer. When a human confirms the outcome, the service retains it in Hindsight. An optional OpenAI-compatible model endpoint can generate the analysis; a deterministic fallback supports local development.

The key design decision is to retain confirmed outcomes rather than treating every model-generated suggestion as operational truth. This reduces the chance that an unverified hypothesis becomes institutional memory.

## What I learned

Memory is only useful when it changes a decision or saves an investigation step. A demo that merely prints retrieved text is not enough. The useful demonstration is a before-and-after comparison: show the initial plan, retain a verified resolution, then show a later incident retrieving that resolution and adjusting its investigation plan.

The second lesson is that memory needs boundaries. Similar symptoms can have different causes. Historical context should guide investigation, not trigger an automatic rollback. Human confirmation remains part of the workflow.

## Limitations and next steps

This is a prototype, not a production incident-management platform. It does not integrate with alerting systems, ticketing tools, observability backends, or approval systems. Its usefulness depends on the quality of incident records and the relevance of retrieval. Before operational adoption, it would need access controls, audit logging, tenant isolation, evaluation against a labeled incident set, and robust handling of service outages.

The next step is to measure whether recalled incidents reduce time to a useful diagnostic hypothesis without increasing incorrect assumptions. That evaluation should compare the same incident scenarios with memory disabled and enabled, and report both successful matches and misleading matches.

The core idea is simple: operational knowledge should be reusable. An incident agent becomes more useful when it can bring verified experience into the next investigation—while keeping the human engineer in control.

*Before publishing: replace this draft with your actual tested behavior, add a real code snippet, screenshots, measured before/after evidence, and links. Do not claim results you have not observed.*
