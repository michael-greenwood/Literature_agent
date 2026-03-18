import logging
from literature_agent.agents.base_agent import BaseAgent
from literature_agent.events.event import Event
from literature_agent.events.event_types import EventTypes
from literature_agent.config.settings import EMBEDDING_MODEL
from sentence_transformers import SentenceTransformer

logger = logging.getLogger("ProjectEmbeddingAgent")


class ProjectEmbeddingAgent(BaseAgent):

    def __init__(self, name, queue, router):
        super().__init__(name, queue, router)
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def handle_event(self, event):

        if event.type not in (
            EventTypes.Project.CREATED,
            EventTypes.Project.UPDATED
        ):
            return

        project = event.payload

        logger.info(f"Embedding project: {project['name']}")

        text = f"""
        {project['name']}

        Description:
        {project['description']}

        Keywords:
        {" ".join(project.get("keywords", []))}

        Techniques:
        {" ".join(project.get("techniques", []))}
        """

        embedding = self.model.encode(text).tolist()

        new_event = Event(
            type=EventTypes.Project.EMBEDDED,
            payload={
                "project": project,
                "embedding": embedding
            },
            source=self.name
        )
        logger.info(new_event.payload)
        self.router.publish(new_event)