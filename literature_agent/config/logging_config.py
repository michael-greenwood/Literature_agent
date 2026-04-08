import logging
import os


def setup_logging():

    if logging.getLogger().handlers:
        return  # 🔥 prevents duplicate handlers on reload

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOG_DIR = os.path.join(BASE_DIR, "logs")

    os.makedirs(LOG_DIR, exist_ok=True)

    # Root logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(LOG_DIR, "literature_agent.log")),
            logging.StreamHandler()
        ]
    )

    # Event trace logger
    event_logger = logging.getLogger("EventTrace")
    event_logger.setLevel(logging.INFO)

    if not event_logger.handlers:  # 🔥 prevent duplicates
        event_handler = logging.FileHandler(os.path.join(LOG_DIR, "event_trace.log"))

        event_formatter = logging.Formatter(
            "%(asctime)s | %(message)s"
        )

        event_handler.setFormatter(event_formatter)
        event_logger.addHandler(event_handler)

    event_logger.propagate = False