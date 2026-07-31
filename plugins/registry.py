"""
====================================================
Registro de Plugins
====================================================
"""

from plugins.plugin_manager import plugin_manager

from plugins.spotify.plugin import SpotifyPlugin
from plugins.android.plugin import AndroidPlugin


plugin_manager.register(

    SpotifyPlugin()

)

plugin_manager.register(

    AndroidPlugin()
)