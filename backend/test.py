import asyncio
from llm_reply import generate_reply
msgs = ["yo, can we meet later?", "i'm kinda stressed today ngl"]
style = {"raw_analysis": {"is_lowercase_heavy": True, "avg_msg_len": 12}}
print(asyncio.run(generate_reply(msgs, "alex", style)))
