from database.db import get_connection


def init_db():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS papers (
        id TEXT PRIMARY KEY,
        title TEXT,
        abstract TEXT,
        embedding TEXT,
        embedding_model TEXT,
        embedding_dim INTEGER
)
    """)

    conn.commit()
    conn.close()