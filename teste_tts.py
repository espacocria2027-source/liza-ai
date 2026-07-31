import asyncio
import edge_tts

async def main():
    communicate = edge_tts.Communicate(
        text="Olá Beto, eu sou a L I Z A. Estou pronta para ajudar você.",
        voice="pt-BR-FranciscaNeural"
    )

    await communicate.save("liza.mp3")
    print("Áudio gerado com sucesso!")

asyncio.run(main())