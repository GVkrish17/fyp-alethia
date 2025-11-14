from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import asyncio
from llm_router import route

from core.chat_monitor import get_recent_chat_history, message_buffer, start_monitoring, get_all_chats
from core.style_profiler import analyze_user_messages, generate_style_summary

app = FastAPI()

# CORS to allow frontend to fetch from this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LLMRequest(BaseModel):
    task: Optional[str] = "reply"  # "reply" | "relationship" | "crisis" | "all"
    username: str
    messages: List[str]
    style: Dict = {}

@app.on_event("startup")
async def startup_event():
    start_monitoring()

@app.get("/")
def home():
    return {"status": "API is running"}

@app.get("/chats")
async def list_all_chats():
    chats = await get_all_chats()
    return chats

@app.get("/chat/{username}/messages")
async def get_chat_messages(username: str, limit: int = 50):
    chat_id = await get_recent_chat_history(username, limit)
    return list(message_buffer[chat_id])

@app.get("/chat/{username}/style")
async def get_user_style(username: str):
    chat_id = await get_recent_chat_history(username, 100)
    messages = list(message_buffer[chat_id])
    style_data = analyze_user_messages(messages)
    style_summary = generate_style_summary(style_data)
    return {
        "summary": style_summary,
        "raw": style_data
    }

@app.post("/llm")
async def llm_endpoint(req: LLMRequest):
    result = await route(req.task, req.messages, req.username, req.style)
    return result
