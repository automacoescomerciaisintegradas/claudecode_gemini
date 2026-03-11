"""
WhatsApp Integration via Evolution API
=======================================

This module provides a webhook handler for Evolution API to interact
with Cludocode Gemini agents via WhatsApp.

Setup:
1. Install Evolution API (https://github.com/EvolutionAPI/evolution-api)
2. Configure a Webhook in Evolution API pointing to http://your-server:8000/integrations/whatsapp/webhook
"""

import logging
import httpx
from fastapi import APIRouter, Request, BackgroundTasks

router = APIRouter(prefix="/integrations/whatsapp")
logger = logging.getLogger("whatsapp")

EVOLUTION_API_URL = "http://localhost:8080"
EVOLUTION_API_KEY = "your-api-key"
INSTANCE_NAME = "GeminiAgent"

async def send_whatsapp_message(number: str, text: str):
    """Sends a message via Evolution API."""
    url = f"{EVOLUTION_API_URL}/message/sendText/{INSTANCE_NAME}"
    headers = {"apikey": EVOLUTION_API_KEY}
    data = {
        "number": number,
        "text": text
    }
    async with httpx.AsyncClient() as client:
        await client.post(url, json=data, headers=headers)

@router.post("/webhook")
async def whatsapp_webhook(request: Request, background_tasks: BackgroundTasks):
    """Handles incoming messages from Evolution API."""
    data = await request.json()
    
    # Extract message info
    message = data.get("data", {}).get("message", {})
    text = message.get("conversation") or message.get("extendedTextMessage", {}).get("text")
    sender = data.get("data", {}).get("key", {}).get("remoteJid")
    
    if not text or not sender:
        return {"status": "ignored"}

    logger.info(f"WhatsApp message from {sender}: {text}")

    if text.startswith("/task"):
        task_desc = text.replace("/task", "").strip()
        await send_whatsapp_message(sender, f"🤖 Entendido! Vou iniciar a tarefa: {task_desc}")
        
        # Integration with Orchestrator would go here
        # background_tasks.add_task(run_agent_task, sender, task_desc)
        
    return {"status": "ok"}
