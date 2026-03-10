import threading


class BaseAgent(threading.Thread):

    def __init__(self, name, queue, router):
        super().__init__(daemon=True)
        self.name = name
        self.queue = queue
        self.router = router
        self.running = True

    def handle_event(self, event):
        """
        Override in subclasses
        """
        raise NotImplementedError

    def run(self):
        while self.running:
            event = self.queue.get()

            try:
                self.handle_event(event)
            except Exception as e:
                print(f"[{self.name}] Error handling event:", e)

            self.queue.task_done()

    def stop(self):
        self.running = False