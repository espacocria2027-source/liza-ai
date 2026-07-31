"""
====================================================
L.I.Z.A Event Bus
====================================================
"""

from collections import defaultdict


class EventBus:

    def __init__(self):

        self.listeners = defaultdict(list)

    def subscribe(self, event_name, callback):

        self.listeners[event_name].append(callback)

    def emit(self, event_name, data=None):

        if event_name not in self.listeners:
            return

        for callback in self.listeners[event_name]:

            try:

                callback(data)

            except Exception as e:

                print(f"[EVENT ERROR] {event_name}: {e}")


event_bus = EventBus()