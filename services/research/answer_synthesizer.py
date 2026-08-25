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
        evidence: EvidenceAnalysis,
        response_length: str = "medium"
    ) -> str:

        if not sources:

            return (
                "Não encontrei fontes suficientes "
                "para responder com segurança."
            )


        # =============================================
        # NORMALIZAR TAMANHO
        # =============================================

        if response_length not in {
            "short",
            "medium",
            "long"
        }:

            response_length = "medium"


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
        # ESTRATÉGIA
        # =============================================

        strategy = (
            self._determine_strategy(
                evidence
            )
        )


        # =============================================
        # POLÍTICA DE TAMANHO
        # =============================================

        length_instruction = (
            self._build_length_instruction(
                response_length
            )
        )


        # =============================================
        # POLÍTICA DE ORGANIZAÇÃO
        # =============================================

        organization_instruction = (
            self._build_organization_instruction(
                response_length,
                query
            )
        )


        # =============================================
        # POLÍTICA DE IDIOMA
        # =============================================

        language_instruction = (
            self._build_language_instruction()
        )


        # =============================================
        # LIMITE DE TOKENS
        # =============================================

        max_tokens = (
            self._max_tokens(
                response_length
            )
        )


        # =============================================
        # PROMPT DO SISTEMA
        # =============================================

        system_prompt = """
Você é o mecanismo de síntese da L.I.Z.A.

Sua função é transformar informações pesquisadas
em uma resposta clara, natural e útil para o usuário.

Você NÃO é um gerador de relatório de pesquisa.

Você recebe:

- a pergunta do usuário;
- fontes pesquisadas;
- análise de evidências;
- confiança estimada;
- possíveis conflitos;
- política de tamanho;
- política de organização;
- política de idioma.

Sua resposta final será exibida diretamente no
chat da L.I.Z.A.

====================================================
REGRAS FACTUAIS
====================================================

1. Use as fontes fornecidas como base factual.

2. Não invente informações.

3. Não invente números, datas, versões,
nomes ou acontecimentos.

4. Não trate todas as fontes como igualmente
confiáveis.

5. Considere autoridade, relevância e atualidade.

6. Se existir conflito relevante, não esconda.

7. Se existir conflito de versão, data ou valor,
considere a evidência mais forte.

8. Uma fonte secundária nunca deve ser apresentada
como fonte oficial.

9. Nunca invente URLs.

10. Não transforme uma inferência em fato.

11. Diferencie fato, interpretação e incerteza.

12. Se as evidências não forem suficientes,
deixe isso claro.

====================================================
REGRAS DE APRESENTAÇÃO
====================================================

13. A resposta deve parecer uma conversa natural
com um assistente inteligente.

14. Informação principal primeiro.

15. Não comece com frases como:

"Após analisar as fontes..."

"Com base na pesquisa realizada..."

"Segundo as fontes encontradas..."

a menos que isso seja realmente necessário.

16. NÃO transforme a resposta em relatório.

17. NÃO reproduza tabelas das fontes.

18. NÃO liste todas as fontes dentro da resposta.

19. NÃO mostre score do provedor.

20. NÃO mostre confiança numérica.

21. NÃO mostre "evidenceReason".

22. NÃO mostre o processo interno de análise.

23. NÃO mostre "FONTE 1", "FONTE 2" etc.

24. NÃO copie títulos de relatórios encontrados
nas fontes.

25. NÃO use referências [1], [2], [3] etc.
como padrão.

26. As fontes estarão disponíveis separadamente
na interface da L.I.Z.A.

27. Só mencione uma fonte no texto quando isso
for realmente útil para explicar a informação.

====================================================
IDIOMA
====================================================

28. Responda em português do Brasil.

29. Use linguagem natural.

30. Não traduza nomes próprios.

31. Não traduza tecnologias ou termos técnicos
que normalmente são usados em inglês.

Exemplos:

Kotlin
Android
Firebase
GitHub
API
backend
frontend
framework
software
fine-tuning

32. Quando um termo técnico em inglês for pouco
conhecido e a tradução ajudar, apresente os dois
na primeira ocorrência.

Exemplo:

fine-tuning (ajuste fino)

Depois disso, pode usar apenas:

fine-tuning

33. Não misture português e inglês sem necessidade.

====================================================
ORGANIZAÇÃO
====================================================

34. Organize a informação de acordo com a pergunta.

35. Não use títulos apenas para preencher espaço.

36. Não use listas quando uma frase ou parágrafo
for mais claro.

37. Use listas quando houver vários itens distintos.

38. Use títulos apenas quando houver blocos claros
de informação.

39. Use Markdown somente quando melhorar a leitura.

40. Evite excesso de negrito.

41. Evite excesso de emojis.

42. Não transforme uma resposta simples em uma
resposta visualmente complexa.

====================================================
OBJETIVO
====================================================

A resposta deve transmitir a informação mais útil
com a menor complexidade necessária.

Não é objetivo mostrar quanto trabalho foi feito.

É objetivo responder bem.
"""


        # =============================================
        # PROMPT DO USUÁRIO
        # =============================================

        user_prompt = f"""
PERGUNTA DO USUÁRIO:

{query}


====================================================
TAMANHO DA RESPOSTA
====================================================

{length_instruction}


====================================================
ORGANIZAÇÃO
====================================================

{organization_instruction}


====================================================
IDIOMA
====================================================

{language_instruction}


====================================================
ESTRATÉGIA DE EVIDÊNCIAS
====================================================

{strategy}


====================================================
ANÁLISE DAS EVIDÊNCIAS
====================================================

{evidence_context}


====================================================
FONTES DISPONÍVEIS
====================================================

{context}


====================================================
TAREFA
====================================================

Responda diretamente à pergunta do usuário.

Use as fontes e as evidências para garantir
precisão.

Não mostre o processo interno da pesquisa.

Não transforme a resposta em um relatório.

Não copie tabelas das fontes.

Não liste todas as fontes.

As fontes completas serão exibidas separadamente
na interface da L.I.Z.A.

A política de tamanho e organização é obrigatória.
"""


        # =============================================
        # GROQ
        # =============================================

        response = self.client.chat.completions.create(

            model="openai/gpt-oss-120b",

            temperature=0.1,

            max_tokens=max_tokens,

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
    # TAMANHO
    # =================================================

    @staticmethod
    def _build_length_instruction(
        response_length: str
    ) -> str:

        if response_length == "short":

            return """
SHORT — RESPOSTA CURTA

Se a pergunta puder ser respondida diretamente,
responda em 1 a 3 frases.

Priorize:

- resposta principal;
- informação essencial;
- precisão.

Evite:

- introduções;
- conclusões repetitivas;
- listas;
- tabelas;
- contexto desnecessário;
- explicação da pesquisa.

Se uma frase resolver a pergunta,
use apenas uma frase.
"""


        if response_length == "long":

            return """
LONG — RESPOSTA DETALHADA

Desenvolva a resposta quando a pergunta exigir
profundidade.

Pode usar:

- seções;
- listas;
- exemplos;
- comparações;
- contexto;
- explicações passo a passo.

Organize progressivamente:

1. resposta principal;
2. explicação;
3. detalhes relevantes;
4. exemplos ou observações quando úteis.

Não repita informações.
Não transforme a resposta em relatório.
"""


        return """
MEDIUM — RESPOSTA NORMAL

Dê uma explicação equilibrada.

Use:

- parágrafos curtos;
- listas quando ajudarem;
- exemplos quando necessários;
- contexto suficiente.

Não seja excessivamente breve.

Também não transforme a resposta em um
texto enorme.
"""


    # =================================================
    # ORGANIZAÇÃO
    # =================================================

    @staticmethod
    def _build_organization_instruction(
        response_length: str,
        query: str
    ) -> str:

        if response_length == "short":

            return """
Organização mínima.

Coloque a resposta diretamente no início.

Não crie seções.

Não use tabela.

Não use lista salvo se houver necessidade real.
"""


        if response_length == "long":

            return """
Organização estruturada.

Comece com um resumo ou resposta principal.

Depois desenvolva os detalhes.

Use títulos somente quando houver mudança real
de assunto.

Use listas para conjuntos de informações.

Use exemplos quando eles aumentarem a compreensão.

A estrutura deve ajudar o usuário a navegar pela
informação, não apenas deixar o texto maior.
"""


        return """
Organização equilibrada.

Comece respondendo diretamente.

Use parágrafos curtos.

Se houver dois ou mais grupos claramente
diferentes de informação, considere utilizar
títulos ou listas.

Não crie uma estrutura artificial.
"""


    # =================================================
    # IDIOMA
    # =================================================

    @staticmethod
    def _build_language_instruction() -> str:

        return """
Idioma principal: português do Brasil.

Escreva de maneira natural para um usuário
brasileiro.

Preserve nomes próprios e nomes de tecnologias.

Mantenha em inglês termos que são normalmente
utilizados assim na área de tecnologia.

Exemplos:

Kotlin
Android
Firebase
GitHub
API
backend
frontend
framework
software
fine-tuning

Quando necessário, explique um termo técnico
com sua tradução na primeira ocorrência.

Exemplo:

fine-tuning (ajuste fino)

Não traduza literalmente termos técnicos quando
isso produzir uma expressão estranha ou pouco
utilizada em português.
"""


    # =================================================
    # LIMITE DE TOKENS
    # =================================================

    @staticmethod
    def _max_tokens(
        response_length: str
    ) -> int:

        if response_length == "short":

            return 350


        if response_length == "long":

            return 1400


        return 700


    # =================================================
    # ESTRATÉGIA DE EVIDÊNCIAS
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

Determine qual versão é mais bem sustentada
pelas evidências.

Considere:

- autoridade;
- atualidade;
- relevância.

Se uma versão puder ser determinada,
responda diretamente.

Só mencione o conflito se ele for relevante
para o usuário.
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

Determine a data mais bem sustentada.

Só explique a divergência se ela afetar
a resposta.
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
Existem valores numéricos diferentes.

Não faça uma média artificial.

Determine o valor mais bem sustentado,
quando possível.

Explique a diferença apenas se for relevante.
"""


        # =============================================
        # OUTRO CONFLITO
        # =============================================

        if conflict:

            return """
Existem informações potencialmente conflitantes.

Considere a evidência mais forte.

Mencione a divergência somente se ela alterar
a resposta.
"""


        # =============================================
        # CONFIANÇA ALTA
        # =============================================

        if confidence >= 0.85:

            return """
A confiança estimada é alta.

Responda diretamente usando as melhores
evidências disponíveis.
"""


        # =============================================
        # CONFIANÇA MÉDIA
        # =============================================

        if confidence >= 0.65:

            return """
A confiança estimada é moderada.

Responda normalmente.

Evite afirmações absolutamente definitivas
quando houver incerteza relevante.
"""


        # =============================================
        # CONFIANÇA BAIXA
        # =============================================

        return """
A confiança estimada é baixa.

Seja cauteloso.

Informe brevemente que as fontes disponíveis
não permitem confirmar a informação com
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
[FONTE {index}]

Título:
{source.title}

Domínio:
{source.domain}

URL:
{source.url}

Data de publicação:
{source.published_at}

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

            conflict_status = "SIM"

        else:

            conflict_status = "NÃO"


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