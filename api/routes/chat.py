from flask import Blueprint
from flask import request
from flask import jsonify

from core.liza import liza


chat_bp = Blueprint(

    "chat",

    __name__

)


@chat_bp.route("/chat", methods=["POST"])
def chat():

    dados = request.get_json(force=True, silent=True) or {}

    usuario = dados.get(

        "usuario",

        "usuario"

    )

    mensagem = dados.get(

        "message",

        ""

    )

    resultado = liza.process(

        usuario,

        mensagem

    )

    return jsonify(resultado)