from literature_agent.database.db import get_connection


def init_db():

    conn = get_connection()
    cur = conn.cursor()

    # -----------------------------
    # Projects
    # -----------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        base_description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS project_versions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        title TEXT,
        base_description TEXT,
        structure_json TEXT,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
    """)

    # -----------------------------
    # Papers
    # -----------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS papers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        abstract TEXT,
        doi TEXT,
        journal TEXT,
        year INTEGER,
        source TEXT,
        metadata_json TEXT,
        processed BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -----------------------------
    # Authors
    # -----------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS authors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS paper_authors (
        paper_id INTEGER NOT NULL,
        author_id INTEGER NOT NULL,
        author_order INTEGER,

        PRIMARY KEY (paper_id, author_id),

        FOREIGN KEY (paper_id) REFERENCES papers(id),
        FOREIGN KEY (author_id) REFERENCES authors(id)
    )
    """)

    # -----------------------------
    # Embeddings
    # -----------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS embeddings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity_type TEXT NOT NULL,
        entity_id INTEGER NOT NULL,
        vector BLOB NOT NULL,
        model TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -----------------------------
    # Query Units
    # -----------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS query_units (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_version_id INTEGER NOT NULL,

        type TEXT,
        origin TEXT,

        text TEXT NOT NULL,
        embedding_id INTEGER,

        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (project_version_id) REFERENCES project_versions(id),
        FOREIGN KEY (embedding_id) REFERENCES embeddings(id)
    )
    """)

    # -----------------------------
    # Similarity Results
    # -----------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS similarity_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        paper_id INTEGER NOT NULL,
        query_unit_id INTEGER NOT NULL,

        score REAL,
        threshold REAL,
        passed BOOLEAN,

        query_version INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (paper_id) REFERENCES papers(id),
        FOREIGN KEY (query_unit_id) REFERENCES query_units(id)
    )
    """)

    # -----------------------------
    # Reasoning Results
    # -----------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reasoning_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        paper_id INTEGER NOT NULL,
        query_unit_id INTEGER NOT NULL,

        relevance_label TEXT,
        explanation TEXT,
        extracted_data TEXT,
        confidence REAL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (paper_id) REFERENCES papers(id),
        FOREIGN KEY (query_unit_id) REFERENCES query_units(id)
    )
    """)

    # -----------------------------
    # Indexes
    # -----------------------------
    cur.execute("CREATE INDEX IF NOT EXISTS idx_papers_created ON papers(created_at)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_query_units_project_version ON query_units(project_version_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_query_units_active ON query_units(is_active)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_similarity_paper ON similarity_results(paper_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_similarity_query ON similarity_results(query_unit_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_similarity_passed ON similarity_results(passed)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_reasoning_lookup ON reasoning_results(paper_id, query_unit_id)")

    # Optional uniqueness constraint
    cur.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS unique_similarity
    ON similarity_results(paper_id, query_unit_id, query_version)
    """)

    conn.commit()
    conn.close()