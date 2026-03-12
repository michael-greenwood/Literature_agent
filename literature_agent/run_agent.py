from config.logging_config import *
from router.event_router import EventRouter
from events.event import Event
from events.event_types import EventTypes

from queues.embedding_queue import embedding_queue
from queues.ingestion_queue import ingestion_queue
from queues.storage_queue import storage_queue

from agents.embedding.embedding_agent import EmbeddingAgent
from agents.embedding.storage_agent import StorageAgent
from agents.ingestion.ingestion_agent import IngestionAgent
from queues.debug_queue import debug_queue
from agents.debug.debug_agent import DebugAgent
from database.init_db import init_db
from queues.project_ingestion_queue import project_ingestion_queue
from queues.project_embedding_queue import project_embedding_queue
from queues.project_storage_queue import project_storage_queue

from agents.ingestion.project_ingestion_agent import ProjectIngestionAgent
from agents.embedding.project_embedding_agent import ProjectEmbeddingAgent
from agents.embedding.project_storage_agent import ProjectStorageAgent
import time


def main():

    init_db()

    router = EventRouter()

    # Register routing
    router.register_queue(EventTypes.Literature_Source.INGEST, ingestion_queue)
    router.register_queue(EventTypes.Paper.INGESTED, embedding_queue)
    router.register_queue(EventTypes.Embedding.CREATED, storage_queue)
    router.register_queue(EventTypes.Literature_Source.INGEST, debug_queue)
    router.register_queue(EventTypes.Paper.INGESTED, debug_queue)
    router.register_queue(EventTypes.Embedding.CREATED, debug_queue)
    router.register_queue(EventTypes.Project.INGEST, project_ingestion_queue)
    router.register_queue(EventTypes.Project.CREATED, project_embedding_queue)
    router.register_queue(EventTypes.Project.EMBEDDED, project_storage_queue)
    # Create agents
    embedding_agent = EmbeddingAgent(
        name="EmbeddingAgent",
        queue=embedding_queue,
        router=router
    )

    storage_agent = StorageAgent(
        name="StorageAgent",
        queue=storage_queue,
        router=router
    )

    ingestion_agent = IngestionAgent(
        name="IngestionAgent",
        queue=ingestion_queue,
        router=router,
        data_file="literature_agent/data/abstracts.json"
    )
    project_ingestion_agent = ProjectIngestionAgent(
        name="ProjectIngestionAgent",
        queue=project_ingestion_queue,
        router=router,
        data_file="literature_agent/data/projects.json"
    )

    project_embedding_agent = ProjectEmbeddingAgent(
        name="ProjectEmbeddingAgent",
        queue=project_embedding_queue,
        router=router
    )

    project_storage_agent = ProjectStorageAgent(
        name="ProjectStorageAgent",
        queue=project_storage_queue,
        router=router
    )
    debug_agent = DebugAgent(
        name="DebugAgent",
        queue=debug_queue,
        router=router
    )
    # Start agents
    agents = [
        debug_agent,
        embedding_agent,
        storage_agent,
        ingestion_agent,
        project_ingestion_agent,
        project_embedding_agent,
        project_storage_agent
    ]
    for agent in agents:
        agent.start()
    time.sleep(0.1)  # Give threads time to start
    

    # Give threads time to spin up
    time.sleep(0.1)

    # Kick off pipeline
    router.publish(
        Event(
            type=EventTypes.Literature_Source.INGEST,
            payload={},
            source="Main"
        )
    )
    router.publish(
        Event(
            type=EventTypes.Project.INGEST,
            payload={},
            source="Main"
        )
    )
    # Keep service alive
    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping agents...")

        for agent in agents:
            agent.stop()

        for agent in agents:
            agent.join(timeout=5)

        print("Shutdown complete")


if __name__ == "__main__":
    main()