from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
from groq import Groq
from elevenlabs.client import ElevenLabs
import os

from database import criar_tabela, conectar

app = Flask(__name__)
CORS(app)

criar_tabela()

# =========================
# CLIENTES IA
# =========================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

eleven = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

# =========================
# ESTADO DO SISTEMA
# =========================

modo_sistema = {
    "ligado": True
}

# =========================
# HOME
# =========================

@app.route("/")
def home():
    return send_from_directory(".", "index.html")


# =========================
# REGISTER
# =========================

@app.route("/register", methods=["POST"])
def register():
    dados = request.json or {}
    usuario = dados.get("usuario")
    senha = dados.get("senha")

    if not usuario or not senha:
        return jsonify({"success": False, "message": "Preencha usuário e senha"})

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
            (usuario, senha)
        )

        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Usuário criado com sucesso"})

    except Exception:
        return jsonify({"success": False, "message": "Usuário já existe"})


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["POST"])
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

    return jsonify({"success": False, "message": "Usuário ou senha incorretos"})


# =========================
# COMANDOS
# =========================

@app.route("/comando", methods=["POST"])
def comando():
    dados = request.json or {}
    cmd = dados.get("cmd", "").lower()

    if cmd in ["desligar", "off", "desativa"]:
        modo_sistema["ligado"] = False

    elif cmd in ["ligar", "on", "ativa"]:
        modo_sistema["ligado"] = True

    return jsonify({"ligado": modo_sistema["ligado"]})


# =========================
# CHAT (L.I.Z.A)
# =========================

@app.route("/chat", methods=["POST"])
def chat():
    dados = request.json or {}

    mensagem = dados.get("message")
    usuario = dados.get("usuario")

    if not mensagem:
        return jsonify({"text": "Mensagem vazia"}), 400

    if not usuario:
        return jsonify({"text": "Usuário não informado"}), 400

    if not modo_sistema["ligado"]:
        return jsonify({"text": "L.I.Z.A está desligada no momento."})

    msg_lower = mensagem.lower()

    if "desliga l.i.z.a" in msg_lower:
        modo_sistema["ligado"] = False
        return jsonify({"text": "Desligando sistema L.I.Z.A..."})

    if "liga l.i.z.a" in msg_lower:
        modo_sistema["ligado"] = True
        return jsonify({"text": "L.I.Z.A ativada novamente."})

    # =========================
    # MEMÓRIA
    # =========================

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT mensagem, resposta FROM memoria WHERE usuario=? ORDER BY id DESC LIMIT 10",
        (usuario,)
    )

    rows = cursor.fetchall()

    historico = []
    for r in reversed(rows):
        historico.append({"role": "user", "content": r[0]})
        historico.append({"role": "assistant", "content": r[1]})

       # =========================
    # IA (GROQ)
    # =========================

    resposta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """
Você é L.I.Z.A.

Uma inteligência artificial feminina criada por Beto.

Fale sempre em português do Brasil.

Sua personalidade é:

- Inteligente
- Amigável
- Natural
- Prestativa
- Levemente descontraída

Evite respostas robóticas.

Converse como uma pessoa real.

Ajude com programação,
tecnologia, estudos e tarefas
do dia a dia.

Sua voz é Sarah.

Responda sempre de forma clara,
útil e agradável.
"""
            }
        ] + historico + [
            {
                "role": "user",
                "content": mensagem
            }
        ]
    )

    texto = resposta.choices[0].message.content

    # =========================
    # SALVAR MEMÓRIA
    # =========================

    cursor.execute(
        "INSERT INTO memoria (usuario, mensagem, resposta) VALUES (?, ?, ?)",
        (usuario, mensagem, texto)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "text": texto
    })


# =========================
# VOZ (ELEVENLABS - SARAH)
# =========================

@app.route("/tts", methods=["POST"])
def tts():

    dados = request.json or {}
    texto = dados.get("text", "")

    if not texto:
        return jsonify({
            "error": "Texto vazio"
        }), 400

    audio_stream = eleven.text_to_speech.convert(
        voice_id="EXAVITQu4vr4xnSDxMaL",  # Sarah
        model_id="eleven_multilingual_v2",
        text=texto
    )

    audio_bytes = b"".join(audio_stream)

    return Response(
        audio_bytes,
        mimetype="audio/mpeg"
    )
# =========================
# START
# =========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )