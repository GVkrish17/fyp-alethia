# llm_router.py
from typing import List, Dict
from pii_filter import scrub_list, scrub_output
from llm_reply import generate_reply
from llm_relationship import classify_relationship
from llm_crisis import analyze_message

async def route(task: str, messages: List[str], username: str, style: Dict) -> Dict:
    # 1) scrub inputs
    clean_msgs = scrub_list(messages)

    # 2) route to module
    if task == "reply":
        out = await generate_reply(clean_msgs, username, style)
        out = scrub_output(out)
        return {"type": "reply", "result": out}

    if task == "relationship":
        out = classify_relationship(clean_msgs)
        return {"type": "relationship", "result": out}

    if task == "crisis":
        out = await analyze_message(clean_msgs)
        return {"type": "crisis", "result": out}

    # default: run all 3
    reply = await generate_reply(clean_msgs, username, style)
    relation = classify_relationship(clean_msgs)
    crisis = await analyze_message(clean_msgs)
    return {
        "type": "all",
        "result": {
            "reply": scrub_output(reply),
            "relationship": relation,
            "crisis": crisis,
        },
    }
