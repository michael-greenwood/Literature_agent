class EventTypes:

    class Literature_Source:
        INGEST = "start_ingestion"

    class Paper:
        INGESTED = "paper_ingested"
        STORED = "paper_stored"

    class Embedding:
        CREATED = "embedding_created"

    class Similarity:
        SCORED = "similarity_scored"

    class Reasoning:
        REQUESTED = "reasoning_requested"
        COMPLETED = "reasoning_completed"

    class Project:
        INGEST = "project.ingest"
        CREATED = "project.created"
        UPDATED = "project.updated"
        EMBEDDED = "project.embedded"