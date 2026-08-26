from flask import Blueprint
from flask import request
from flask import jsonify
from flask import Response
from flask import stream_with_context

from core.liza import liza
from ai.conversation_service import conversar_stream


chat_bp = Blueprint(

    "chat",

    __name__

)


# ==========================================================
# CHAT TRADICIONAL
# ==========================================================

@chat_bp.route(

    "/chat",

    methods=["POST"]

)
def chat():

    dados = request.get_json(

        force=True,

        silent=True

    ) or {}


    # ======================================================
    # DADOS RECEBIDOS
    # ======================================================

    usuario = dados.get(

        "usuario",

        "usuario"

    )


    mensagem = dados.get(

        "message",

        ""

    )


    prompt = dados.get(

        "prompt",

        ""

    )


    # ======================================================
    # DEBUG
    # ======================================================

    print(
        "========================================"
    )

    print(
        "LIZA CHAT"
    )

    print(
        f"Usuário: {usuario}"
    )

    print(
        f"Mensagem: {mensagem}"
    )

    print(
        "Prompt recebido: "
        + (
            "SIM"
            if prompt.strip()
            else "NÃO"
        )
    )

    print(
        f"Tamanho do prompt: {len(prompt)}"
    )

    print(
        "========================================"
    )


    # ======================================================
    # PROCESSAR LIZA
    # ======================================================

    resultado = liza.process(

        usuario,

        mensagem,

        prompt

    )


    # ======================================================
    # RESPOSTA
    # ======================================================

    return jsonify(

        resultado

    )


# ==========================================================
# CHAT STREAMING
# ==========================================================

@chat_bp.route(

    "/chat/stream",

    methods=["POST"]

)
def chat_stream():

    dados = request.get_json(

        force=True,

        silent=True

    ) or {}


    usuario = dados.get(

        "usuario",

        "usuario"

    )


    prompt = dados.get(

        "prompt",

        ""

    )


    mensagem = dados.get(

        "message",

        ""

    )


    def generate():

        for token in conversar_stream(

            usuario,

            prompt,

            mensagem

        ):

            yield f"data:{token}\n\n"


        yield "event:end\ndata:done\n\n"


    return Response(

        stream_with_context(

            generate()

        ),

        mimetype="text/event-stream",

        headers={

            "Cache-Control": "no-cache",

            "Connection": "keep-alive",

            "X-Accel-Buffering": "no"

        }

    )