from literature_agent.database.db import get_connection


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

    cur.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id TEXT PRIMARY KEY,
        name TEXT,
        description TEXT,
        embedding TEXT,
        embedding_model TEXT,
        embedding_dim INTEGER
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS paper_project_similarity (
        paper_id TEXT,
        project_id TEXT,
        similarity_score REAL,
        PRIMARY KEY (paper_id, project_id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS paper_project_screening (
        paper_id TEXT,
        project_id TEXT,
        similarity_score REAL,
        decision TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (paper_id, project_id)
    )
    """)
    conn.commit()
    conn.close()