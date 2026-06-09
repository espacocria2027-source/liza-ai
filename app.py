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

historico = []

@app.route("/")
def home():
    return send_from_directory(".", "index.html")


# =========================
# CADASTRO
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
            "message": "Login realizado"
        })

    return jsonify({
        "success": False,
        "message": "Usuário ou senha incorretos"
    })


# =========================
# CHAT
# =========================

@app.route("/chat", methods=["POST"])
def chat():

    dados = request.json

    if not dados or "message" not in dados:
        return jsonify({"text": "Mensagem vazia"}), 400

    mensagem = dados["message"]

    historico.append({
        "role": "user",
        "content": mensagem
    })

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

Se alguém perguntar quem criou você,
responda que foi Beto.

Você é amigável, inteligente,
educada e prestativa.

Você gosta de ajudar as pessoas
com programação, estudos,
tecnologia e assuntos do dia a dia.

Seu nome completo é L.I.Z.A.
"""
            }
        ] + historico[-10:]
    )

    texto = resposta.choices[0].message.content

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO memoria (mensagem, resposta) VALUES (?, ?)",
        (mensagem, texto)
    )

    conn.commit()
    conn.close()

    historico.append({
        "role": "assistant",
        "content": texto
    })

    return jsonify({
        "text": texto
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )