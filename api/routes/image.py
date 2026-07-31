"""
====================================================
IMAGE ROUTE
====================================================
"""

from flask import Blueprint
from flask import jsonify
from flask import request

import base64

from ai.providers.model_provider import provider

image_bp = Blueprint(
    "image",
    __name__
)


@image_bp.route("/analisar-imagem", methods=["POST"])
def analisar_imagem():

    try:

        if "imagem" not in request.files:

            return jsonify({

                "text": "Nenhuma imagem enviada."

            }), 400

        imagem = request.files["imagem"]

        conteudo = imagem.read()

        imagem_base64 = base64.b64encode(
            conteudo
        ).decode("utf-8")

        messages = [

            {

                "role": "user",

                "content": [

                    {

                        "type": "text",

                        "text": (
                            "Descreva detalhadamente esta imagem "
                            "em português do Brasil. "
                            "Fale naturalmente como a L.I.Z.A."
                        )

                    },

                    {

                        "type": "image_url",

                        "image_url": {

                            "url": f"data:image/jpeg;base64,{imagem_base64}"

                        }

                    }

                ]

            }

        ]

        resposta = provider.vision(messages)

        return jsonify({

            "text": resposta

        })

    except Exception as e:

        return jsonify({

            "text": str(e)

        }), 500