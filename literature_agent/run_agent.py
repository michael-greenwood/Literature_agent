from config.logging_config import *
from router.event_router import EventRouter
from events.event import Event
from events.event_types import EventTypes
from queues.embedding_queue import embedding_queue
from agents.embedding.embedding_agent import EmbeddingAgent
from agents.embedding.storage_agent import StorageAgent
from queues.ingestion_queue import ingestion_queue
from queues.storage_queue import storage_queue
from database.init_db import init_db
from agents.ingestion.ingestion_agent import IngestionAgent

import time

def main():

    init_db()
    router = EventRouter()

    router.register_queue(EventTypes.Literature_Source.INGEST, ingestion_queue)
    router.register_queue(EventTypes.Paper.INGESTED, embedding_queue)
    router.register_queue(EventTypes.Embedding.CREATED, storage_queue)

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

    embedding_agent.start()
    storage_agent.start()
    ingestion_agent.start()

    time.sleep(0.1)
    router.publish(Event(EventTypes.Literature_Source.INGEST,payload={}, source="Main"))
    agents = [embedding_agent, storage_agent, ingestion_agent]

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