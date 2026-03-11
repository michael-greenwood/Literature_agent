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
    debug_agent = DebugAgent(
        name="DebugAgent",
        queue=debug_queue,
        router=router
    )
    # Start agents
    debug_agent.start()
    embedding_agent.start()
    storage_agent.start()
    time.sleep(0.1)  # Ensure debug agent is ready to receive logs
    ingestion_agent.start()

    agents = [
        embedding_agent,
        storage_agent,
        ingestion_agent,
        debug_agent
    ]

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