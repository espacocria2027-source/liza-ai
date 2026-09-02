from flask import Blueprint
from flask import request
from flask import jsonify
from flask import Response
from flask import stream_with_context
import json

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

    # ======================================================
    # DADOS
    # ======================================================

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

    # ======================================================
    # DEBUG
    # ======================================================

    print(
        "========================================"
    )

    print(
        "LIZA CHAT STREAM"
    )

    print(
        f"Usuário: {usuario}"
    )

    print(
        f"Mensagem: {mensagem}"
    )

    print(
        "========================================"
    )

    # ======================================================
    # GERADOR SSE
    # ======================================================

    def generate():

        try:

            for token in conversar_stream(
                usuario,
                prompt,
                mensagem
            ):

                if token is None:
                    continue

                token = str(token)

                if not token:
                    continue

                # ------------------------------------------
                # ENVIA O TOKEN COMO JSON
                # ------------------------------------------

                payload = json.dumps(
                    token,
                    ensure_ascii=False
                )

                yield f"data:{payload}\n\n"

            # ------------------------------------------
            # FINAL DO STREAM
            # ------------------------------------------

            yield "event:end\ndata:done\n\n"

            print(
                "LIZA STREAM FINALIZADO"
            )

        except Exception as e:

            print(
                "ERRO NO LIZA STREAM:"
            )

            print(
                str(e)
            )

            # ------------------------------------------
            # ENVIA ERRO PARA O ANDROID
            # ------------------------------------------

            erro = json.dumps(
                str(e),
                ensure_ascii=False
            )

            yield (
                "event:error\n"
                f"data:{erro}\n\n"
            )

    # ======================================================
    # RESPOSTA SSE
    # ======================================================

    return Response(

        stream_with_context(
            generate()
        ),

        mimetype="text/event-stream",

        headers={

            "Cache-Control": "no-cache",

            "Connection": "keep-alive",

            "X-Accel-Buffering": "no",

            "Access-Control-Allow-Origin": "*"

        }

    )