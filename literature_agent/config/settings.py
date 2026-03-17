import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#DATABASE LOCATOIN
DATABASE_PATH = os.path.join(BASE_DIR, "database", "literature.db")

# Embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Data locations
DATA_DIR = os.path.join(BASE_DIR, "data")
PROMPT_DIR = os.path.join(BASE_DIR, "prompts")

# Event system
MAX_QUEUE_SIZE = 1000

# Ingestion settings
ARXIV_QUERY = "carbon capture"
INGESTION_INTERVAL_SECONDS = 3600


#screening thresholds
HIGH_SIMILARITY_THRESHOLD = 0.7
LOW_SIMILARITY_THRESHOLD = 0.4