from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from lit_agent_engine import LitAgentEngine
from database.db import get_connection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global engine instance
engine = LitAgentEngine()

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

    cur.execute("""
    SELECT id, title, abstract
    FROM papers
    WHERE id = ?
    """, (paper_id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return {"error": "Paper not found"}

    return {
        "id": row[0],
        "title": row[1],
        "abstract": row[2]
    }