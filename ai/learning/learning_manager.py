"""
====================================================
LEARNING MANAGER
====================================================
"""

import json
import os


FACTS_FILE = "ai/learning/facts.json"


class LearningManager:

    def __init__(self):

        os.makedirs("ai/learning", exist_ok=True)

        if not os.path.exists(FACTS_FILE):

            with open(FACTS_FILE, "w", encoding="utf8") as f:

                json.dump({}, f)

    def load(self):

        with open(FACTS_FILE, "r", encoding="utf8") as f:

            return json.load(f)

    def save(self, data):

        with open(FACTS_FILE, "w", encoding="utf8") as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )

    def get_user(self, usuario):

        data = self.load()

        if usuario not in data:

            data[usuario] = []

            self.save(data)

        return data[usuario]

    def add_fact(self, usuario, fact):

        fact = fact.strip()

        if not fact:

            return

        data = self.load()

        if usuario not in data:

            data[usuario] = []

        if fact not in data[usuario]:

            data[usuario].append(fact)

            self.save(data)


learning = LearningManager()