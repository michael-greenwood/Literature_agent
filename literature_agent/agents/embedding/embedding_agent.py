from agents.base_agent import BaseAgent
from events.event import Event


class EmbeddingAgent(BaseAgent):

    def handle_event(self, event):

        if event.type != "paper_ingested":
            return

        paper = event.payload

        print(f"[EmbeddingAgent] Creating embedding for:", paper["title"])

        # TODO
        # call embedding model here

        embedding = [0.0] * 10  # placeholder

        new_event = Event(
            type="embedding_created",
            payload={
                "paper": paper,
                "embedding": embedding
            },
            source=self.name
        )

        self.router.publish(new_event)