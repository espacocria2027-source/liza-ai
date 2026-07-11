from groq import Groq
import os
import base64

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analisar_imagem_bytes(conteudo: bytes):

    imagem_base64 = base64.b64encode(
        conteudo
    ).decode("utf-8")

    resposta = client.chat.completions.create(

        model="meta-llama/llama-4-scout-17b-16e-instruct",

        messages=[

            {
                "role": "user",

                "content": [

                    {
                        "type": "text",

                        "text": """
Você é L.I.Z.A.

Analise cuidadosamente esta imagem.

Descreva primeiro o que você observa.

Depois explique os detalhes importantes.

Caso exista texto na imagem, leia-o.

Caso exista programação, explique o código.

Caso exista um documento, faça um resumo.

Fale naturalmente em português do Brasil.

Nunca responda como um robô.

Nunca diga que é um modelo de linguagem.
"""
                    },

                    {
                        "type": "image_url",

                        "image_url": {
                            "url": f"data:image/jpeg;base64,{imagem_base64}"
                        }

                    }

                ]

            }

        ]

    )

    return resposta.choices[0].message.content