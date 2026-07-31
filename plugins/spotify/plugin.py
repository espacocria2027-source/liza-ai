from plugins.base_plugin import BasePlugin


class SpotifyPlugin(BasePlugin):

    @property
    def name(self):

        return "spotify"

    def initialize(self):

        print("Spotify Plugin carregado.")

    def execute(self, action, parameters):

        if action == "play":

            return {

                "success": True,

                "message": "Tocando música."

            }

        return {

            "success": False,

            "message": "Ação desconhecida."

        }