from flask import Blueprint
from flask import request
from flask import jsonify

from database import conectar


auth_bp = Blueprint(
    "auth",
    __name__
)


# =========================
# REGISTER
# =========================

@auth_bp.route("/register", methods=["POST"])
def register():

    dados = request.json or {}

    usuario = dados.get("usuario")
    senha = dados.get("senha")

    if not usuario or not senha:

        return jsonify({

            "success": False,

            "message": "Preencha usuário e senha"

        })

    try:

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
            (usuario, senha)
        )

        conn.commit()

        conn.close()

        return jsonify({

            "success": True,

            "message": "Usuário criado com sucesso"

        })

    except Exception:

        return jsonify({

            "success": False,

            "message": "Usuário já existe"

        })


# =========================
# LOGIN
# =========================

@auth_bp.route("/login", methods=["POST"])
def login():

    dados = request.json or {}

    usuario = dados.get("usuario")
    senha = dados.get("senha")

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM usuarios WHERE usuario=? AND senha=?",

        (usuario, senha)

    )

    resultado = cursor.fetchone()

    conn.close()

    if resultado:

        return jsonify({

            "success": True,

            "message": "Login realizado",

            "usuario": usuario

        })

    return jsonify({

        "success": False,

        "message": "Usuário ou senha incorretos"

    })