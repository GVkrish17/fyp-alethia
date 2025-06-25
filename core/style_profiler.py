import re
import emoji
from collections import Counter
import json


def extract_emojis(text):
    return [e for e in text if e in emoji.EMOJI_DATA]

def extract_abbreviations(text):
    return re.findall(r"\b[a-z]{2,4}\b", text)

def is_abbreviation(word):
    return word.islower() and len(word) <= 4 and not word in {"this", "that", "when", "what", "your"}

def analyze_user_messages(messages):
    emoji_counter = Counter()
    word_counter = Counter()
    message_lengths = []
    abbreviation_counter = Counter()

    for msg in messages:
        if not msg["from_me"]: continue  # only user messages

        text = msg["text"]
        if not text: continue

        emojis = extract_emojis(text)
        emoji_counter.update(emojis)

        words = re.findall(r"\b\w+\b", text.lower())
        word_counter.update(words)

        abbrs = [w for w in words if is_abbreviation(w)]
        abbreviation_counter.update(abbrs)

        message_lengths.append(len(text))

    return {
        "avg_msg_len": sum(message_lengths) / len(message_lengths) if message_lengths else 0,
        "top_emojis": emoji_counter.most_common(5),
        "top_words": word_counter.most_common(10),
        "common_abbreviations": abbreviation_counter.most_common(5),
        "is_lowercase_heavy": all(msg["text"].islower() for msg in messages if msg["from_me"] and msg["text"]),
    }

def generate_style_summary(style_data):
    summary = []

    if style_data["avg_msg_len"] < 25:
        summary.append("replies are short")
    else:
        summary.append("writes longer messages")

    if style_data["is_lowercase_heavy"]:
        summary.append("prefers all lowercase")

    if style_data["top_emojis"]:
        emojis = ''.join([e[0] for e in style_data["top_emojis"]])
        summary.append(f"uses emojis like {emojis}")

    if style_data["common_abbreviations"]:
        abbrs = [abbr[0] for abbr in style_data["common_abbreviations"]]
        summary.append(f"commonly uses short forms like: {', '.join(abbrs)}")

    return "User " + ", ".join(summary) + "."

def save_profile(style_data, summary, out_path="data/user_style.json"):
    data = {
        "summary": summary,
        "raw_analysis": style_data
    }
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)

# Main function that wraps up this whole file. To be used in other functions to generate user_style.
async def user_style(target_chat, MESSAGE_CONTEXT_WINDOW):
    from core.chat_monitor import get_recent_chat_history, message_buffer
    chat_id = await get_recent_chat_history(target_chat, MESSAGE_CONTEXT_WINDOW)
    messages = list(message_buffer[chat_id])
    messages_from_me = []
    for msg in messages:
        if msg["from_me"]:
            messages_from_me.append(msg)

    for i in messages_from_me:
        print(i)

    style_data = analyze_user_messages(messages)
    style_summary = generate_style_summary(style_data)
    save_profile(style_data, style_summary)
    return style_summary
