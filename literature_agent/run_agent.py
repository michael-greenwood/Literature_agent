from router.event_router import EventRouter
from events.event import Event
from events.event_types import EventTypes
from queues.embedding_queue import embedding_queue
from agents.embedding.embedding_agent import EmbeddingAgent


def main():

    router = EventRouter()

    router.register_queue(EventTypes.Paper.INGESTED, embedding_queue)

    embedding_agent = EmbeddingAgent(
        name="EmbeddingAgent",
        queue=embedding_queue,
        router=router
    )

    embedding_agent.start()

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