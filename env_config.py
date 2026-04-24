import os
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent
ENV_PATH = BACKEND_DIR / ".env"
PLACEHOLDER_VALUES = {
    "your_api_key_here",
    "your_gemini_api_key_here",
    "your_google_api_key_here",
    "replace_me",
}


def load_backend_env(override: bool = False) -> Path:
    if ENV_PATH.exists():
        load_dotenv(dotenv_path=ENV_PATH, override=override)
    return ENV_PATH


def get_clean_env(name: str, default=None):
    value = os.getenv(name)
    if value is None:
        return default

    value = value.strip()
    return value if value else default


def get_gemini_api_key():
    for env_name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        value = get_clean_env(env_name)
        if value and value.lower() not in PLACEHOLDER_VALUES:
            return value
    return None
