"""
=========================================
L.I.Z.A. CORE
=========================================
"""

from core.context_manager import ContextManager
from core.session_manager import SessionManager
from core.task_manager import TaskManager
from core.response_manager import ResponseManager

from ai.conversation_service import conversation

from ai.actions.action_manager import action_manager


class LizaCore:

    def __init__(self):

        self.context = ContextManager()

        self.sessions = SessionManager()

        self.tasks = TaskManager()

        self.responses = ResponseManager()

    def process(

        self,

        usuario,

        message

    ):

        session = self.sessions.get(usuario)

        self.context.update(

            usuario,

            message

        )

        result = action_manager.execute(

            usuario,

            message

        )

        if result["action"] != "chat":

            return self.responses.action(result)

        chat = conversation.chat(

            usuario,

            message

        )

        return self.responses.chat(chat)


liza = LizaCore()