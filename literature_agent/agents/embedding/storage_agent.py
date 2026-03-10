import json
from agents.base_agent import BaseAgent
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
        (id, title, abstract, embedding, embedding_model)
        VALUES (?, ?, ?, ?, ?)
        """, (
            paper.get("id", paper["title"]),
            paper["title"],
            paper["abstract"],
            json.dumps(embedding),
            EMBEDDING_MODEL
        ))

        conn.commit()
        conn.close()

        print("[StorageAgent] Stored:", paper["title"])