# ====================================================
# L.I.Z.A. — RESEARCH ROUTE
# ====================================================

from flask import (
    Blueprint,
    jsonify,
    request
)

from services.research.research_service import (
    ResearchService
)

from services.research.tavily_search_provider import (
    TavilySearchProvider
)

from services.research.source_scorer import (
    SourceScorer
)

from services.research.answer_synthesizer import (
    AnswerSynthesizer
)

from services.research.evidence_analyzer import (
    EvidenceAnalyzer
)


# ====================================================
# BLUEPRINT
# ====================================================

research_bp = Blueprint(
    "research",
    __name__,
    url_prefix="/pesquisar"
)


# ====================================================
# COMPONENTES
# ====================================================

search_provider = (
    TavilySearchProvider()
)

source_scorer = (
    SourceScorer()
)

answer_synthesizer = (
    AnswerSynthesizer()
)

evidence_analyzer = (
    EvidenceAnalyzer()
)


# ====================================================
# SERVIÇO PRINCIPAL
# ====================================================

research_service = ResearchService(

    search_provider,

    source_scorer,

    answer_synthesizer,

    evidence_analyzer

)


# ====================================================
# PESQUISAR
# ====================================================

@research_bp.post("")
def pesquisar():

    # ================================================
    # RECEBER JSON
    # ================================================

    data = request.get_json(
        silent=True
    )


    if not data:

        return jsonify({

            "success":
                False,

            "error":
                "Corpo da requisição ausente."

        }), 400


    # ================================================
    # CONSULTA
    # ================================================

    query = data.get(
        "query",
        ""
    )


    if not isinstance(
        query,
        str
    ):

        return jsonify({

            "success":
                False,

            "error":
                "A consulta deve ser um texto."

        }), 400


    query = query.strip()


    if not query:

        return jsonify({

            "success":
                False,

            "error":
                "A consulta não pode estar vazia."

        }), 400


    # ================================================
    # PESQUISA
    # ================================================

    try:

        result = (
            research_service.research(
                query
            )
        )


        # ============================================
        # RESPOSTA
        # ============================================

        return jsonify({

            "success":
                True,

            **result

        }), 200


    except ValueError as error:

        print(
            f"⚠ Erro de validação na pesquisa: {error}"
        )


        return jsonify({

            "success":
                False,

            "error":
                str(error)

        }), 400


    except Exception as error:

        print(
            f"❌ Erro na pesquisa: {error}"
        )


        return jsonify({

            "success":
                False,

            "error":
                "Não foi possível realizar "
                "a pesquisa."

        }), 500