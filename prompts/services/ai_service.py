from groq import Groq
import os

from prompts.system_prompt import SYSTEM_PROMPT

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def gerar_resposta(mensagem, historico):

    resposta = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }

        ] + historico + [

            {
                "role": "user",
                "content": mensagem
            }

        ]

    )

    return resposta.choices[0].message.content