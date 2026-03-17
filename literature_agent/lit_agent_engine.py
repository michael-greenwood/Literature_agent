import time
from config.logging_config import *
from config.settings import DATA_DIR
import os
from router.event_router import EventRouter
from events.event import Event
from events.event_types import EventTypes

from database.init_db import init_db

# Agents
from agents.embedding.embedding_agent import EmbeddingAgent
from agents.embedding.storage_agent import StorageAgent
from agents.ingestion.ingestion_agent import IngestionAgent
from agents.debug.debug_agent import DebugAgent
from agents.ingestion.project_ingestion_agent import ProjectIngestionAgent
from agents.embedding.project_embedding_agent import ProjectEmbeddingAgent
from agents.embedding.project_storage_agent import ProjectStorageAgent
from agents.similarity.similarity_agent import SimilarityAgent
from agents.screening.screening_agent_basic import ScreeningAgentBasic
from agents.reasoning.reasoning_agent import ReasoningAgent

# Queues
from queues.embedding_queue import embedding_queue
from queues.ingestion_queue import ingestion_queue
from queues.storage_queue import storage_queue
from queues.debug_queue import debug_queue
from queues.project_ingestion_queue import project_ingestion_queue
from queues.project_embedding_queue import project_embedding_queue
from queues.project_storage_queue import project_storage_queue
from queues.similarity_queue import similarity_queue
from queues.screening_queue_basic import screening_queue_basic
from queues.reasoning_queue import reasoning_queue


class LitAgentEngine:

    def __init__(self):
        self.router = None
        self.agents = []
        self.running = False

    def start(self):

        if self.running:
            print("[Engine] Already running")
            return

        print("[Engine] Starting...")

        init_db()

        self.router = EventRouter()

        # --- Routing ---
        self.router.register_queue(EventTypes.Literature_Source.INGEST, ingestion_queue)
        self.router.register_queue(EventTypes.Paper.INGESTED, embedding_queue)
        self.router.register_queue(EventTypes.Embedding.CREATED, storage_queue)

        # Debug
        self.router.register_queue(EventTypes.Literature_Source.INGEST, debug_queue)
        self.router.register_queue(EventTypes.Paper.INGESTED, debug_queue)
        self.router.register_queue(EventTypes.Embedding.CREATED, debug_queue)
        self.router.register_queue(EventTypes.Project.INGEST, debug_queue)
        self.router.register_queue(EventTypes.Project.CREATED, debug_queue)
        self.router.register_queue(EventTypes.Project.EMBEDDED, debug_queue)
        self.router.register_queue(EventTypes.Paper.STORED, debug_queue)
        self.router.register_queue(EventTypes.Similarity.SCORED, debug_queue)
        self.router.register_queue(EventTypes.Reasoning.REQUESTED, debug_queue)
        self.router.register_queue(EventTypes.Reasoning.COMPLETED, debug_queue)

        # Project pipeline
        self.router.register_queue(EventTypes.Project.INGEST, project_ingestion_queue)
        self.router.register_queue(EventTypes.Project.CREATED, project_embedding_queue)
        self.router.register_queue(EventTypes.Project.EMBEDDED, project_storage_queue)

        # Main pipeline
        self.router.register_queue(EventTypes.Paper.STORED, similarity_queue)
        self.router.register_queue(EventTypes.Similarity.SCORED, screening_queue_basic)
        self.router.register_queue(EventTypes.Reasoning.REQUESTED, reasoning_queue)

        # --- Agents ---
        self.agents = [
            DebugAgent("DebugAgent", debug_queue, self.router),
            EmbeddingAgent("EmbeddingAgent", embedding_queue, self.router),
            StorageAgent("StorageAgent", storage_queue, self.router),
            IngestionAgent("IngestionAgent", ingestion_queue, self.router,
                           data_file=os.path.join(DATA_DIR, "abstracts.json")),
            ProjectIngestionAgent("ProjectIngestionAgent", project_ingestion_queue, self.router,
                                  data_file=os.path.join(DATA_DIR, "projects.json")),
            ProjectEmbeddingAgent("ProjectEmbeddingAgent", project_embedding_queue, self.router),
            ProjectStorageAgent("ProjectStorageAgent", project_storage_queue, self.router),
            SimilarityAgent("SimilarityAgent", similarity_queue, self.router),
            ScreeningAgentBasic("ScreeningAgentBasic", screening_queue_basic, self.router),
            ReasoningAgent("ReasoningAgent", reasoning_queue, self.router)
        ]

        # Start agents
        for agent in self.agents:
            agent.start()

        time.sleep(0.1)

        # Kick off ingestion
        self.router.publish(Event(
            type=EventTypes.Literature_Source.INGEST,
            payload={},
            source="Engine"
        ))

        self.router.publish(Event(
            type=EventTypes.Project.INGEST,
            payload={},
            source="Engine"
        ))

        self.running = True
        print("[Engine] Started")

    def stop(self):

        if not self.running:
            print("[Engine] Not running")
            return

        print("[Engine] Stopping...")

        for agent in self.agents:
            agent.stop()

        for agent in self.agents:
            agent.join(timeout=5)

        self.running = False
        print("[Engine] Stopped")

    def get_state(self):
        return {
            "running": self.running,
            "num_agents": len(self.agents)
        }