"""
Telegram Integration
====================

Simple bot implementation using python-telegram-bot to interact
with Cludocode Gemini agents.
"""

import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logger = logging.getLogger("telegram")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "your-bot-token")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Olá! Eu sou o assistente Cleudocode.\n"
        "Envie /task [descrição] para começar uma nova tarefa de codificação."
    )

async def task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Por favor, forneça uma descrição. Ex: /task Crie uma API de login")
        return
        
    task_desc = " ".join(context.args)
    await update.message.reply_text(f"🚀 Iniciando orquestração para: {task_desc}")
    
    # Integration with Orchestrator would go here

def run_telegram_bot():
    """Starts the Telegram bot poll."""
    if TELEGRAM_TOKEN == "your-bot-token":
        logger.warning("TELEGRAM_TOKEN não configurado. Ignorando bot.")
        return

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('task', task))
    
    application.run_polling()

if __name__ == "__main__":
    run_telegram_bot()
