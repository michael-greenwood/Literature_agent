# Embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Data locations
DATA_DIR = "literature_agent/data"
PROMPT_DIR = "literature_agent/prompts"

# Event system
MAX_QUEUE_SIZE = 1000

# Ingestion settings
ARXIV_QUERY = "carbon capture"
INGESTION_INTERVAL_SECONDS = 3600

# Future database location
DATABASE_PATH = "literature_agent/database/literature.db"

#screening thresholds
HIGH_SIMILARITY_THRESHOLD = 0.7
LOW_SIMILARITY_THRESHOLD = 0.4