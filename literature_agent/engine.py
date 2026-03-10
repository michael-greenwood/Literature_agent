import threading
import time
from datetime import datetime

from data_loader import load_abstracts, load_projects
from models import initialize_memory, update_engine_timestamp
import json
from llm_client import query_llm
from llm_parsing import safe_json_parse
from prompt_loader import load_prompt

DEBUG_LLM = False

class LiteratureEngine:

    def __init__(self):
        self.memory_lock = threading.Lock()
        self.corpus = []
        self.projects = {}
        self.memory = None

        self.ingestion_thread = None
        self.stop_flag = False

    # -------------------------
    # PUBLIC CONTROL METHODS
    # -------------------------

    def start(self):
        with self.memory_lock:
            self.projects = load_projects()
            self.corpus = load_abstracts(randomize=True)

            self.memory = initialize_memory(self.projects)
            self.memory["engine"]["status"] = "running"
            update_engine_timestamp(self.memory)

            self.stop_flag = False

        # Start background thread
        self.ingestion_thread = threading.Thread(
            target=self._ingestion_loop,
            daemon=True
        )
        self.ingestion_thread.start()

    def reset(self):
        self.stop_flag = True

        if self.ingestion_thread and self.ingestion_thread.is_alive():
            self.ingestion_thread.join()

        with self.memory_lock:
            self.memory = initialize_memory(self.projects)
            self.memory["engine"]["status"] = "idle"
            update_engine_timestamp(self.memory)

    def get_state(self):
        with self.memory_lock:
            return self.memory

    # -------------------------
    # INGESTION LOOP
    # -------------------------

    def _ingestion_loop(self):
        print(len(self.corpus))
        for paper in self.corpus:

            if self.stop_flag:
                break

            # Stage 1: Begin processing
            self._set_current_processing(paper, stage="extracting")

            # Stage 2: LLM extraction
            extraction = self._extract_with_llm(paper)
            self._update_current_processing(stage="scoring", extraction=extraction)

            # Stage 3: Score each project (multi-step)
            project_scores = {}
            for project_name, project in self.projects.items():
                if self.stop_flag:
                    break
                score_obj = self._score_project_with_llm(
                    project_name, project, paper, extraction
                )
                project_scores[project_name] = score_obj

                # Update live view incrementally as each project score arrives
                self._update_current_processing(
                    stage="scoring",
                    project_scores=project_scores
                )

            if self.stop_flag:
                break

            if DEBUG_LLM:
                print("\n========== FINAL PROJECT SCORES ==========")
                for name, score in project_scores.items():
                    print(
                        f"{name}: "
                        f"score={score.get('score')} | "
                        f"rec={score.get('recommendation')} | "
                        f"conf={score.get('confidence')}"
                    )
                print("==========================================\n")

            # Stage 4: Finalize routing
            self._finalize_paper(paper, extraction, project_scores)



        # End of corpus
        with self.memory_lock:
            self.memory["engine"]["status"] = "running"  # continuous feel
            update_engine_timestamp(self.memory)

    # -------------------------
    # INTERNAL HELPERS
    # -------------------------

    def _set_current_processing(self, paper, stage):
        with self.memory_lock:
            self.memory["current_processing"] = {
                "paper_id": paper["id"],
                "title": paper["title"],
                "stage": stage,
                "extraction": None,
                "project_scores": None
            }
            update_engine_timestamp(self.memory)

    def _update_current_processing(self, stage=None, extraction=None, project_scores=None):
        with self.memory_lock:
            if stage:
                self.memory["current_processing"]["stage"] = stage
            if extraction:
                self.memory["current_processing"]["extraction"] = extraction
            if project_scores:
                self.memory["current_processing"]["project_scores"] = project_scores
            update_engine_timestamp(self.memory)

    def _simulate_extraction(self, paper):
        text = paper["abstract"].lower()

        return {
            "materials": [w for w in ["zeolite", "mof", "aluminum"] if w in text],
            "methods": [w for w in ["3d printing", "extrusion", "electrodeposition"] if w in text],
            "limitations": [w for w in ["humidity", "mechanical", "fragility"] if w in text]
        }

    def _score_projects(self, extraction):
        scores = {}

        for project_name, project in self.projects.items():
            score = 0

            for kw in project.get("keywords", []):
                for category in extraction.values():
                    if any(kw.lower() in item for item in category):
                        score += 10

            scores[project_name] = {
                "score": min(score, 100),
                "why_relevant": "Keyword overlap detected.",
                "why_not_relevant": "Limited overlap in other categories."
            }

        return scores

    # -------------------------
    # LLM METHODS (MULTI-STEP)
    # -------------------------

    def _extract_with_llm(self, paper):
        template = load_prompt("extraction.txt")
        prompt = template.format(
            title=paper["title"],
            abstract=paper["abstract"]
        )

        raw = query_llm(prompt)

        if DEBUG_LLM:
            print("\n================ EXTRACTION RAW =================")
            print(raw)

        data = safe_json_parse(raw)

        if DEBUG_LLM:
            print("--------------- EXTRACTION PARSED ---------------")
            print(json.dumps(data, indent=2))

        # Hardening
        for k in ["materials", "methods", "findings", "limitations", "keywords"]:
            if k not in data or not isinstance(data[k], list):
                data[k] = []
        if "problem" not in data or not isinstance(data["problem"], str):
            data["problem"] = ""

        return data


    def _score_project_with_llm(self, project_name, project, paper, extraction):

        template = load_prompt("project_scoring.txt")
        prompt = template.format(
            project_name=project_name,
            project_description=project.get("description", ""),
            project_keywords=project.get("keywords", []),
            project_techniques=project.get("techniques", []),
            title=paper["title"],
            abstract=paper["abstract"],
            extraction=json.dumps(extraction, indent=2)
        )

        raw = query_llm(prompt)

        if DEBUG_LLM:
            print(f"\n=========== SCORING RAW: {project_name} ===========")
            print(raw)

        data = safe_json_parse(raw)

        # -----------------------------
        # Retry once if malformed JSON
        # -----------------------------
        if not data:
            if DEBUG_LLM:
                print(f"!!! JSON parse failed for {project_name}, attempting repair...")

            repair_prompt = f"""
            The following response was supposed to be valid JSON.
            Fix it and return ONLY valid JSON.

            Response:
            {raw}
            """.strip()

            repair_raw = query_llm(repair_prompt)

            if DEBUG_LLM:
                print(f"=========== REPAIR RAW: {project_name} ===========")
                print(repair_raw)

            data = safe_json_parse(repair_raw)

        # -----------------------------
        # Final fallback if still broken
        # -----------------------------
        if not data:
            if DEBUG_LLM:
                print(f"!!! JSON repair failed for {project_name}. Using safe fallback.")

            return {
                "score": 0,
                "recommendation": "exclude",
                "confidence": 0,
                "why_relevant": "",
                "why_not_relevant": "Invalid LLM JSON response",
                "matched_signals": [],
                "missing_signals": []
            }

        if DEBUG_LLM:
            print(f"----------- SCORING PARSED: {project_name} -----------")
            print(json.dumps(data, indent=2))

        # -----------------------------
        # Hardening
        # -----------------------------
        if "score" not in data:
            data["score"] = 0

        try:
            data["score"] = int(data["score"])
        except Exception:
            data["score"] = 0

        for k in ["matched_signals", "missing_signals"]:
            if k not in data or not isinstance(data[k], list):
                data[k] = []

        for k in ["why_relevant", "why_not_relevant"]:
            if k not in data or not isinstance(data[k], str):
                data[k] = ""

        if "recommendation" not in data or data["recommendation"] not in ["include", "watch", "exclude"]:
            data["recommendation"] = "exclude"

        if "confidence" not in data:
            data["confidence"] = 0

        try:
            data["confidence"] = int(data["confidence"])
        except Exception:
            data["confidence"] = 0

        # Clamp values
        data["score"] = max(0, min(100, data["score"]))
        data["confidence"] = max(0, min(100, data["confidence"]))

        return data

    
    def _repair_json(self, raw):

        repair_prompt = f"""
            The following response was supposed to be valid JSON.
            Fix it and return ONLY valid JSON.

            Response:
            {raw}
            """

        repair_raw = query_llm(repair_prompt)
        return safe_json_parse(repair_raw)

    def _finalize_paper(self, paper, extraction, project_scores):


        assigned_projects = [
            name for name, data in project_scores.items()
            if data.get("recommendation") == "include"
        ]
        if DEBUG_LLM:
            print(f"ROUTED PROJECTS: {assigned_projects}")

        with self.memory_lock:
            paper_id = paper["id"]

            self.memory["papers"][paper_id] = {
                "metadata": {
                    "title": paper["title"],
                    "abstract": paper.get("abstract"),
                    "authors": paper.get("authors"),
                    "year": paper.get("year"),
                    "source": paper.get("source"),
                    "doi": paper.get("doi"),
                    "arxiv_id": paper.get("arxiv_id")
                },
                "extraction": extraction,
                "project_scores": project_scores,
                "assigned_projects": assigned_projects,
                "processed_at": datetime.utcnow().isoformat()
            }


            self.memory["engine"]["total_processed"] += 1

            # Determine best project + score for event log
            best_project = None
            best_score = 0

            for name, data in project_scores.items():
                if data.get("score", 0) > best_score:
                    best_score = data.get("score", 0)
                    best_project = name

            if assigned_projects:
                self.memory["engine"]["total_routed"] += 1
                for project_name in assigned_projects:
                    project_state = self.memory["projects"][project_name]
                    project_state["paper_ids"].append(paper_id)
                    project_state["total_papers"] += 1

                event_action = "routed"
            else:
                self.memory["engine"]["total_discarded"] += 1
                self.memory["discarded"].append(paper_id)
                event_action = "discarded"

            # -------------------------
            # Append activity event
            # -------------------------
            self.memory["event_log"].insert(0, {
                "timestamp": datetime.utcnow().isoformat(),
                "paper_id": paper_id,
                "title": paper["title"],
                "action": event_action,
                "best_project": best_project,
                "best_score": best_score
            })

            # Limit feed size (keep last 50)
            self.memory["event_log"] = self.memory["event_log"][:50]

            # Clear current processing
            self.memory["current_processing"] = None

            update_engine_timestamp(self.memory)

