from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from literature_agent.engine import LitAgentEngine
from literature_agent.database.db import get_connection
from literature_agent.engine import get_engine
import json
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# engine instance

engine = get_engine()

# -------------------------
# Engine Control
# -------------------------

@app.post("/engine/start")
def start_engine():
    engine.start()
    return {"status": "started"}


@app.post("/engine/stop")
def stop_engine():
    engine.stop()
    return {"status": "stopped"}


@app.get("/engine/state")
def get_engine_state():
    return engine.get_state()


# -------------------------
# Project Data
# -------------------------
@app.get("/projects/{project_id}")
def get_project(project_id: str):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT id, name, description
    FROM projects
    WHERE id = ?
    """, (project_id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return {"error": "Project not found"}

    return {
        "id": row[0],
        "name": row[1],
        "description": row[2]
    }

@app.get("/projects")
def get_projects():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT id, name, description
    FROM projects
    """)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "name": r[1],
            "description": r[2]
        }
        for r in rows
    ]

@app.get("/papers")
def get_papers(limit: int = 10):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT id, title, year
    FROM papers
    ORDER BY rowid DESC
    LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "title": r[1],
            "year": r[2]
        }
        for r in rows
    ]

@app.get("/projects/{project_id}/screened")
def get_project_screened(project_id: str):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT
        p.id,
        p.title,
        s.similarity_score,
        s.decision
    FROM paper_project_screening s
    JOIN papers p ON s.paper_id = p.id
    WHERE s.project_id = ?
    ORDER BY s.similarity_score DESC
    LIMIT 100
    """, (project_id,))

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "paper_id": r[0],
            "title": r[1],
            "score": r[2],
            "decision": r[3]
        }
        for r in rows
    ]


# -------------------------
# Accepted Papers
# -------------------------

@app.get("/projects/{project_id}/accepted")
def get_project_accepted(project_id: str):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT
        p.id,
        p.title,
        s.similarity_score
    FROM paper_project_screening s
    JOIN papers p ON s.paper_id = p.id
    WHERE s.project_id = ?
    AND s.decision = 'pass_high'
    ORDER BY s.similarity_score DESC
    """, (project_id,))

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "paper_id": r[0],
            "title": r[1],
            "score": r[2]
        }
        for r in rows
    ]


# -------------------------
# Paper Detail
# -------------------------

@app.get("/papers/{paper_id}")
def get_paper(paper_id: str):

    conn = get_connection()
    cur = conn.cursor()

    # -------------------------
    # Core paper
    # -------------------------
    cur.execute("""
    SELECT id, title, abstract, authors, year
    FROM papers
    WHERE id = ?
    """, (paper_id,))

    row = cur.fetchone()

    if not row:
        conn.close()
        return {"error": "Paper not found"}

    paper = {
        "id": row[0],
        "title": row[1],
        "abstract": row[2],
        "authors": json.loads(row[3]) if row[3] else [],
        "year": row[4]
    }

    # -------------------------
    # Sources
    # -------------------------
    cur.execute("""
    SELECT source, external_id, metadata_json
    FROM paper_sources
    WHERE paper_id = ?
    """, (paper_id,))

    sources = []
    for s in cur.fetchall():
        sources.append({
            "source": s[0],
            "external_id": s[1],
            "metadata": json.loads(s[2]) if s[2] else {}
        })

    conn.close()

    paper["sources"] = sources

    return paper