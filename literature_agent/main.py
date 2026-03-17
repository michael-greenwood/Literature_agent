from lit_agent_engine import LitAgentEngine
import time

engine = LitAgentEngine()
engine.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    engine.stop()