"""
====================================================
Android Client Manager
====================================================
"""

from threading import Lock


class AndroidClientManager:

    def __init__(self):

        self.lock = Lock()

        self.devices = {}

    def connect(self, device_id, info):

        with self.lock:

            self.devices[device_id] = {

                "online": True,

                "info": info

            }

    def disconnect(self, device_id):

        with self.lock:

            if device_id in self.devices:

                self.devices[device_id]["online"] = False

    def is_online(self, device_id):

        if device_id not in self.devices:
            return False

        return self.devices[device_id]["online"]

    def get(self, device_id):

        return self.devices.get(device_id)

    def all(self):

        return self.devices


android_clients = AndroidClientManager()