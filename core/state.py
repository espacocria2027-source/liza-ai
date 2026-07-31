"""
====================================================
L.I.Z.A STATE
====================================================
"""


class LizaState:

    def __init__(self):

        self.online = True

        self.version = "2.0"

        self.device = None

        self.user = None

        self.last_execution = None

        self.mode = "normal"

        self.memory_loaded = False


state = LizaState()