from app.memory import MemoryService

SAMPLES = [
    """CONFIRMED INCIDENT EXPERIENCE
Incident ID: INC-DEMO-1042
Service: payments-api
Environment: production
Symptom: Elevated HTTP 502 responses after deployment
Logs/evidence: upstream connect error; p95 latency increased from 180ms to 2400ms; 502 rate 18%
Deployment/change: payments-api v2.8.1 deployed 10 minutes before alert
CONFIRMED ROOT CAUSE BY ENGINEER: Connection pool limit was reduced in the new configuration.
CONFIRMED RESOLUTION STEPS: Restored the previous pool limit and verified error rate returned to baseline.
APPROVED RUNBOOK FOR RECURRENCE: Check deploy diff, upstream connection pool saturation, and error rate before considering rollback.
OUTCOME: resolved
TRUST BOUNDARY: Historical context, not proof of a future cause.
""",
    """CONFIRMED INCIDENT EXPERIENCE
Incident ID: INC-DEMO-1088
Service: payments-api
Environment: production
Symptom: Recurring HTTP 502 responses under peak traffic
Logs/evidence: upstream connect error; connection pool at 100%; p95 latency 2100ms
Deployment/change: No deployment in the last 2 hours
CONFIRMED ROOT CAUSE BY ENGINEER: Connection pool saturation during a traffic spike.
CONFIRMED RESOLUTION STEPS: Scaled worker capacity and restored validated pool settings; monitored recovery.
APPROVED RUNBOOK FOR RECURRENCE: Compare traffic, pool utilization, and upstream saturation; avoid rollback without a deployment correlation.
OUTCOME: resolved
TRUST BOUNDARY: Historical context, not proof of a future cause.
""",
]

if __name__ == "__main__":
    memory = MemoryService()
    for sample in SAMPLES:
        memory.retain(sample, context="synthetic confirmed incident and recurrence runbook", metadata={"source": "sentinel-seed", "kind": "confirmed-incident"})
    print(f"Seeded {len(SAMPLES)} synthetic incidents into {memory.mode} memory.")
    memory.close()
