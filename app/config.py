import os
from dotenv import load_dotenv
load_dotenv()
def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    return default if value is None else value.strip().lower() in {"1", "true", "yes", "on"}
HINDSIGHT_BASE_URL = os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY", "").strip()
HINDSIGHT_BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "incident-response-agent").strip()
HINDSIGHT_AUTO_CREATE_BANK = env_bool("HINDSIGHT_AUTO_CREATE_BANK", False)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
DEMO_MODE = env_bool("DEMO_MODE", True)
