from plugins.base_plugin import BasePlugin


class AndroidPlugin(BasePlugin):

    @property
    def name(self):
        return "android"

    def initialize(self):
        print("Android Plugin carregado.")

    def execute(self, action, parameters):

        if action == "open_youtube":

            return {
                "success": True,
                "action": "open_url",
                "url": "https://www.youtube.com"
            }

        elif action == "open_google":

            return {
                "success": True,
                "action": "open_url",
                "url": "https://www.google.com"
            }

        elif action == "open_spotify":

            return {
                "success": True,
                "action": "open_url",
                "url": "https://open.spotify.com"
            }

        return {
            "success": False,
            "message": "Ação desconhecida."
        }