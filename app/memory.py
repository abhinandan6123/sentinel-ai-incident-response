from app import config
class MemoryService:
    """Hindsight adapter. Local mode is a clearly labelled UI/test fallback."""
    def __init__(self):
        self.demo_memories: list[str] = []
        self.client = None
        self.mode = "demo"
        if not config.DEMO_MODE:
            if not config.HINDSIGHT_API_KEY:
                raise RuntimeError("HINDSIGHT_API_KEY is required when DEMO_MODE=false")
            from hindsight_client import Hindsight
            self.client = Hindsight(base_url=config.HINDSIGHT_BASE_URL, api_key=config.HINDSIGHT_API_KEY)
            self.mode = "hindsight"
            if config.HINDSIGHT_AUTO_CREATE_BANK:
                try:
                    self.client.create_bank(bank_id=config.HINDSIGHT_BANK_ID, name="Incident Response Agent")
                except Exception as exc:
                    print(f"Bank auto-create skipped; ensure the bank exists: {exc}")
    def recall(self, query: str) -> list[str]:
        if self.mode == "demo":
            return self.demo_memories[-5:]
        result = self.client.recall(bank_id=config.HINDSIGHT_BANK_ID, query=query)
        return [str(item.text) for item in (getattr(result, "results", None) or [])]
    def retain(self, content: str, context: str = "confirmed incident resolution") -> None:
        if self.mode == "demo":
            self.demo_memories.append(content); return
        self.client.retain(bank_id=config.HINDSIGHT_BANK_ID, content=content, context=context,
            metadata={"source":"incident-response-agent", "kind":"confirmed-incident"})
    def close(self):
        if self.client and hasattr(self.client, "close"): self.client.close()
