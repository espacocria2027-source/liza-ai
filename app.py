from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

humor = "feliz"

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def perguntar_ia(pergunta):

    resposta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"""
Você é L.I.Z.A.

Você é uma IA feminina.

Fale em português do Brasil.

Humor atual: {humor}

Você é amigável, inteligente e prestativa.
"""
            },
            {
                "role": "user",
                "content": pergunta
            }
        ]
    )

    return resposta.choices[0].message.content


@app.route("/chat", methods=["POST"])
def chat():

    dados = request.json

    if not dados or "message" not in dados:
        return jsonify({
            "response": "Mensagem vazia"
        }), 400

    mensagem = dados["message"]

    resposta = perguntar_ia(mensagem)

    return jsonify({
        "response": resposta
    })


@app.route("/")
def home():
    return "L.I.Z.A ONLINE"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )