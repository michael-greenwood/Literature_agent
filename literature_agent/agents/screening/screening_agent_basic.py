import logging

from agents.base_agent import BaseAgent
from events.event import Event
from events.event_types import EventTypes
from database.db import get_connection
from config.settings import (
    HIGH_SIMILARITY_THRESHOLD,
    LOW_SIMILARITY_THRESHOLD
)

logger = logging.getLogger("ScreeningAgentBasic")


class ScreeningAgentBasic(BaseAgent):

    def handle_event(self, event):

        if event.type != EventTypes.Similarity.SCORED:
            return

        paper_id = event.payload["paper_id"]
        scores = event.payload["scores"]

        logger.info(f"Screening paper: {paper_id}")

        conn = get_connection()
        cur = conn.cursor()

        for entry in scores:

            project_id = entry["project_id"]
            score = entry["score"]

            # --- decision logic ---
            if score >= HIGH_SIMILARITY_THRESHOLD:
                decision = "pass_high"

            elif score >= LOW_SIMILARITY_THRESHOLD:
                decision = "review"

            else:
                decision = "reject"

            # --- store result ---
            cur.execute("""
            INSERT OR REPLACE INTO paper_project_screening
            (paper_id, project_id, similarity_score, decision)
            VALUES (?, ?, ?, ?)
            """, (
                paper_id,
                project_id,
                score,
                decision
            ))

            # --- trigger reasoning ONLY for high ---
            if decision == "pass_high":

                logger.info(
                    f"Paper {paper_id} passed HIGH threshold for project {project_id} "
                    f"(score={score})"
                )

                new_event = Event(
                    type=EventTypes.Reasoning.REQUESTED,
                    payload={
                        "paper_id": paper_id,
                        "project_id": project_id,
                        "similarity_score": score
                    },
                    source=self.name,
                    parent_id=event.id
                )

                self.router.publish(new_event)

        conn.commit()
        conn.close()

        logger.info(f"Screening complete for paper: {paper_id}")