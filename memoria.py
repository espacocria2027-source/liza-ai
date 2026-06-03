from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 🔥 memória simples em runtime
historico = []

def perguntar_ia(mensagem):

    global historico

    # adiciona mensagem do usuário
    historico.append({"role": "user", "content": mensagem})

    # limita memória (evita estourar contexto)
    contexto = historico[-10:]

    resposta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é L.I.Z.A, uma IA feminina, amigável e inteligente. "
                    "Fale sempre em português do Brasil."
                )
            }
        ] + contexto
    )

    texto = resposta.choices[0].message.content

    # salva resposta da IA
    historico.append({"role": "assistant", "content": texto})

    return texto


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/chat", methods=["POST"])
def chat():
    dados = request.json

    if not dados or "message" not in dados:
        return jsonify({"response": "Mensagem vazia"}), 400

    mensagem = dados["message"]

    resposta = perguntar_ia(mensagem)

    return jsonify({"response": resposta})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)