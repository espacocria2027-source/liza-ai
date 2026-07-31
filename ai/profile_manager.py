"""
====================================================
PROFILE MANAGER
====================================================
"""

from dataclasses import dataclass, asdict
import json
import os


PROFILE_DIR = "profiles"

os.makedirs(PROFILE_DIR, exist_ok=True)


@dataclass
class UserProfile:

    short_answers: bool = True

    asks_questions: bool = True

    likes_examples: bool = True

    likes_complete_code: bool = True

    likes_markdown: bool = True

    likes_step_by_step: bool = True

    preferred_language: str = "pt-BR"

    favorite_topics: list = None

    if favorite_topics is None:
        favorite_topics = []


class ProfileManager:

    def _path(self, user):

        return os.path.join(PROFILE_DIR, f"{user}.json")


    def load(self, user):

        path = self._path(user)

        if not os.path.exists(path):

            profile = UserProfile()

            self.save(user, profile)

            return profile

        with open(path, "r", encoding="utf8") as f:

            data = json.load(f)

        return UserProfile(**data)


    def save(self, user, profile):

        with open(self._path(user), "w", encoding="utf8") as f:

            json.dump(
                asdict(profile),
                f,
                ensure_ascii=False,
                indent=4
            )


profile_manager = ProfileManager()