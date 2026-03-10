import queue


class EventRouter:

    def __init__(self):
        self.queues = {}

    def register_queue(self, event_type, q):
        self.queues.setdefault(event_type, []).append(q)

    def publish(self, event):
        if event.type not in self.queues:
            return

        for q in self.queues[event.type]:
            q.put(event)