from agents.base_agent import BaseAgent
from events.event import Event
from events.event_types import EventTypes
from config.settings import EMBEDDING_MODEL
import logging
logger = logging.getLogger("EmbeddingAgent")
from sentence_transformers import SentenceTransformer


class EmbeddingAgent(BaseAgent):

    def __init__(self, name, queue, router):
        super().__init__(name, queue, router)

        print("[EmbeddingAgent] Loading model:", EMBEDDING_MODEL)
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def handle_event(self, event):

        if event.type != EventTypes.Paper.INGESTED:
            return

        paper = event.payload

        print(f"[EmbeddingAgent] Creating embedding for:", paper["title"])
        logger.info(f"Creating embedding for: {paper['title']}")
        text = paper["title"] + " " + paper["abstract"]

        embedding = self.model.encode(text).tolist()

        new_event = Event(
            type=EventTypes.Embedding.CREATED,
            payload={
                "paper": paper,
                "embedding": embedding
            },
            source=self.name
        )
        print("Embedding size:", len(embedding))

        self.router.publish(new_event)