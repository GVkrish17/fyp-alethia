# llm_crisis.py
import re
import httpx
from typing import List, Dict

OLLAMA_URL = "http://localhost:11434/api/generate"
TINY_MODEL = "tinydolphin"  # or "tinyllama"

DANGER_PATTERNS = [
    r"\bkill myself\b", r"\bcommit suicide\b", r"\bi want to die\b",
    r"\bkill you\b", r"\bi will find you\b", r"\baddress is \d+",
]
ANGER_PATTERNS = [r"\bI hate you\b", r"\bshut up\b", r"\bf\*{0,2}ck you\b"]
STRESS_PATTERNS = [r"\boverwhelmed\b", r"\banxious\b", r"\bstressed\b"]
SADNESS_PATTERNS = [r"\bcrying\b", r"\bworthless\b", r"\bso sad\b"]

def rule_scan(text: str) -> str:
    for pat in DANGER_PATTERNS:
        if re.search(pat, text, flags=re.I):
            return "danger"
    for pat in ANGER_PATTERNS:
        if re.search(pat, text, flags=re.I):
            return "anger"
    for pat in STRESS_PATTERNS:
        if re.search(pat, text, flags=re.I):
            return "stress"
    for pat in SADNESS_PATTERNS:
        if re.search(pat, text, flags=re.I):
            return "sadness"
    return "unknown"

async def tiny_llm_judgement(text: str) -> str:
    prompt = f"""Classify the primary crisis tone in the message as one of:
- stress, anger, sadness, danger, or none.

Message: {text}
Answer with ONLY one word from: stress/anger/sadness/danger/none"""
    payload = {"model": TINY_MODEL, "prompt": prompt, "stream": False}
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(OLLAMA_URL, json=payload)
        r.raise_for_status()
        resp = r.json().get("response", "").strip().lower()
        return resp if resp in {"stress","anger","sadness","danger","none"} else "none"

async def analyze_message(messages: List[str]) -> Dict:
    text = " ".join(messages[-8:])  # small window
    label = rule_scan(text)
    if label == "unknown":
        label = await tiny_llm_judgement(text)
    return {"crisis": label}
