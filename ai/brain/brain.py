"""
=========================================
L.I.Z.A Brain
=========================================
"""

from ai.brain.context_engine import context_engine
from ai.brain.memory_engine import memory_engine
from ai.brain.reasoning_engine import reasoning_engine
from ai.brain.planner_engine import planner_engine
from ai.brain.execution_manager import execution_manager


class Brain:

    def process(self, usuario, mensagem):

        # ==========================
        # Contexto
        # ==========================

        contexto = context_engine.build(
            usuario,
            mensagem
        )

        # ==========================
        # Memória
        # ==========================

        memoria = memory_engine.load(
            usuario
        )

        # ==========================
        # Raciocínio
        # ==========================

        reasoning = reasoning_engine.think(
            contexto,
            memoria,
            mensagem
        )

        # ==========================
        # Planejamento
        # ==========================

        plan = planner_engine.create(
            reasoning
        )

        # ==========================
        # Execução
        # ==========================

        result = execution_manager.execute(
            usuario,
            plan
        )

        # ==========================
        # Histórico
        # ==========================

        execution_manager.save(
            usuario,
            plan,
            result
        )

        return result


brain = Brain()