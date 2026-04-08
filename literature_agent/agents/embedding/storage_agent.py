import json

from literature_agent.agents.base_agent import BaseAgent
from literature_agent.events.event import Event
from literature_agent.events.event_types import EventTypes
from literature_agent.database.db import get_connection
from literature_agent.config.settings import EMBEDDING_MODEL


class StorageAgent(BaseAgent):

    def handle_event(self, event):

        if event.type != EventTypes.Embedding.CREATED:
            return

        paper = event.payload["paper"]
        embedding = event.payload["embedding"]

        conn = get_connection()
        cur = conn.cursor()

        # -------------------------
        # Store core paper
        # -------------------------
        cur.execute("""
        INSERT OR REPLACE INTO papers
        (id, title, abstract, authors, year, embedding, embedding_model, embedding_dim)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            paper["id"],
            paper.get("title"),
            paper.get("abstract"),
            json.dumps(paper.get("authors", [])),
            paper.get("year"),
            json.dumps(embedding),
            EMBEDDING_MODEL,
            len(embedding)
        ))

        # -------------------------
        # Store source-specific info
        # -------------------------
        source = paper.get("source")

        if source:
            external_id = paper.get("arxiv_id") or paper.get("doi")

            cur.execute("""
            INSERT OR REPLACE INTO paper_sources
            (paper_id, source, external_id, metadata_json)
            VALUES (?, ?, ?, ?)
            """, (
                paper["id"],
                source,
                external_id,
                json.dumps({
                    "doi": paper.get("doi"),
                    "arxiv_id": paper.get("arxiv_id")
                })
            ))

        conn.commit()
        conn.close()

        print("[StorageAgent] Stored:", paper.get("title"))

        # -------------------------
        # Emit event AFTER storage
        # -------------------------
        new_event = Event(
            type=EventTypes.Paper.STORED,
            payload={"paper": paper, "embedding": embedding},
            source=self.name,
            parent_id=event.id
        )

        self.router.publish(new_event)