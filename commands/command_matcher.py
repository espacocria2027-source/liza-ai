"""
====================================================
L.I.Z.A Command Matcher
====================================================
"""

import re

from commands.command_database import COMMANDS


class CommandMatcher:

    def detect(self, message):

        texto = message.lower().strip()

        for command in COMMANDS:

            for pattern in command.patterns:

                match = re.search(

                    pattern,

                    texto,

                    re.IGNORECASE

                )

                if match is None:

                    continue

                parameters = {}

                # ==========================================
                # GOOGLE SEARCH
                # ==========================================

                if command.action == "GOOGLE_SEARCH":

                    parameters["query"] = match.group(1)

                # ==========================================
                # YOUTUBE SEARCH
                # ==========================================

                elif command.action == "YOUTUBE_SEARCH":

                    parameters["query"] = match.group(1)

                # ==========================================
                # PLAYLIST
                # ==========================================

                elif command.action == "PLAY_PLAYLIST":

                    parameters["playlist"] = match.group(1)

                # ==========================================
                # PLAY VIDEO
                # ==========================================

                elif command.action == "PLAY_VIDEO":

                    parameters["video"] = match.group(1)

                # ==========================================
                # WHATSAPP
                # ==========================================

                elif command.action == "SEND_WHATSAPP":

                    parameters["contact"] = match.group(1)

                    parameters["message"] = match.group(2)

                # ==========================================
                # EMAIL
                # ==========================================

                elif command.action == "SEND_EMAIL":

                    parameters["to"] = match.group(1)

                    parameters["message"] = match.group(2)

                # ==========================================
                # CALL
                # ==========================================

                elif command.action == "CALL":

                    parameters["contact"] = match.group(1)

                return {

                    "intent": "android",

                    "action": command.action,

                    "parameters": parameters

                }

        return None


matcher = CommandMatcher()