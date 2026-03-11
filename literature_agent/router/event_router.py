class EventRouter:

    def __init__(self):
        self.routes = {}

    def register_queue(self, event_type, q):
        self.routes.setdefault(event_type, []).append(q)

    def resolve_destinations(self, event):
        """
        Placeholder for future routing logic.
        """
        return self.routes.get(event.type, [])

    def publish(self, event):

        destinations = self.resolve_destinations(event)

        if not destinations:
            print(f"[Router] No route for event type: {event.type}")
            return

        for q in destinations:
            q.put(event)