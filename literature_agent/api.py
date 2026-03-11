from fastapi import FastAPI
from old_code.engine import LiteratureEngine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create one global engine instance
engine = LiteratureEngine()


# -------------------------
# Engine Control
# -------------------------

@app.post("/engine/start")
def start_engine():
    engine.start()
    return {"status": "started"}


@app.post("/engine/reset")
def reset_engine():
    engine.reset()
    return {"status": "reset"}


# -------------------------
# Engine State
# -------------------------

@app.get("/engine/state")
def get_state():
    return engine.get_state()


# -------------------------
# Project View
# -------------------------

@app.get("/projects/{project_name}")
def get_project(project_name: str):
    state = engine.get_state()
    project = state["projects"].get(project_name)

    if not project:
        return {"error": "Project not found"}

    return project


# -------------------------
# Paper Detail View
# -------------------------

@app.get("/papers/{paper_id}")
def get_paper(paper_id: str):
    state = engine.get_state()
    paper = state["papers"].get(paper_id)

    if not paper:
        return {"error": "Paper not found"}

    return paper
