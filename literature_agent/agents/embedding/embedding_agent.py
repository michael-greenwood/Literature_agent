from agents.base_agent import BaseAgent
from events.event import Event
from events.event_types import EventTypes

class EmbeddingAgent(BaseAgent):

    def handle_event(self, event):

        if event.type != EventTypes.Paper.INGESTED:
            return

        paper = event.payload

        print(f"[EmbeddingAgent] Creating embedding for:", paper["title"])

        # TODO
        # call embedding model here

        embedding = [0.0] * 10  # placeholder

        new_event = Event(
            type=EventTypes.Embedding.CREATED,
            payload={
                "paper": paper,
                "embedding": embedding
            },
            source=self.name
        )

        self.router.publish(new_event)