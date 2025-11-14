# llm_reply.py
import httpx
from typing import List, Dict

OLLAMA_URL = "http://localhost:11434/api/generate"  # default ollama endpoint
MODEL_NAME = "mistral"

REPLY_SYSTEM_PROMPT = """You are an empathetic texting assistant grounded in MI, NVC, and CBT.
- Keep replies short (1–3 sentences).
- Avoid therapy jargon.
- Mirror user's style (e.g., lowercase if they prefer).
- Offer validation before suggestions.
- Never include private data you weren't given.
Format: plain text reply only."""

def build_user_style_hint(style: Dict) -> str:
    # style like user_style.json
    # e.g., {"summary": "...", "raw_analysis": {"is_lowercase_heavy": true, ...}}
    hint = []
    if style:
        if style.get("raw_analysis", {}).get("is_lowercase_heavy"):
            hint.append("User prefers all lowercase.")
        avg_len = style.get("raw_analysis", {}).get("avg_msg_len", 0)
        if avg_len and avg_len < 25:
            hint.append("User writes very short messages.")
    return " ".join(hint) if hint else "No special style noted."

def build_prompt(messages: List[str], username: str, style: Dict) -> str:
    last_msgs = "\n".join([f"- {m}" for m in messages[-12:]])  # 6–12 window
    style_hint = build_user_style_hint(style)
    return f"""{REPLY_SYSTEM_PROMPT}

USER STYLE HINTS: {style_hint}

CONTEXT (last messages with {username}):
{last_msgs}

Write a single suggested reply:"""

async def generate_reply(messages: List[str], username: str, style: Dict) -> str:
    prompt = build_prompt(messages, username, style)
    payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(OLLAMA_URL, json=payload)
        r.raise_for_status()
        data = r.json()
        text = data.get("response", "").strip()
        return text
