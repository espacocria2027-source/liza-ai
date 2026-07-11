import asyncio
import edge_tts


async def gerar_audio_async(texto: str, arquivo: str = "liza.mp3"):

    communicate = edge_tts.Communicate(
        text=texto,
        voice="pt-BR-FranciscaNeural"
    )

    await communicate.save(arquivo)

    return arquivo


def gerar_audio(texto: str, arquivo: str = "liza.mp3"):

    asyncio.run(
        gerar_audio_async(texto, arquivo)
    )

    return arquivo