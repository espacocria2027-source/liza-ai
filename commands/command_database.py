"""
====================================================
L.I.Z.A Command Database
====================================================
"""

from commands.apps import APPS
from commands.browser import BROWSER
from commands.camera import CAMERA
from commands.communication import COMMUNICATION
from commands.media import MEDIA
from commands.search import SEARCH
from commands.system import SYSTEM


COMMANDS = (

    APPS
    + BROWSER
    + CAMERA
    + COMMUNICATION
    + MEDIA
    + SEARCH
    + SYSTEM

)