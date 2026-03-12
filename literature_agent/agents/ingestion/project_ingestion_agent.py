import json
import logging

from agents.base_agent import BaseAgent
from events.event import Event
from events.event_types import EventTypes

logger = logging.getLogger("ProjectIngestionAgent")


class ProjectIngestionAgent(BaseAgent):

    def __init__(self, name, queue, router, data_file):
        super().__init__(name, queue, router)
        self.data_file = data_file

    def handle_event(self, event):

        if event.type != EventTypes.Project.INGEST:
            return

        with open(self.data_file) as f:
            projects = json.load(f)

        logger.info(f"Loaded {len(projects)} projects from {self.data_file}")

        for project in projects:

            logger.info(f"Ingesting project: {project['name']}")

            new_event = Event(
                type=EventTypes.Project.CREATED,
                payload=project,
                source=self.name
            )

            self.router.publish(new_event)