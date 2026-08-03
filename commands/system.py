from commands.command import CommandDefinition

SYSTEM = [

    CommandDefinition(

        name="settings",

        patterns=[

            r"\babra as configurações\b",
            r"\babrir configurações\b"

        ],

        action="OPEN_SETTINGS"

    ),

    CommandDefinition(

        name="calculator",

        patterns=[

            r"\babra a calculadora\b"

        ],

        action="OPEN_CALCULATOR"

    ),

    CommandDefinition(

        name="clock",

        patterns=[

            r"\babra o relógio\b",
            r"\babra o relogio\b"

        ],

        action="OPEN_CLOCK"

    )

]