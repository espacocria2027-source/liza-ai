from flask import (
    Flask,
    request,
    jsonify,
    send_from_directory
)

from flask_cors import CORS

# ==========================================================
# DATABASE
# ==========================================================

from database import criar_tabela

# ==========================================================
# SERVICES
# ==========================================================

from services.auth_service import (
    registrar_usuario,
    login_usuario
)

from services.chat_service import (
    processar_chat
)

from services.vision_service import (
    analisar_imagem_bytes
)

from services.tts_service import (
    gerar_audio
)

# ==========================================================
# FLASK
# ==========================================================

app = Flask(__name__)

CORS(app)

criar_tabela()

# ==========================================================
# ESTADO DA L.I.Z.A.
# ==========================================================

modo_sistema = {
    "ligado": True
}

# ==========================================================
# HOME
# ==========================================================

@app.route("/")
def home():

    return send_from_directory(
        ".",
        "index.html"
    )
# ==========================================================
# REGISTER
# ==========================================================

@app.route("/register", methods=["POST"])
def register():

    dados = request.json or {}

    return jsonify(

        registrar_usuario(

            usuario=dados.get("usuario"),

            senha=dados.get("senha")

        )

    )


# ==========================================================
# LOGIN
# ==========================================================

@app.route("/login", methods=["POST"])
def login():

    dados = request.json or {}

    return jsonify(

        login_usuario(

            usuario=dados.get("usuario"),

            senha=dados.get("senha")

        )

    )


# ==========================================================
# COMANDOS
# ==========================================================

@app.route("/comando", methods=["POST"])
def comando():

    dados = request.json or {}

    cmd = dados.get("cmd", "").lower()

    if cmd in [

        "desligar",

        "off",

        "desativa"

    ]:

        modo_sistema["ligado"] = False

        return jsonify({

            "ligado": False,

            "message": "L.I.Z.A desligada."

        })

    if cmd in [

        "ligar",

        "on",

        "ativa"

    ]:

        modo_sistema["ligado"] = True

        return jsonify({

            "ligado": True,

            "message": "L.I.Z.A ligada."

        })

    return jsonify({

        "ligado": modo_sistema["ligado"],

        "message": "Comando não reconhecido."

    })
# ==========================================================
# ANALISAR IMAGEM
# ==========================================================

@app.route("/analisar-imagem", methods=["POST"])
def analisar_imagem():

    try:

        if "imagem" not in request.files:

            return jsonify({

                "success": False,

                "text": "Nenhuma imagem enviada."

            }), 400

        imagem = request.files["imagem"]

        descricao = analisar_imagem_bytes(

            imagem.read()

        )

        return jsonify({

            "success": True,

            "text": descricao

        })

    except Exception as e:

        print("ERRO VISION:", e)

        return jsonify({

            "success": False,

            "text": f"Erro ao analisar imagem: {str(e)}"

        }), 500
    # ==========================================================
# CHAT (L.I.Z.A.)
# ==========================================================

@app.route("/chat", methods=["POST"])
def chat():

    dados = request.json or {}

    mensagem = dados.get("message", "").strip()

    usuario = dados.get("usuario", "").strip()

    if not mensagem:

        return jsonify({

            "success": False,

            "text": "Mensagem vazia."

        }), 400

    if not usuario:

        return jsonify({

            "success": False,

            "text": "Usuário não informado."

        }), 400

    if not modo_sistema["ligado"]:

        return jsonify({

            "success": False,

            "text": "L.I.Z.A. está desligada no momento."

        })

    comando = mensagem.lower()

    if comando in [

        "desliga l.i.z.a",

        "desliga liza"

    ]:

        modo_sistema["ligado"] = False

        return jsonify({

            "success": True,

            "text": "Desligando sistema L.I.Z.A..."

        })

    if comando in [

        "liga l.i.z.a",

        "liga liza"

    ]:

        modo_sistema["ligado"] = True

        return jsonify({

            "success": True,

            "text": "L.I.Z.A. ativada novamente."

        })

    try:

        resposta = processar_chat(

            usuario=usuario,

            mensagem=mensagem

        )

        return jsonify({

            "success": True,

            "text": resposta

        })

    except Exception as e:

        print("ERRO CHAT:", e)

        return jsonify({

            "success": False,

            "text": str(e)

        }), 500
    # ==========================================================
# TEXT TO SPEECH (L.I.Z.A.)
# ==========================================================

@app.route("/tts", methods=["POST"])
def tts():

    try:

        dados = request.json or {}

        texto = dados.get("text", "").strip()

        if not texto:

            return jsonify({

                "success": False,

                "error": "Texto vazio."

            }), 400

        arquivo = gerar_audio(

            texto=texto

        )

        return send_from_directory(

            ".",

            arquivo,

            mimetype="audio/mpeg"

        )

    except Exception as e:

        print("ERRO TTS:", e)

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({

        "success": True,

        "status": "online",

        "service": "L.I.Z.A Backend",

        "version": "2.0"

    })


# ==========================================================
# START SERVER
# ==========================================================

if __name__ == "__main__":

    print()

    print("==========================================")

    print("        L.I.Z.A Backend iniciado")

    print("==========================================")

    print("Servidor: http://0.0.0.0:10000")

    print("Status: Online")

    print("==========================================")

    print()

    app.run(

        host="0.0.0.0",

        port=10000,

        debug=False

    )