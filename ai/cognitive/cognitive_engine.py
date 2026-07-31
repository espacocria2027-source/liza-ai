"""
====================================================
L.I.Z.A Cognitive Engine
====================================================
"""

from core.context_manager import context_manager

from ai.cognitive.goal_manager import goal_manager
from ai.cognitive.reasoning_engine import reasoning
from ai.cognitive.validator import validator
from ai.cognitive.optimizer import optimizer

from ai.workflow.ai_workflow_planner import ai_workflow_planner


class CognitiveEngine:

    def plan(self, usuario: str, mensagem: str):
        """
        Planeja uma tarefa utilizando contexto,
        objetivo, raciocínio e IA.
        """

        # ==========================
        # CONTEXTO
        # ==========================

        contexto = context_manager.build(usuario)

        # ==========================
        # OBJETIVO
        # ==========================

        goal = goal_manager.create(
            usuario,
            mensagem
        )

        # ==========================
        # RACIOCÍNIO
        # ==========================

        reasoning_result = reasoning.think(
            goal,
            contexto
        )

        # ==========================
        # PLANNER IA
        # ==========================

        workflow = ai_workflow_planner.create(
            mensagem
        )

        # ==========================
        # VALIDAÇÃO
        # ==========================

        workflow = validator.validate(
            workflow
        )

        # ==========================
        # OTIMIZAÇÃO
        # ==========================

        workflow = optimizer.optimize(
            workflow
        )

        return workflow


cognitive = CognitiveEngine()