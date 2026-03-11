import queue
import threading


class BaseAgent(threading.Thread):

    def __init__(self, name, queue, router):
        super().__init__(daemon=True)
        self.name = name
        self.queue = queue
        self.router = router
        self.running = True

    def handle_event(self, event):
        raise NotImplementedError

    def run(self):

        while self.running:

            try:
                event = self.queue.get(timeout=1)
            except queue.Empty:
                continue

            try:
                self.handle_event(event)
            except Exception as e:
                print(f"[{self.name}] Error handling event:", e)

            self.queue.task_done()

    def stop(self):
        self.running = False