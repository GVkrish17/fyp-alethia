# pii_filter.py
import re
from typing import List

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{4}\b")
ADDRESS = re.compile(r"\b\d{1,5}\s+\w+(?:\s\w+){0,3}\s(?:street|st|road|rd|ave|avenue|blvd|lane|ln)\b", re.I)
NAME_HINT = re.compile(r"\b([A-Z][a-z]{2,})\b")  # crude; tune later

REDACT = "[redacted]"

def scrub(text: str) -> str:
    text = EMAIL.sub(REDACT, text)
    text = PHONE.sub(REDACT, text)
    text = ADDRESS.sub(REDACT, text)
    # Be careful with names—optional, can over-redact:
    return text

def scrub_list(msgs: List[str]) -> List[str]:
    return [scrub(m) for m in msgs]

def scrub_output(text: str) -> str:
    # ensure the model didn't invent PII (rare but safe to check)
    return scrub(text)
