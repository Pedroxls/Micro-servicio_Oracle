from pathlib import Path

from db import execute
from .task_service import get_tasks_by_email
from .notification_service import list_notifications

SQL_DIR = Path(__file__).resolve().parent.parent / "SQL"


def load_sql(filename: str) -> str:
    return (SQL_DIR / filename).read_text(encoding="utf-8")


def log_chat(
    usuario_id: int,
    user_email: str | None,
    mensaje_usuario: str,
    respuesta_bot: str,
) -> None:
    sql = load_sql("sqlchatbot_insert.sql")
    execute(
        sql,
        {
            "usuario_id": usuario_id,
            "user_email": user_email,
            "msg_user": mensaje_usuario,
            "msg_bot": respuesta_bot,
        },
    )


def basic_context(usuario_id: int, user_email: str | None) -> str:
    tasks = get_tasks_by_email(user_email) if user_email else []
    notifs = list_notifications(usuario_id)

    tareas_pendientes = [
        f"- {t.get('TITULO', 'Sin título')} (estado: {t.get('ESTADO')})"
        for t in tasks
        if (t.get("ESTADO") or "").lower() != "done"
    ]
    notificaciones_no_leidas = [
        f"- {n.get('TITULO', 'Notificación')} ({n.get('FECHA')})"
        for n in notifs
        if (n.get("LEIDA") or "N") != "Y"
    ]

    contexto = ["Eres un asistente que ayuda con tareas y notificaciones."]
    if tareas_pendientes:
        contexto.append("Tareas pendientes:")
        contexto.extend(tareas_pendientes)
    if notificaciones_no_leidas:
        contexto.append("Notificaciones sin leer:")
        contexto.extend(notificaciones_no_leidas)
    if not tareas_pendientes and not notificaciones_no_leidas:
        contexto.append("No hay tareas pendientes ni notificaciones sin leer.")

    return "\n".join(contexto)