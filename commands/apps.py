from commands.command import CommandDefinition

APPS = [

    CommandDefinition(

        name="youtube",

        patterns=[

            r"\babra o youtube\b",
            r"\babre o youtube\b",
            r"\babrir youtube\b"

        ],

        action="OPEN_YOUTUBE"

    ),

    CommandDefinition(

        name="google",

        patterns=[

            r"\babra o google\b",
            r"\babre o google\b",
            r"\babrir google\b"

        ],

        action="OPEN_GOOGLE"

    ),

    CommandDefinition(

        name="spotify",

        patterns=[

            r"\babra o spotify\b",
            r"\babre o spotify\b",
            r"\babrir spotify\b"

        ],

        action="OPEN_SPOTIFY"

    ),

    CommandDefinition(

        name="play_store",

        patterns=[

            r"\babra a play store\b",
            r"\babrir play store\b"

        ],

        action="OPEN_PLAY_STORE"

    ),

    CommandDefinition(

        name="gmail",

        patterns=[

            r"\babra o gmail\b",
            r"\babrir gmail\b"

        ],

        action="OPEN_GMAIL"

    )

]