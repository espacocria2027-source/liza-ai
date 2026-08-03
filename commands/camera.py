from commands.command import CommandDefinition

CAMERA = [

    CommandDefinition(

        name="camera",

        patterns=[

            r"\babra a câmera\b",
            r"\babrir câmera\b",
            r"\babra a camera\b"

        ],

        action="OPEN_CAMERA"

    ),

    CommandDefinition(

        name="photo",

        patterns=[

            r"\btire uma foto\b",
            r"\bfotografe\b"

        ],

        action="TAKE_PHOTO"

    )

]