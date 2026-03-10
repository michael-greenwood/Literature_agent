from config.logging_config import *
from router.event_router import EventRouter
from events.event import Event
from events.event_types import EventTypes
from queues.embedding_queue import embedding_queue
from agents.embedding.embedding_agent import EmbeddingAgent
from agents.embedding.storage_agent import StorageAgent
from queues.storage_queue import storage_queue
from database.init_db import init_db
from events.event_types import EventTypes
def main():

    init_db()
    router = EventRouter()

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
    embedding_agent.start()
    storage_agent.start()
    test_paper = {
        "title": "Test Paper",
        "abstract": "Testing embedding agent."
    }

    event = Event(
        type="paper_ingested",
        payload=test_paper
    )

    router.publish(event)

    embedding_queue.join()


if __name__ == "__main__":
    main()