import logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Base logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/literature_agent.log"),
        logging.StreamHandler()
    ]
)

# Event trace logger
event_logger = logging.getLogger("EventTrace")
event_logger.setLevel(logging.INFO)

event_handler = logging.FileHandler(f"{LOG_DIR}/event_trace.log")

event_formatter = logging.Formatter(
    "%(asctime)s | %(message)s"
)

event_handler.setFormatter(event_formatter)

event_logger.addHandler(event_handler)
event_logger.propagate = False