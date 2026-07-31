"""
====================================================
Services
====================================================
"""

from ai.decision.decision_engine import decision_engine


class Services:

    @property
    def decision(self):

        return decision_engine


services = Services()