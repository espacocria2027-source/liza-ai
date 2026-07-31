"""
=========================================
L.I.Z.A Tool Selector
=========================================
"""

from dataclasses import dataclass


@dataclass
class ToolResult:

    action: str

    parameters: dict


class ToolSelector:

    def select(self, reasoning):

        action = reasoning.get("action", "UNKNOWN")

        parameters = reasoning.get("parameters", {})

        # ===================================
        # Android
        # ===================================

        if action == "OPEN_APP":

            return ToolResult(

                action="OPEN_APP",

                parameters={

                    "package": parameters.get("package")

                }

            )

        if action == "GOOGLE_SEARCH":

            return ToolResult(

                action="GOOGLE_SEARCH",

                parameters={

                    "query": parameters.get("query")

                }

            )

        if action == "YOUTUBE_SEARCH":

            return ToolResult(

                action="YOUTUBE_SEARCH",

                parameters={

                    "query": parameters.get("query")

                }

            )

        if action == "SEND_WHATSAPP":

            return ToolResult(

                action="SEND_WHATSAPP",

                parameters={

                    "phone": parameters.get("phone"),

                    "message": parameters.get("message")

                }

            )

        if action == "CALL":

            return ToolResult(

                action="CALL",

                parameters={

                    "phone": parameters.get("phone")

                }

            )

        if action == "OPEN_BROWSER":

            return ToolResult(

                action="OPEN_BROWSER",

                parameters={

                    "url": parameters.get("url")

                }

            )

        if action == "OPEN_CAMERA":

            return ToolResult(

                action="OPEN_CAMERA",

                parameters={}

            )

        if action == "SET_VOLUME":

            return ToolResult(

                action="SET_VOLUME",

                parameters={

                    "level": parameters.get("level", 50)

                }

            )

        if action == "CREATE_EVENT":

            return ToolResult(

                action="CREATE_EVENT",

                parameters=parameters

            )

        if action == "SEND_EMAIL":

            return ToolResult(

                action="SEND_EMAIL",

                parameters=parameters

            )

        return ToolResult(

            action="UNKNOWN",

            parameters={}

        )


tool_selector = ToolSelector()