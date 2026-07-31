"""
=========================================
L.I.Z.A Execution Manager
=========================================
"""

import json

from database import conectar


class ExecutionManager:

    def execute(self, usuario, plan):

        executed = []

        success = True

        for step in plan.steps:

            executed.append({

                "action": step.action,

                "parameters": step.parameters,

                "status": "pending"

            })

        return {

            "type": "execution",

            "message": plan.message,

            "steps": executed,

            "success": success

        }

    def save(

        self,

        usuario,

        plan,

        result

    ):

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute(

            """
            INSERT INTO action_history(

                usuario,

                acao,

                parametros,

                sucesso

            )

            VALUES(?,?,?,?)
            """,

            (

                usuario,

                plan.goal,

                json.dumps(result),

                1

            )

        )

        conn.commit()

        conn.close()


execution_manager = ExecutionManager()