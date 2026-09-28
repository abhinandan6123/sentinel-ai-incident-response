from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from app import config


@dataclass
class MemoryItem:
    text: str
    memory_id: str = ""
    service: str = ""
    title: str = "Prior confirmed incident"
    source: str = "hindsight"
    confirmed: bool = True


class MemoryService:
    """Hindsight adapter with an explicitly labelled local fallback for demos/tests."""

    def __init__(self):
        self.demo_memories: list[MemoryItem] = []
        self.client = None
        self.mode = "demo"
        self.provider = "local"

        if not config.DEMO_MODE:
            if not config.HINDSIGHT_API_KEY:
                raise RuntimeError("HINDSIGHT_API_KEY is required when DEMO_MODE=false")
            from hindsight_client import Hindsight

            self.client = Hindsight(
                base_url=config.HINDSIGHT_BASE_URL,
                api_key=config.HINDSIGHT_API_KEY,
            )
            self.mode = "hindsight"
            self.provider = "Vectorize Hindsight"
            if config.HINDSIGHT_AUTO_CREATE_BANK:
                try:
                    self.client.create_bank(
                        bank_id=config.HINDSIGHT_BANK_ID,
                        name="Sentinel Incident Memory",
                    )
                except Exception as exc:
                    # Existing banks are expected to raise on duplicate creation.
                    print(f"Hindsight bank auto-create skipped: {exc}")

    @staticmethod
    def _extract_text(item: Any) -> str:
        if isinstance(item, str):
            return item
        if isinstance(item, dict):
            return str(item.get("text") or item.get("content") or item.get("memory") or item)
        return str(getattr(item, "text", None) or getattr(item, "content", None) or item)

    @staticmethod
    def _extract_id(item: Any) -> str:
        if isinstance(item, dict):
            return str(item.get("id") or item.get("memory_id") or "")
        return str(getattr(item, "id", None) or getattr(item, "memory_id", None) or "")

    def recall(self, query: str, limit: int = 5) -> list[MemoryItem]:
        if self.mode == "demo":
            # Demo memory is intentionally small and deterministic.
            return self.demo_memories[-limit:][::-1]

        try:
            result = self.client.recall(
                bank_id=config.HINDSIGHT_BANK_ID,
                query=query,
                limit=limit,
            )
        except TypeError:
            # Keep compatibility with older hindsight-client releases.
            result = self.client.recall(
                bank_id=config.HINDSIGHT_BANK_ID,
                query=query,
            )
        raw = getattr(result, "results", None) or []
        return [
            MemoryItem(
                text=self._extract_text(item),
                memory_id=self._extract_id(item),
            )
            for item in raw[:limit]
        ]

    def retain(self, content: str, context: str = "confirmed incident resolution", metadata: dict | None = None) -> str:
        if self.mode == "demo":
            memory_id = f"demo-{len(self.demo_memories) + 1:03d}"
            self.demo_memories.append(MemoryItem(text=content, memory_id=memory_id, source="local-demo"))
            return memory_id

        result = self.client.retain(
            bank_id=config.HINDSIGHT_BANK_ID,
            content=content,
            context=context,
            metadata=metadata or {},
        )
        return self._extract_id(result) or "retained"

    def status(self) -> dict:
        return {
            "mode": self.mode,
            "provider": self.provider,
            "bank_id": config.HINDSIGHT_BANK_ID,
            "configured": self.mode == "hindsight" or bool(self.demo_memories) or config.DEMO_MODE,
            "demo_warning": (
                "Local process memory. Restarting the server clears this memory."
                if self.mode == "demo"
                else None
            ),
        }

    def close(self):
        if self.client and hasattr(self.client, "close"):
            self.client.close()


def memory_to_text(item: MemoryItem) -> str:
    return item.text


def extract_service(text: str) -> str:
    match = re.search(r"Service:\s*([^\n.]+)", text, re.IGNORECASE)
    return match.group(1).strip() if match else ""
