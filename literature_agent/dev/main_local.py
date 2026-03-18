from literature_agent.engine import LitAgentEngine
import time

engine = LitAgentEngine()
engine.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    engine.stop()