"""
====================================================
Plugin Manager
====================================================
"""

class PluginManager:

    def __init__(self):

        self.plugins = {}

    def register(self, plugin):

        self.plugins[plugin.name] = plugin

        plugin.initialize()

    def get(self, name):

        return self.plugins.get(name)

    def all(self):

        return self.plugins

    def execute(self, plugin_name, action, parameters=None):

        plugin = self.get(plugin_name)

        if plugin is None:

            return {

                "success": False,

                "message": "Plugin não encontrado."

            }

        return plugin.execute(

            action,

            parameters or {}

        )


plugin_manager = PluginManager()