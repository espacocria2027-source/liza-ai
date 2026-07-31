"""
=========================================
L.I.Z.A Reasoning Engine V2
=========================================
"""

from ai.providers.model_provider import provider


class ReasoningEngine:

    def think(

        self,

        contexto,

        memoria,

        mensagem

    ):

        prompt = f"""
Você é o cérebro da L.I.Z.A.

Sua função NÃO é responder diretamente.

Sua função é pensar.

===========================
CONTEXTO
===========================

{contexto}

===========================
MEMÓRIA
===========================

{memoria}

===========================
MENSAGEM
===========================

{mensagem}

===========================
OBJETIVO
===========================

Analise a intenção do usuário.

Determine:

1. O objetivo principal.

2. O que ele realmente deseja.

3. Se precisa executar alguma ação.

4. Se precisa pesquisar.

5. Se precisa conversar.

6. Se precisa controlar o Android.

7. Se precisa criar um plano.

8. Quais informações estão faltando.

Responda em formato JSON.

Exemplo:

{{
    "goal":"Abrir Spotify",

    "intent":"action",

    "requires_plan":true,

    "requires_memory":false,

    "requires_android":true,

    "missing_information":[],

    "confidence":0.98
}}

Não converse.

Não explique.

Retorne apenas o JSON.
"""

        resposta = provider.reasoning(

            [

                {

                    "role": "system",

                    "content": "Você é o módulo de raciocínio da L.I.Z.A."

                },

                {

                    "role": "user",

                    "content": prompt

                }

            ]

        )

        return resposta


reasoning_engine = ReasoningEngine()