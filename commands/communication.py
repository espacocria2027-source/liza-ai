from commands.command import CommandDefinition

COMMUNICATION = [

    CommandDefinition(

        name="whatsapp",

        patterns=[

            r"\babra o whatsapp\b",
            r"\babrir whatsapp\b"

        ],

        action="OPEN_WHATSAPP"

    ),

    CommandDefinition(

        name="telegram",

        patterns=[

            r"\babra o telegram\b"

        ],

        action="OPEN_TELEGRAM"

    )

]