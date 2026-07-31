"""
=========================================
PLUGIN MANAGER
=========================================
"""

class PluginManager:

    def __init__(self):

        self.plugins = []

    def register(self, plugin):

        self.plugins.append(plugin)

        print(f"[PLUGIN] {plugin.name} carregado.")

    def execute(self, action, data):

        for plugin in self.plugins:

            if plugin.can_handle(action):

                return plugin.execute(

                    action,

                    data

                )

        return None


plugin_manager = PluginManager()