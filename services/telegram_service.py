import os

from fastapi import APIRouter, HTTPException, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

router = APIRouter(prefix="/telegram", tags=["telegram"])
_application: Application | None = None
_started = False


async def _get_application() -> Application:
    global _application, _started
    if _application is None:
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            raise HTTPException(status_code=500, detail="TELEGRAM_BOT_TOKEN no configurado")
        _application = Application.builder().token(token).build()
        _application.add_handler(CommandHandler("start", start))
        _application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    if not _started:
        await _application.initialize()
        await _application.start()
        _started = True
    return _application


async def shutdown_bot() -> None:
    global _started
    if _application and _started:
        await _application.stop()
        await _application.shutdown()
        _started = False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text("Bot activo. Envía tu mensaje.")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(f"Recibido: {update.message.text}")


@router.post("/webhook")
async def telegram_webhook(request: Request):
    app = await _get_application()
    payload = await request.json()
    update = Update.de_json(payload, app.bot)
    await app.process_update(update)
    return {"ok": True}