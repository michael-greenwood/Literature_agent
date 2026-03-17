import json

from agents.base_agent import BaseAgent
from events.event import Event
from events.event_types import EventTypes
from database.db import get_connection
from config.settings import EMBEDDING_MODEL


class StorageAgent(BaseAgent):

    def handle_event(self, event):

        if event.type != EventTypes.Embedding.CREATED:
            return

        paper = event.payload["paper"]
        embedding = event.payload["embedding"]

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        INSERT OR REPLACE INTO papers
        (id, title, abstract, embedding, embedding_model, embedding_dim)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            paper["id"],
            paper["title"],
            paper["abstract"],
            json.dumps(embedding),
            EMBEDDING_MODEL,
            len(embedding)
        ))

        conn.commit()
        conn.close()

        print("[StorageAgent] Stored:", paper["title"])

        # Emit event AFTER storage
        new_event = Event(
            type=EventTypes.Paper.STORED,
            payload={"paper": paper, "embedding": embedding},
            source=self.name,
            parent_id=event.id
        )

        self.router.publish(new_event)