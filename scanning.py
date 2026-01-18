import socket
import argparse
import sqlite3
import time
from datetime import datetime, timezone
from typing import Optional, Tuple, List

LOCALHOST = {"127.0.0.1", "localhost", "::1"}

def parse_ports(spec: str) -> List[int]:

    ports: List[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            start, end = int(a), int(b)
            if start > end:
                start, end = end, start
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))
    ports = sorted(set(p for p in ports if 1 <= p <= 65535))
    return ports


# DB_PATH_DEFAULT = "scan_results.sqlite3"

# def utc_now_iso() -> str:
#     return datetime.now(timezone.utc).isoformat()

# def init_db(conn: sqlite3.Connection) -> None:
#     conn.execute("""
#         CREATE TABLE IF NOT EXIST targets (
#                  id INTEGER PRIMARY KEY AUTOINCREMENT,
#                  host TEXT NOT NULL,
#                  port INTEGER NOT NULL,
#                  enabled INTEGER NOT NULL DEFAULT 1,
#                  UNIQUE(host, port)
#             )
#     """)
#     conn.execute("""
#         CREATE TABLE IF NOT EXISTS checks (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             target_id INTEGER NOT NULL,
#             ts_utc TEXT NOT NULL,
#             ok INTEGER NOT NULL,
#             connect_ms INTEGER,
#             error TEXT,
#             FOREIGN KEY(target_id) REFERENCES targets(id)
#         )
#     """)
#     conn.commit()