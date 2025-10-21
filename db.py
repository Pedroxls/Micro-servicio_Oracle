import os
from contextlib import contextmanager
from typing import Any, Dict, List

import oracledb
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
ORACLE_DSN = os.getenv("ORACLE_DSN")
ORACLE_WALLET_DIR = os.getenv("ORACLE_WALLET_DIR", "./infra/wallet")
ORACLE_WALLET_PASSWORD = os.getenv("ORACLE_WALLET_PASSWORD")
DB_POOL_MIN = int(os.getenv("DB_POOL_MIN", "1"))
DB_POOL_MAX = int(os.getenv("DB_POOL_MAX", "5"))
DB_POOL_INC = int(os.getenv("DB_POOL_INC", "1"))

_pool: oracledb.ConnectionPool | None = None


def get_pool() -> oracledb.ConnectionPool:
    global _pool
    if _pool is None:
        if not all([ORACLE_USER, ORACLE_PASSWORD, ORACLE_DSN, ORACLE_WALLET_DIR]):
            raise RuntimeError("Variables Oracle incompletas en .env")
        _pool = oracledb.create_pool(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=ORACLE_DSN,
            min=DB_POOL_MIN,
            max=DB_POOL_MAX,
            increment=DB_POOL_INC,
            config_dir=ORACLE_WALLET_DIR,
            wallet_location=ORACLE_WALLET_DIR,
            wallet_password=ORACLE_WALLET_PASSWORD,
        )
        logger.info("Pool Oracle inicializado")
    return _pool


@contextmanager
def get_connection():
    pool = get_pool()
    conn = pool.acquire()
    try:
        yield conn
    finally:
        pool.release(conn)


def fetch_all(sql: str, params: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or {})
            columns = [col[0] for col in cur.description or []]
            return [dict(zip(columns, row)) for row in cur.fetchall()]


def execute(sql: str, params: Dict[str, Any] | None = None) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or {})
            conn.commit()
            return cur.rowcount