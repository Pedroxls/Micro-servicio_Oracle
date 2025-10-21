import os
from typing import List, Dict

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

_client: OpenAI | None = None


def client() -> OpenAI:
    global _client
    if _client is None:
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY no configurado en .env")
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def chat_complete(messages: List[Dict[str, str]]) -> str:
    response = client().responses.create(
        model=OPENAI_MODEL,
        input=messages,
    )
    return response.output_text