import logging

from agents.base_agent import BaseAgent
from events.event import Event
from events.event_types import EventTypes

logger = logging.getLogger("ReasoningAgent")


class ReasoningAgent(BaseAgent):

    def handle_event(self, event):

        if event.type != EventTypes.Reasoning.REQUESTED:
            return

        paper_id = event.payload["paper_id"]
        project_id = event.payload["project_id"]
        score = event.payload["similarity_score"]

        logger.info(
            f"[ReasoningAgent] Processing paper {paper_id} "
            f"for project {project_id} (score={score})"
        )

        # --- STUB OUTPUT ---
        reasoning_result = {
            "paper_id": paper_id,
            "project_id": project_id,
            "summary": f"Paper {paper_id} is relevant to project {project_id}",
            "confidence": score
        }

        # Optional: emit completion event
        new_event = Event(
            type=EventTypes.Reasoning.COMPLETED,
            payload=reasoning_result,
            source=self.name,
            parent_id=event.id
        )

        self.router.publish(new_event)