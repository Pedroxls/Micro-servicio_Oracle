from pathlib import Path

from db import fetch_all

SQL_DIR = Path(__file__).resolve().parent.parent / "SQL"


def load_sql(filename: str) -> str:
    return (SQL_DIR / filename).read_text(encoding="utf-8")


def get_tasks_by_email(email: str):
    sql = load_sql("sqltasks_by_email.sql")
    return fetch_all(sql, {"email": email})


def get_tasks_by_project(proyecto_id: int):
    sql = load_sql("sqltasks_by_project.sql")
    return fetch_all(sql, {"proyecto_id": proyecto_id})