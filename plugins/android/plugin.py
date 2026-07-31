from plugins.base_plugin import BasePlugin


class AndroidPlugin(BasePlugin):

    @property
    def name(self):

        return "android"

    def initialize(self):

        print("Android Plugin carregado.")

    def execute(self, action, parameters):

        return {

            "success": True,

            "action": action,

            "parameters": parameters

        }