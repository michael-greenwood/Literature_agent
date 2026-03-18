import json
import logging
import numpy as np

from literature_agent.agents.base_agent import BaseAgent
from literature_agent.events.event import Event
from literature_agent.events.event_types import EventTypes
from literature_agent.database.db import get_connection

logger = logging.getLogger("SimilarityAgent")


class SimilarityAgent(BaseAgent):

    def handle_event(self, event):

        if event.type != EventTypes.Paper.STORED:
            return

        paper = event.payload["paper"]
        paper_embedding = event.payload["embedding"]

        paper_id = paper["id"]

        logger.info(f"Computing similarity for paper: {paper['title']}")

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        SELECT id, embedding
        FROM projects
        WHERE embedding IS NOT NULL
        """)

        projects = cur.fetchall()

        paper_vec = np.array(paper_embedding)

        scores = []  # ← collect scores for event

        for project_id, project_embedding_json in projects:

            project_embedding = np.array(json.loads(project_embedding_json))

            similarity = float(np.dot(paper_vec, project_embedding))

            # store in DB
            cur.execute("""
            INSERT OR REPLACE INTO paper_project_similarity
            (paper_id, project_id, similarity_score)
            VALUES (?, ?, ?)
            """, (
                paper_id,
                project_id,
                similarity
            ))

            # collect for event
            scores.append({
                "project_id": project_id,
                "score": similarity
            })

        conn.commit()
        conn.close()

        logger.info(
            f"Similarity scores stored for paper: {paper['title']} "
            f"against {len(projects)} projects"
        )

        # publish event
        new_event = Event(
            type=EventTypes.Similarity.SCORED,
            payload={
                "paper_id": paper_id,
                "scores": scores
            },
            source=self.name,
            parent_id=event.id
        )

        self.router.publish(new_event)