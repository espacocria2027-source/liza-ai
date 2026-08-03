"""
====================================================
Search Commands
====================================================
"""

from commands.command import CommandDefinition


SEARCH = [

    # =====================================================
    # PESQUISA GOOGLE
    # =====================================================

    CommandDefinition(

        name="google_search",

        patterns=[

            r"pesquise (.+) no google",
            r"procure (.+) no google",
            r"buscar (.+) no google",
            r"pesquisa (.+) no google"

        ],

        action="GOOGLE_SEARCH"

    ),

    # =====================================================
    # PESQUISA YOUTUBE
    # =====================================================

    CommandDefinition(

        name="youtube_search",

        patterns=[

            r"pesquise (.+) no youtube",
            r"procure (.+) no youtube",
            r"buscar (.+) no youtube",
            r"pesquisa (.+) no youtube"

        ],

        action="YOUTUBE_SEARCH"

    ),

    # =====================================================
    # REPRODUZIR VÍDEO
    # =====================================================

    CommandDefinition(

        name="play_video",

        patterns=[

            r"toque (.+) no youtube",
            r"reproduza (.+) no youtube",
            r"abra o vídeo (.+)"

        ],

        action="PLAY_VIDEO"

    )

]