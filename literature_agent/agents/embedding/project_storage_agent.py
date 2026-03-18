import json
import logging

from literature_agent.agents.base_agent import BaseAgent
from literature_agent.events.event_types import EventTypes
from literature_agent.database.db import get_connection
from literature_agent.config.settings import EMBEDDING_MODEL

logger = logging.getLogger("ProjectStorageAgent")


class ProjectStorageAgent(BaseAgent):

    def handle_event(self, event):

        if event.type != EventTypes.Project.EMBEDDED:
            return

        project = event.payload["project"]
        embedding = event.payload["embedding"]

        logger.info(f"Storing project: {project['name']}")

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        INSERT OR REPLACE INTO projects
        (id, name, description, embedding, embedding_model, embedding_dim)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            project["name"],
            project["name"],
            project["description"],
            json.dumps(embedding),
            EMBEDDING_MODEL,
            len(embedding)
        ))

        conn.commit()

        logger.info(
            f"Stored project: {project['name']} | embedding_dim={len(embedding)}"
        )

        conn.close()