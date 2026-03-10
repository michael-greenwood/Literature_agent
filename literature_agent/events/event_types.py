class EventTypes:

    class Paper:
        INGESTED = "paper_ingested"

    class Embedding:
        CREATED = "embedding_created"

    class Similarity:
        SCORED = "similarity_scored"

    class Reasoning:
        REQUESTED = "reasoning_requested"
        COMPLETED = "reasoning_completed"