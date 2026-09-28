from app.memory import MemoryService
SAMPLE=("Synthetic incident INC-DEMO-001. Service: Checkout API. Environment: staging. Symptom: intermittent 502 Bad Gateway errors after deployment. Confirmed root cause: upstream request timeout was configured below the dependency's normal response time. Confirmed resolution: restore approved timeout configuration, verify upstream health, and run checkout smoke test. Outcome: resolved. Synthetic demo data, not a real production incident.")
if __name__=="__main__":
    memory=MemoryService(); memory.retain(SAMPLE,context="synthetic incident runbook example"); print(f"Seeded one incident into {memory.mode} memory."); memory.close()
