from pathlib import Path

from db import fetch_all, execute

SQL_DIR = Path(__file__).resolve().parent.parent / "SQL"


def load_sql(filename: str) -> str:
    return (SQL_DIR / filename).read_text(encoding="utf-8")


def list_notifications(usuario_id: int):
    sql = load_sql("sqlnotifications.sql")
    return fetch_all(sql, {"usuario_id": usuario_id})


def mark_read(notif_id: int) -> bool:
    sql = load_sql("sqlmark_notification_read.sql")
    rows = execute(sql, {"notif_id": notif_id})
    return bool(rows)