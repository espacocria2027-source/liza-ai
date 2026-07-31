from flask import Blueprint
from flask import request
from flask import jsonify


command_bp = Blueprint(
    "command",
    __name__
)

# Estado do sistema
modo_sistema = {
    "ligado": True
}


@command_bp.route("/comando", methods=["POST"])
def comando():

    dados = request.json or {}

    cmd = dados.get("cmd", "").lower()

    if cmd in ["desligar", "off", "desativa"]:

        modo_sistema["ligado"] = False

    elif cmd in ["ligar", "on", "ativa"]:

        modo_sistema["ligado"] = True

    return jsonify({

        "ligado": modo_sistema["ligado"]

    })


def sistema_ligado():

    return modo_sistema["ligado"]


def ligar():

    modo_sistema["ligado"] = True


def desligar():

    modo_sistema["ligado"] = False