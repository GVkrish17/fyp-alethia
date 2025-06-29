import os
import json
import asyncio
from utils.config import TELEGRAM_API_ID, TELEGRAM_API_HASH, SESSION_NAME, MESSAGE_CONTEXT_WINDOW
from core.tone_analyser import analyze_tone
from core.suggestion_generator import generate_reply
from collections import defaultdict, deque
from telethon import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from core.style_profiler import user_style

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
    save_log(sender_name, message_buffer[chat_id])

    # ANALYSIS PIPELINE: Here you can call your tone/relationship/suggestion modules
    # Example:
    # from core.tone_analyzer import analyze_tone
    # analyze_tone(msg)

    tone_result = analyze_tone(msg)
    print(f"[🧠 TONE] {tone_result['tone']} - VADER: {tone_result['vader']}")

    if chat_id and len(message_buffer[chat_id]) > 0:
        chat_context = list(message_buffer[chat_id])[-100:]

        #Simulated user texting style (we'll learn this later)
        user_style_hint = await user_style(chat_id,MESSAGE_CONTEXT_WINDOW)
        print("USER STYLE: ", user_style_hint)

        reply = generate_reply(chat_context, user_style_hint)
        print(f"\n💡 Suggested Reply: {reply}\n")

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

async def fetch_recent_messages(chat_username_or_id, limit):
    """
    Fetches last `limit` messages from a specific chat and stores in message_buffer
    """
    entity = await client.get_entity(chat_username_or_id)
    messages = await client.get_messages(entity, limit=limit)

    chat_id = entity.id

    for m in reversed(messages):  # maintain oldest → newest order
        message_buffer[chat_id].append({
            "sender_id": m.sender_id,
            "text": m.text,
            "from_me": m.out,
            "timestamp": m.date.isoformat()
        })

    print(f"[📥] Fetched {len(messages)} historical messages from: {chat_username_or_id} (chat_id: {chat_id})")
    return chat_id

async def get_recent_chat_history(chat_username_or_id, limit):
    """
    Starts client, fetches past messages from target chat, returns chat_id and messages
    """
    return await fetch_recent_messages(chat_username_or_id, limit=limit)
