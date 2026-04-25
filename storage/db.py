import sqlite3
from pathlib import Path
from config import DB_PATH, ROOT_DIR

def get_conn():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    schema = (ROOT_DIR / "storage" / "schema.sql").read_text()
    with get_conn() as conn:
        conn.executescript(schema)
        conn.commit()
