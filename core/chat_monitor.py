import os
import json
import asyncio
from utils.config import TELEGRAM_API_ID, TELEGRAM_API_HASH, SESSION_NAME, MESSAGE_CONTEXT_WINDOW
from core.tone_analyser import analyze_tone
from collections import defaultdict, deque
from telethon import TelegramClient, events

# Message buffer: chat_id -> deque of messages
message_buffer = defaultdict(lambda: deque(maxlen=MESSAGE_CONTEXT_WINDOW))

# Create Telegram client
client = TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)

async def handle_message(event):
    chat_id = event.chat_id
    sender = await event.get_sender()
    msg = event.message.message

    # Add to buffer
    message_buffer[chat_id].append({
        "sender_id": sender.id,
        "text": msg,
        "from_me": event.out,  # True if sent by user
        "timestamp": event.message.date.isoformat()
    })

    # DEBUG PRINT
    if event.out:
        sender_name = "You"
    else:
        sender_name = sender.username or f"{sender.first_name or ''} {sender.last_name or ''}".strip() or "Unknown"
    print(f"[Chat {chat_id}] {sender_name}: {msg}")

    # Save raw logs (optional)
    save_log(chat_id, message_buffer[chat_id])

    # ANALYSIS PIPELINE: Here you can call your tone/relationship/suggestion modules
    # Example:
    # from core.tone_analyzer import analyze_tone
    # analyze_tone(msg)

    tone_result = analyze_tone(msg)
    print(f"[🧠 TONE] {tone_result['tone']} - VADER: {tone_result['vader']}")

async def fetch_history(chat_username, limit=100):
    entity = await client.get_entity(chat_username)
    messages = await client.get_messages(entity, limit=limit)

    history = [{
        "sender_id": m.sender_id,
        "text": m.text,
        "timestamp": m.date.isoformat()
    } for m in messages]

    print(f"[📜] Fetched {len(history)} messages from {chat_username}")
    return history

def save_log(chat_id, chat_log):
    log_path = f"data/logs/{chat_id}.json"
    with open(log_path, "w") as f:
        json.dump(list(chat_log), f, indent=2)

def start_monitoring():
    print("[✅] Starting Telegram client...")
    client.start()

    # Attach handler
    @client.on(events.NewMessage(incoming=True))
    async def incoming_handler(event):
        await handle_message(event)

    @client.on(events.NewMessage(outgoing=True))
    async def outgoing_handler(event):
        await handle_message(event)

    print("[💬] Listening to real-time messages...")
    client.run_until_disconnected()
