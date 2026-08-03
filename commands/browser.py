"""
====================================================
Browser Commands
====================================================
"""

from commands.command import CommandDefinition


BROWSER = [

    # ==========================================
    # ABRIR NAVEGADOR
    # ==========================================

    CommandDefinition(

        name="browser",

        patterns=[

            r"\babra o navegador\b",
            r"\babrir navegador\b",
            r"\babra o chrome\b",
            r"\babrir chrome\b",
            r"\babra a internet\b",
            r"\babrir internet\b"

        ],

        action="OPEN_BROWSER"

    ),

    # ==========================================
    # ABRIR GOOGLE
    # ==========================================

    CommandDefinition(

        name="google",

        patterns=[

            r"\babra o google\b",
            r"\babre o google\b",
            r"\babrir google\b"

        ],

        action="OPEN_GOOGLE"

    ),

    # ==========================================
    # ABRIR YOUTUBE
    # ==========================================

    CommandDefinition(

        name="youtube",

        patterns=[

            r"\babra o youtube\b",
            r"\babre o youtube\b",
            r"\babrir youtube\b"

        ],

        action="OPEN_YOUTUBE"

    )

]