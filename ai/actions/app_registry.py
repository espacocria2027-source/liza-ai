"""
=========================================
L.I.Z.A. APP REGISTRY
=========================================
Centraliza todos os aplicativos conhecidos.
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class AppInfo:

    name: str

    package: str

    aliases: list[str]


class AppRegistry:

    def __init__(self):

        self.apps: Dict[str, AppInfo] = {}

        self._register_defaults()

    def register(
        self,
        name: str,
        package: str,
        aliases: list[str]
    ):

        app = AppInfo(
            name=name,
            package=package,
            aliases=aliases
        )

        self.apps[name.lower()] = app

        for alias in aliases:

            self.apps[alias.lower()] = app

    def find(self, text: str) -> Optional[AppInfo]:

        text = text.lower()

        for key, app in self.apps.items():

            if key in text:

                return app

        return None

    def list_apps(self):

        unique = {}

        for app in self.apps.values():

            unique[app.package] = app

        return list(unique.values())

    def _register_defaults(self):

        self.register(

            "WhatsApp",

            "com.whatsapp",

            [

                "zap",

                "whatsapp",

                "whats"

            ]

        )

        self.register(

            "Instagram",

            "com.instagram.android",

            [

                "instagram",

                "insta"

            ]

        )

        self.register(

            "Facebook",

            "com.facebook.katana",

            [

                "facebook",

                "face"

            ]

        )

        self.register(

            "YouTube",

            "com.google.android.youtube",

            [

                "youtube",

                "yt"

            ]

        )

        self.register(

            "Chrome",

            "com.android.chrome",

            [

                "chrome",

                "google"

            ]

        )

        self.register(

            "Gmail",

            "com.google.android.gm",

            [

                "gmail",

                "email"

            ]

        )

        self.register(

            "Spotify",

            "com.spotify.music",

            [

                "spotify"

            ]

        )

        self.register(

            "Telegram",

            "org.telegram.messenger",

            [

                "telegram"

            ]

        )

        self.register(

            "Netflix",

            "com.netflix.mediaclient",

            [

                "netflix"

            ]

        )

        self.register(

            "Maps",

            "com.google.android.apps.maps",

            [

                "maps",

                "mapas",

                "google maps"

            ]

        )

        self.register(

            "Câmera",

            "camera",

            [

                "camera",

                "câmera"

            ]

        )

        self.register(

            "Galeria",

            "gallery",

            [

                "galeria",

                "gallery",

                "fotos"

            ]

        )

        self.register(

            "Configurações",

            "settings",

            [

                "configurações",

                "configuracoes",

                "settings"

            ]

        )


registry = AppRegistry()