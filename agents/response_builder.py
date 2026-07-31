"""
====================================================
Response Builder
====================================================
"""


class ResponseBuilder:

    def merge(self, responses):

        chat = []

        executions = []

        errors = []

        for response in responses:

            tipo = response.get("type")

            if tipo == "chat":

                chat.append(

                    response.get(

                        "text",

                        ""

                    )

                )

            elif tipo == "execution":

                executions.append(response)

            elif tipo == "error":

                errors.append(

                    response.get(

                        "text",

                        ""

                    )

                )

        return {

            "chat": "\n\n".join(chat),

            "executions": executions,

            "errors": errors

        }


response_builder = ResponseBuilder()