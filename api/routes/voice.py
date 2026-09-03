from flask import Blueprint
from flask import jsonify
from flask import request
from flask import Response
from flask import stream_with_context

import asyncio
import edge_tts
import time


voice_bp = Blueprint("voice", __name__)

VOICE = "pt-BR-FranciscaNeural"


# =========================================================
# EDGE-TTS
# =========================================================

async def gerar_audio(texto, inicio_request):
    inicio_edge = time.perf_counter()

    print()
    print("=" * 70)
    print("🎙️ EDGE-TTS INICIADO")
    print("Texto:", texto)
    print("=" * 70)

    print(
        f"⏱️ Desde chegada da requisição: "
        f"{inicio_edge - inicio_request:.3f}s"
    )

    communicate = edge_tts.Communicate(
        text=texto,
        voice=VOICE
    )

    primeiro_evento = True
    primeiro_audio = True

    total_bytes = 0
    total_chunks = 0

    try:

        async for chunk in communicate.stream():

            # =================================================
            # PRIMEIRO EVENTO EDGE-TTS
            # =================================================

            if primeiro_evento:

                primeiro_evento = False

                tempo_primeiro_evento = (
                    time.perf_counter() - inicio_edge
                )

                tempo_desde_request = (
                    time.perf_counter() - inicio_request
                )

                print(
                    f"📡 PRIMEIRO EVENTO EDGE-TTS: "
                    f"{tempo_primeiro_evento:.3f}s"
                )

                print(
                    f"📡 DESDE REQUEST: "
                    f"{tempo_desde_request:.3f}s"
                )

            # =================================================
            # IGNORA EVENTOS QUE NÃO SÃO ÁUDIO
            # =================================================

            if chunk["type"] != "audio":
                continue

            audio = chunk["data"]

            if not audio:
                continue

            # =================================================
            # PRIMEIRO ÁUDIO
            # =================================================

            if primeiro_audio:

                primeiro_audio = False

                agora = time.perf_counter()

                tempo_primeiro_audio = (
                    agora - inicio_edge
                )

                tempo_desde_request = (
                    agora - inicio_request
                )

                print()
                print("🎵 PRIMEIRO ÁUDIO EDGE-TTS")
                print(
                    f"🎵 Desde Edge-TTS: "
                    f"{tempo_primeiro_audio:.3f}s"
                )
                print(
                    f"🎵 Desde chegada da request: "
                    f"{tempo_desde_request:.3f}s"
                )
                print(
                    f"🎵 Primeiro chunk: "
                    f"{len(audio)} bytes"
                )
                print()

            # =================================================
            # CONTADORES
            # =================================================

            total_chunks += 1
            total_bytes += len(audio)

            # =================================================
            # ENVIA IMEDIATAMENTE PARA O FLASK
            # =================================================

            yield audio

    finally:

        tempo_total_edge = (
            time.perf_counter() - inicio_edge
        )

        tempo_total_request = (
            time.perf_counter() - inicio_request
        )

        print()
        print("=" * 70)
        print("🏁 EDGE-TTS FINALIZADO")
        print(
            f"📦 Chunks: {total_chunks}"
        )
        print(
            f"📦 Bytes: {total_bytes}"
        )
        print(
            f"⏱️ Tempo Edge-TTS: "
            f"{tempo_total_edge:.3f}s"
        )
        print(
            f"⏱️ Tempo desde request: "
            f"{tempo_total_request:.3f}s"
        )
        print("=" * 70)
        print()


# =========================================================
# STREAM BRIDGE
# =========================================================

def gerar_stream(texto, inicio_request):

    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    generator = gerar_audio(
        texto,
        inicio_request
    )

    try:

        while True:

            try:

                chunk = loop.run_until_complete(
                    generator.__anext__()
                )

                if chunk:
                    yield chunk

            except StopAsyncIteration:

                break

    finally:

        try:

            loop.run_until_complete(
                generator.aclose()
            )

        except Exception:
            pass

        try:

            loop.close()

        except Exception:
            pass


# =========================================================
# /TTS
# =========================================================

@voice_bp.route("/tts", methods=["POST"])
def tts():

    # =====================================================
    # CRONÔMETRO DA REQUEST
    # =====================================================

    inicio_request = time.perf_counter()

    print()
    print("╔" + "═" * 68 + "╗")
    print("║ 🚀 NOVA REQUEST /tts")
    print("╚" + "═" * 68 + "╝")

    # =====================================================
    # RECEBE JSON
    # =====================================================

    dados = request.get_json(silent=True) or {}

    texto = dados.get(
        "text",
        ""
    ).strip()

    print(
        f"📥 JSON recebido em "
        f"{time.perf_counter() - inicio_request:.3f}s"
    )

    if not texto:

        print("❌ Texto vazio.")

        return jsonify({
            "success": False,
            "error": "Texto vazio."
        }), 400

    print("📝 Texto:", texto)

    # =====================================================
    # CRIA STREAM
    # =====================================================

    try:

        stream = gerar_stream(
            texto,
            inicio_request
        )

        response = Response(
            stream_with_context(stream),
            mimetype="audio/mpeg",

            headers={

                "Cache-Control":
                    "no-cache, no-store, must-revalidate",

                "Pragma":
                    "no-cache",

                "Expires":
                    "0",

                "Connection":
                    "keep-alive",

                "X-Accel-Buffering":
                    "no"
            }
        )

        print(
            f"📤 Response criada em "
            f"{time.perf_counter() - inicio_request:.3f}s"
        )

        print(
            "📤 Iniciando streaming..."
        )

        return response

    except Exception as e:

        print(
            "❌ ERRO /tts:",
            repr(e)
        )

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500