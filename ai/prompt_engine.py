"""
==========================================
PROMPT ENGINE
==========================================
"""

from pathlib import Path


PROMPTS = Path(__file__).parent / "prompts"


class PromptEngine:

    def __init__(self):

        self.cache = {}

    def load(self, file):

        if file in self.cache:
            return self.cache[file]

        text = (PROMPTS / file).read_text(
            encoding="utf8"
        )

        self.cache[file] = text

        return text

    def detect_modules(self, message):

        text = message.lower()

        modules = [

            "identity.txt",

            "personality.txt",

            "conversation.txt",

            "reasoning.txt",

            "memory.txt",

            "learning.txt",

            "formatting.txt",

            "safety.txt",

            "humor.txt",

            "final_rules.txt"

        ]

        programming = [

            "python",

            "kotlin",

            "java",

            "javascript",

            "html",

            "css",

            "sql",

            "api",

            "erro",

            "bug",

            "código",

            "codigo"

        ]

        android = [

            "android",

            "compose",

            "jetpack",

            "firebase",

            "activity",

            "fragment"

        ]

        web = [

            "html",

            "css",

            "javascript",

            "site",

            "landing",

            "responsivo"

        ]

        image = [

            "imagem",

            "foto",

            "print",

            "screenshot"

        ]

        if any(word in text for word in programming):

            modules.append("programming.txt")

            modules.append("python.txt")

        if any(word in text for word in android):

            modules.append("android.txt")

        if any(word in text for word in web):

            modules.append("web.txt")

        if any(word in text for word in image):

            modules.append("images.txt")

        return modules

    def build(self, message):

        prompt = []

        for module in self.detect_modules(message):

            prompt.append(

                self.load(module)

            )

        return "\n\n".join(prompt)


engine = PromptEngine()