"""
=========================================
L.I.Z.A Actions
=========================================
"""

from enum import Enum


class Action(str, Enum):

    OPEN_APP = "open_app"

    CLOSE_APP = "close_app"

    PLAY_MUSIC = "play_music"

    PLAY_PLAYLIST = "play_playlist"

    SET_VOLUME = "set_volume"

    GOOGLE_SEARCH = "google_search"

    SEND_MESSAGE = "send_message"

    CALL = "call"

    OPEN_CAMERA = "open_camera"

    OPEN_SETTINGS = "open_settings"

    OPEN_BROWSER = "open_browser"

    TURN_WIFI_ON = "wifi_on"

    TURN_WIFI_OFF = "wifi_off"

    TURN_BLUETOOTH_ON = "bluetooth_on"

    TURN_BLUETOOTH_OFF = "bluetooth_off"

    UNKNOWN = "unknown"