"""
====================================================
Media Commands
====================================================
"""

from commands.command import CommandDefinition


MEDIA = [

    # =====================================================
    # ABRIR SPOTIFY
    # =====================================================

    CommandDefinition(

        name="open_spotify",

        patterns=[

            r"abra o spotify",
            r"abrir spotify",
            r"abre o spotify",
            r"abrir o spotify"

        ],

        action="OPEN_SPOTIFY"

    ),

    # =====================================================
    # TOCAR SPOTIFY
    # =====================================================

    CommandDefinition(

        name="play_spotify",

        patterns=[

            r"toque spotify",
            r"reproduza spotify",
            r"inicie spotify"

        ],

        action="PLAY_SPOTIFY"

    ),

    # =====================================================
    # PLAYLIST
    # =====================================================

    CommandDefinition(

        name="playlist",

        patterns=[

            r"toque a playlist (.+)",
            r"reproduza a playlist (.+)",
            r"abra a playlist (.+)"

        ],

        action="PLAY_PLAYLIST"

    ),

    # =====================================================
    # PAUSAR
    # =====================================================

    CommandDefinition(

        name="pause",

        patterns=[

            r"pause a música",
            r"pausar música",
            r"pare a música"

        ],

        action="PAUSE_SPOTIFY"

    ),

    # =====================================================
    # PRÓXIMA MÚSICA
    # =====================================================

    CommandDefinition(

        name="next",

        patterns=[

            r"próxima música",
            r"proxima música",
            r"próxima faixa",
            r"avançar música"

        ],

        action="NEXT_TRACK"

    ),

    # =====================================================
    # MÚSICA ANTERIOR
    # =====================================================

    CommandDefinition(

        name="previous",

        patterns=[

            r"música anterior",
            r"faixa anterior",
            r"voltar música"

        ],

        action="PREVIOUS_TRACK"

    ),

    # =====================================================
    # TOCAR VÍDEO
    # =====================================================

    CommandDefinition(

        name="play_video",

        patterns=[

            r"toque o vídeo (.+)",
            r"reproduza o vídeo (.+)",
            r"assistir (.+) no youtube"

        ],

        action="PLAY_VIDEO"

    )

]