"""
==========================================
Goal Manager
==========================================
"""

class GoalManager:

    def create(self, usuario, mensagem):

        return {

            "objective": mensagem,

            "priority": "normal",

            "deadline": None,

            "constraints": []

        }


goal_manager = GoalManager()