"""
=========================================
L.I.Z.A. ACTIONS
=========================================
Todas as ações que o Android entende.
"""

from enum import Enum


class Action(str, Enum):

    # Conversa
    CHAT = "chat"

    # Aplicativos
    OPEN_APP = "open_app"
    CLOSE_APP = "close_app"

    # Navegador
    OPEN_BROWSER = "open_browser"

    # Pesquisas
    GOOGLE_SEARCH = "google_search"
    YOUTUBE_SEARCH = "youtube_search"

    # YouTube
    OPEN_VIDEO = "open_video"

    # Ligações
    CALL = "call"

    # SMS
    SEND_SMS = "send_sms"

    # WhatsApp
    SEND_WHATSAPP = "send_whatsapp"

    # Gmail
    SEND_EMAIL = "send_email"

    # Agenda
    CREATE_EVENT = "create_event"

    # Alarmes
    CREATE_ALARM = "create_alarm"

    # Lembretes
    CREATE_REMINDER = "create_reminder"

    # Contatos
    OPEN_CONTACT = "open_contact"

    # Google Maps
    OPEN_MAPS = "open_maps"

    # Spotify
    OPEN_SPOTIFY = "open_spotify"

    PLAY_SPOTIFY = "play_spotify"

    # Câmera
    OPEN_CAMERA = "open_camera"

    TAKE_PHOTO = "take_photo"

    # Galeria
    OPEN_GALLERY = "open_gallery"

    # Arquivos
    OPEN_FILES = "open_files"

    # Lanterna
    FLASHLIGHT_ON = "flashlight_on"

    FLASHLIGHT_OFF = "flashlight_off"

    # Wi-Fi
    WIFI_ON = "wifi_on"

    WIFI_OFF = "wifi_off"

    # Bluetooth
    BLUETOOTH_ON = "bluetooth_on"

    BLUETOOTH_OFF = "bluetooth_off"

    # Volume
    VOLUME_UP = "volume_up"

    VOLUME_DOWN = "volume_down"

    MUTE = "mute"

    # Brilho
    BRIGHTNESS = "brightness"

    # Configurações
    OPEN_SETTINGS = "open_settings"

    # Assistente
    SHARE_TEXT = "share_text"

    COPY_TEXT = "copy_text"

    # Música
    PLAY_MUSIC = "play_music"

    PAUSE_MUSIC = "pause_music"

    NEXT_MUSIC = "next_music"

    PREVIOUS_MUSIC = "previous_music"

    # Sistema
    DEVICE_INFO = "device_info"

    BATTERY = "battery"

    LOCATION = "location"

    # IA
    EXECUTE = "execute"

    UNKNOWN = "unknown"