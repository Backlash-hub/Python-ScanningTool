import socket
import argparse
import sqlite3
import time
from datetime import datetime, timezone
from typing import Optional, Tuple

DB_PATH_DEFAULT = "scan_results.sqlite3"

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def init_db(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXIST targets (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 host TEXT NOT NULL,
                 port INTEGER NOT NULL,
                 enabled INTEGER NOT NULL DEFAULT 1,
                 UNIQUE(host, port)
            )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_id INTEGER NOT NULL,
            ts_utc TEXT NOT NULL,
            ok INTEGER NOT NULL,
            connect_ms INTEGER,
            error TEXT,
            FOREIGN KEY(target_id) REFERENCES targets(id)
        )
    """)
    conn.commit()