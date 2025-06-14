import requests
import json

OLLAMA_HOST = "http://localhost:11434"
MODEL_NAME = "mistral"  # Must match the model you've pulled

def build_prompt(message_history, user_style_hint):
    """
    Converts last N messages into a single prompt with style adaptation.
    """
    prompt = "You are the user's AI assistant trained to sound exactly like them.\n"
    prompt += "You respond with empathy, slang, emojis, and short forms — whatever the user usually uses.\n"
    prompt += "Your task: Read the following chat and suggest a single perfect next reply.\n\n"

    prompt += "=== Recent Chat Messages ===\n"
    for msg in message_history:
        sender = "You" if msg["from_me"] else "Them"
        prompt += f"{sender}: {msg['text']}\n"
    prompt += "\n"

    prompt += "=== Message Style Guide ===\n"
    prompt += f"User's texting style: {user_style_hint}\n\n"

    prompt += "=== Your Reply ===\n"
    prompt += "Reply as the user would. Keep it human, slangy, emotionally smart. No explanations.\n"

    return prompt

def generate_reply(message_history, user_style_hint):
    """
    Send the prompt to Ollama with Mistral to get a reply.
    """
    prompt = build_prompt(message_history, user_style_hint)

    response = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()
    return data.get("response", "").strip()
