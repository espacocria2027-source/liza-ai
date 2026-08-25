# ====================================================
# L.I.Z.A. — ANSWER SYNTHESIZER
# ====================================================

import os

from groq import Groq

from services.research.search_provider import (
    SearchResult
)

from services.research.evidence_analyzer import (
    EvidenceAnalysis
)


class AnswerSynthesizer:

    def __init__(
        self,
        api_key: str | None = None
    ):

        self.api_key = (
            api_key
            or os.getenv(
                "GROQ_API_KEY"
            )
        )

        if not self.api_key:

            raise RuntimeError(
                "GROQ_API_KEY não configurada."
            )

        self.client = Groq(
            api_key=self.api_key
        )


    # =================================================
    # SÍNTESE
    # =================================================

    def synthesize(
        self,
        query: str,
        sources: list[SearchResult],
        evidence: EvidenceAnalysis
    ) -> str:

        if not sources:

            return (
                "Não encontrei fontes suficientes "
                "para responder com segurança."
            )


        # =============================================
        # PREPARAR FONTES
        # =============================================

        context = self._build_context(
            sources
        )


        # =============================================
        # PREPARAR EVIDÊNCIAS
        # =============================================

        evidence_context = (
            self._build_evidence_context(
                evidence
            )
        )


        # =============================================
        # ESTRATÉGIA DA RESPOSTA
        # =============================================

        strategy = (
            self._determine_strategy(
                evidence
            )
        )


        # =============================================
        # PROMPT DO SISTEMA
        # =============================================

        system_prompt = """
Você é o mecanismo de síntese da L.I.Z.A.

Sua função é produzir respostas confiáveis
a partir de pesquisas na Web.

Você recebe:

- a pergunta do usuário;
- fontes pesquisadas;
- uma análise de evidências;
- uma confiança estimada;
- possíveis conflitos entre fontes.

Você DEVE respeitar a análise de evidências.

REGRAS:

1. Use as fontes fornecidas como base factual.

2. Não invente informações.

3. Não invente números, datas, versões,
   nomes ou acontecimentos.

4. Não trate todas as fontes como igualmente
   confiáveis.

5. Considere autoridade, relevância e
   atualidade.

6. Se existir conflito, não esconda o conflito.

7. Se existir conflito de versão, data ou
   valor numérico, compare explicitamente
   as informações.

8. Uma fonte secundária nunca deve ser
   apresentada como fonte oficial.

9. Não invente URLs.

10. Use português do Brasil.

11. Seja natural e direto.

12. Use referências [1], [2], [3] etc.

13. Cada referência deve corresponder
    exatamente ao índice da fonte fornecida.

14. Se a confiança for baixa, deixe claro
    que a informação não pode ser confirmada
    com alta segurança.

15. Se a confiança for alta e as fontes forem
    consistentes, responda de forma direta.

16. Se houver conflito, não escolha uma fonte
    simplesmente porque apareceu primeiro.

17. Quando houver uma fonte claramente mais
    apropriada para a pergunta, explique por
    que ela recebeu maior peso.

18. Não transforme uma inferência em fato.

19. Diferencie claramente:
    - fato encontrado nas fontes;
    - interpretação;
    - incerteza.

20. Nunca diga que uma informação é definitiva
    quando as evidências fornecidas não permitem
    essa conclusão.
"""


        # =============================================
        # PROMPT DA PERGUNTA
        # =============================================

        user_prompt = f"""
PERGUNTA DO USUÁRIO:

{query}


ESTRATÉGIA OBRIGATÓRIA:

{strategy}


ANÁLISE DAS EVIDÊNCIAS:

{evidence_context}


FONTES:

{context}


TAREFA:

Responda à pergunta usando as fontes e a
análise de evidências.

A resposta deve refletir a confiança e o
tipo de conflito detectado.

Use [1], [2], [3] etc. para indicar as fontes
quando apropriado.
"""


        # =============================================
        # GROQ
        # =============================================

        response = self.client.chat.completions.create(

            model="openai/gpt-oss-120b",

            temperature=0.1,

            max_tokens=1400,

            messages=[

                {
                    "role":
                        "system",

                    "content":
                        system_prompt
                },

                {
                    "role":
                        "user",

                    "content":
                        user_prompt
                }

            ]

        )


        # =============================================
        # RESPOSTA
        # =============================================

        answer = (
            response
            .choices[0]
            .message
            .content
        )


        if not answer:

            return (
                "Não foi possível gerar uma "
                "resposta baseada nas fontes."
            )


        return answer.strip()


    # =================================================
    # ESTRATÉGIA
    # =================================================

    @staticmethod
    def _determine_strategy(
        evidence: EvidenceAnalysis
    ) -> str:

        confidence = (
            evidence.confidence
        )

        conflict = (
            evidence.has_conflict
        )

        conflict_type = (
            evidence.conflict_type
        )


        # =============================================
        # CONFLITO DE VERSÃO
        # =============================================

        if (
            conflict
            and
            conflict_type == "VERSION"
        ):

            return """
Existe conflito entre versões.

A resposta deve:

1. identificar as versões encontradas;
2. informar quais fontes apresentam cada versão;
3. considerar a autoridade das fontes;
4. considerar a atualidade das informações;
5. evitar afirmar que uma versão é a mais
   recente sem evidência suficiente;
6. apresentar claramente a versão escolhida
   e o motivo da escolha.
"""


        # =============================================
        # CONFLITO DE DATA
        # =============================================

        if (
            conflict
            and
            conflict_type == "DATE"
        ):

            return """
Existe conflito entre datas.

A resposta deve:

1. apresentar as datas relevantes;
2. relacionar cada data à sua fonte;
3. considerar a data mais recente quando
   a pergunta exigir atualidade;
4. explicar qualquer diferença de contexto;
5. não escolher uma data arbitrariamente.
"""


        # =============================================
        # CONFLITO NUMÉRICO
        # =============================================

        if (
            conflict
            and
            conflict_type == "NUMERIC"
        ):

            return """
Existe conflito entre valores numéricos.

A resposta deve:

1. apresentar os valores encontrados;
2. indicar suas respectivas fontes;
3. verificar se os valores podem representar
   contextos diferentes;
4. não calcular ou inventar uma média;
5. explicar qual valor possui melhor evidência,
   se isso puder ser determinado.
"""


        # =============================================
        # QUALQUER OUTRO CONFLITO
        # =============================================

        if conflict:

            return """
Existem informações potencialmente conflitantes.

Compare as fontes explicitamente.

Não esconda a divergência.

Dê preferência à evidência mais forte,
mas explique a razão dessa preferência.

Se não for possível resolver o conflito,
declare a incerteza.
"""


        # =============================================
        # CONFIANÇA ALTA
        # =============================================

        if confidence >= 0.85:

            return """
A confiança estimada é alta.

As fontes não apresentam conflito relevante.

Responda diretamente, usando as melhores
fontes como base e citando-as quando necessário.
"""


        # =============================================
        # CONFIANÇA MÉDIA
        # =============================================

        if confidence >= 0.65:

            return """
A confiança estimada é moderada.

Responda normalmente, mas evite afirmações
excessivamente definitivas.

Quando relevante, indique que a informação
foi encontrada nas fontes pesquisadas.
"""


        # =============================================
        # CONFIANÇA BAIXA
        # =============================================

        return """
A confiança estimada é baixa.

Seja especialmente cauteloso.

Não apresente a informação como definitiva.

Explique que as fontes disponíveis não são
suficientes para confirmar a resposta com
alta segurança.
"""


    # =================================================
    # CONTEXTO DAS FONTES
    # =================================================

    @staticmethod
    def _build_context(
        sources: list[SearchResult]
    ) -> str:

        blocks = []


        for index, source in enumerate(
            sources,
            start=1
        ):

            blocks.append(

                f"""
[ FONTE {index} ]

Título:
{source.title}

Domínio:
{source.domain}

URL:
{source.url}

Score do provedor:
{source.provider_score}

Conteúdo:
{source.snippet}
"""
            )


        return "\n".join(
            blocks
        )


    # =================================================
    # CONTEXTO DAS EVIDÊNCIAS
    # =================================================

    @staticmethod
    def _build_evidence_context(
        evidence: EvidenceAnalysis
    ) -> str:

        preferred = ", ".join(

            f"[{index}]"

            for index
            in evidence.preferred_sources

        )


        if not preferred:

            preferred = (
                "Nenhuma fonte preferencial definida."
            )


        if evidence.has_conflict:

            conflict_status = (
                "SIM"
            )

        else:

            conflict_status = (
                "NÃO"
            )


        conflict_type = (

            evidence.conflict_type

            if evidence.conflict_type

            else

            "NENHUM"

        )


        return f"""
Confiança estimada:
{evidence.confidence:.2f}

Conflito detectado:
{conflict_status}

Tipo de conflito:
{conflict_type}

Fontes preferenciais:
{preferred}

Justificativa:
{evidence.reason}
"""