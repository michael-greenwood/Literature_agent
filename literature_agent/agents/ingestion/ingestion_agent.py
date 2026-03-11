import json
from agents.base_agent import BaseAgent
from events.event import Event
from events.event_types import EventTypes


class IngestionAgent(BaseAgent):

    def __init__(self, name, queue, router, data_file):
        super().__init__(name, queue, router)
        self.data_file = data_file

    def handle_event(self, event):

        if event.type != EventTypes.Literature_Source.INGEST:
            return

        try:
            print("[IngestionAgent] Loading papers from file")

            with open(self.data_file, "r") as f:
                papers = json.load(f)

            for paper in papers:

                new_event = Event(
                    type=EventTypes.Paper.INGESTED,
                    payload=paper,
                    source=self.name,
                    parent_id=event.id
                )

                self.router.publish(new_event)

            print(f"[IngestionAgent] Published {len(papers)} papers")

        except Exception as e:
            print(f"[IngestionAgent] ERROR: {e}")