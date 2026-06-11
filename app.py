from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
import os

from database import criar_tabela, conectar

app = Flask(__name__)
CORS(app)

criar_tabela()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
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

    dados = request.json
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

@app.route("/login", methods=["POST"])
def login():

    dados = request.json
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


# =========================
# COMANDOS DO SISTEMA
# =========================

@app.route("/comando", methods=["POST"])
def comando():

    dados = request.json
    cmd = dados.get("cmd", "").lower()

    if cmd in ["desligar", "off", "desativa"]:
        modo_sistema["ligado"] = False

    elif cmd in ["ligar", "on", "ativa"]:
        modo_sistema["ligado"] = True

    return jsonify({
        "ligado": modo_sistema["ligado"]
    })


# =========================
# CHAT (ELITE 2 REAL)
# =========================

@app.route("/chat", methods=["POST"])
def chat():

    dados = request.json

    if not dados or "message" not in dados:
        return jsonify({"text": "Mensagem vazia"}), 400

    mensagem = dados["message"]
    usuario = dados.get("usuario")

    # 🔥 BLOQUEIO DO SISTEMA
    if not modo_sistema["ligado"]:
        return jsonify({
            "text": "L.I.Z.A está desligada no momento."
        })

    msg_lower = mensagem.lower()

    if "desliga l.i.z.a" in msg_lower:
        modo_sistema["ligado"] = False
        return jsonify({"text": "Desligando sistema L.I.Z.A..."})

    if "liga l.i.z.a" in msg_lower:
        modo_sistema["ligado"] = True
        return jsonify({"text": "L.I.Z.A ativada novamente."})

    # =========================
    # MEMÓRIA POR USUÁRIO (REAL)
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
    # IA
    # =========================

    resposta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """
Você é L.I.Z.A.

Você é uma inteligência artificial feminina.

Fale sempre em português do Brasil.

Seu criador é Beto.

Se alguém perguntar quem criou você, responda que foi Beto.

Você é amigável, inteligente, educada e prestativa.

Você ajuda programação, estudos e tecnologia.
"""
            }
        ] + historico + [
            {"role": "user", "content": mensagem}
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
# START
# =========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )