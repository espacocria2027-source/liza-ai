from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
from groq import Groq
import os
import json

# 🔥 app sempre primeiro
app = Flask(__name__)
CORS(app)

# 🔑 Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 🧠 memória
historico = []

@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/chat", methods=["POST"])
def chat():

    dados = request.json

    if not dados or "message" not in dados:
        return jsonify({"response": "Mensagem vazia"}), 400

    mensagem = dados["message"]

    historico.append({"role": "user", "content": mensagem})

    contexto = historico[-10:]

    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Você é L.I.Z.A, uma IA feminina, amigável e fale em português do Brasil."
            }
        ] + contexto,
        stream=True
    )

    def gerar():

        resposta_final = ""

        for chunk in stream:
            if chunk.choices[0].delta.content:
                parte = chunk.choices[0].delta.content
                resposta_final += parte

                yield f"data: {json.dumps({'text': parte})}\n\n"

        historico.append({"role": "assistant", "content": resposta_final})

        yield "data: [DONE]\n\n"

    return Response(gerar(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)