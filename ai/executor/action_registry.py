"""
=========================================
Action Registry
=========================================
"""

from ai.executor.actions import Action


class ActionRegistry:

    def __init__(self):

        self.actions = {

            Action.OPEN_APP: self.open_app,

            Action.CLOSE_APP: self.close_app,

            Action.PLAY_MUSIC: self.play_music,

            Action.PLAY_PLAYLIST: self.play_playlist,

            Action.SET_VOLUME: self.set_volume,

            Action.GOOGLE_SEARCH: self.google_search,

            Action.SEND_MESSAGE: self.send_message,

            Action.CALL: self.call,

            Action.OPEN_CAMERA: self.open_camera,

            Action.OPEN_SETTINGS: self.open_settings,

            Action.OPEN_BROWSER: self.open_browser,

            Action.TURN_WIFI_ON: self.wifi_on,

            Action.TURN_WIFI_OFF: self.wifi_off,

            Action.TURN_BLUETOOTH_ON: self.bluetooth_on,

            Action.TURN_BLUETOOTH_OFF: self.bluetooth_off

        }

    def execute(self, action, parameters):

        func = self.actions.get(action)

        if func is None:

            return {

                "success": False,

                "error": "Ação desconhecida"

            }

        return func(parameters)

    def open_app(self, p):
        return {"success": True, "command": "open_app", "parameters": p}

    def close_app(self, p):
        return {"success": True, "command": "close_app", "parameters": p}

    def play_music(self, p):
        return {"success": True, "command": "play_music", "parameters": p}

    def play_playlist(self, p):
        return {"success": True, "command": "play_playlist", "parameters": p}

    def set_volume(self, p):
        return {"success": True, "command": "set_volume", "parameters": p}

    def google_search(self, p):
        return {"success": True, "command": "google_search", "parameters": p}

    def send_message(self, p):
        return {"success": True, "command": "send_message", "parameters": p}

    def call(self, p):
        return {"success": True, "command": "call", "parameters": p}

    def open_camera(self, p):
        return {"success": True, "command": "open_camera", "parameters": p}

    def open_settings(self, p):
        return {"success": True, "command": "open_settings", "parameters": p}

    def open_browser(self, p):
        return {"success": True, "command": "open_browser", "parameters": p}

    def wifi_on(self, p):
        return {"success": True, "command": "wifi_on", "parameters": p}

    def wifi_off(self, p):
        return {"success": True, "command": "wifi_off", "parameters": p}

    def bluetooth_on(self, p):
        return {"success": True, "command": "bluetooth_on", "parameters": p}

    def bluetooth_off(self, p):
        return {"success": True, "command": "bluetooth_off", "parameters": p}


registry = ActionRegistry()