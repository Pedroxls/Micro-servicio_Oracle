from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

from services.task_service import get_tasks_by_email, get_tasks_by_project
from services.notification_service import list_notifications, mark_read
from services.chatbot_service import log_chat, basic_context
from services.telegram_service import router as telegram_router, shutdown_bot
from ai import chat_complete

app = FastAPI(title="TMDV Micro API", version="1.0.0")
app.include_router(telegram_router)


class ChatIn(BaseModel):
    usuario_id: int
    user_email: str | None = None
    mensaje: str


@app.on_event("shutdown")
async def on_shutdown():
    await shutdown_bot()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks/by-email")
def tasks_by_email(email: str = Query(..., min_length=3)):
    return get_tasks_by_email(email)


@app.get("/tasks/by-project/{proyecto_id}")
def tasks_by_project(proyecto_id: int):
    return get_tasks_by_project(proyecto_id)


@app.get("/notifications/{usuario_id}")
def notifications(usuario_id: int):
    return list_notifications(usuario_id)


@app.post("/notifications/{notif_id}/read")
def notification_mark_read(notif_id: int):
    updated = mark_read(notif_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return {"status": "read"}


@app.post("/chat")
def chat(payload: ChatIn):
    context = basic_context(payload.usuario_id, payload.user_email)
    messages = [
        {"role": "system", "content": context},
        {"role": "user", "content": payload.mensaje},
    ]
    respuesta = chat_complete(messages)
    log_chat(
        usuario_id=payload.usuario_id,
        user_email=payload.user_email,
        mensaje_usuario=payload.mensaje,
        respuesta_bot=respuesta,
    )
    return {"respuesta": respuesta}