from agents.base_agent import BaseAgent
import logging

logger = logging.getLogger("EventTrace")


class DebugAgent(BaseAgent):

    def handle_event(self, event):

        logger.info(
            "%s id=%s parent=%s source=%s",
            event.type,
            event.id,
            event.parent_id,
            event.source
        )