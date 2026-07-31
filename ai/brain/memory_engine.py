"""
=========================================
Memory Engine
=========================================
"""

from database import conectar


class MemoryEngine:

    def load(self, usuario):

        conn = conectar()
        cursor = conn.cursor()

        # Últimas conversas
        cursor.execute(
            """
            SELECT mensagem, resposta
            FROM memoria
            WHERE usuario=?
            ORDER BY id DESC
            LIMIT 20
            """,
            (usuario,)
        )

        rows = cursor.fetchall()

        historico = []

        for mensagem, resposta in reversed(rows):

            historico.append({
                "role": "user",
                "content": mensagem
            })

            historico.append({
                "role": "assistant",
                "content": resposta
            })

        conn.close()

        return {

            "history": historico,

            "facts": [],

            "goals": [],

            "preferences": {}

        }

    def save_fact(self, usuario, chave, valor):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO user_facts
            (usuario, chave, valor)
            VALUES (?, ?, ?)
            """,
            (usuario, chave, valor)
        )

        conn.commit()
        conn.close()

    def save_goal(self, usuario, objetivo):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO user_goals
            (usuario, objetivo)
            VALUES (?, ?)
            """,
            (usuario, objetivo)
        )

        conn.commit()
        conn.close()


memory_engine = MemoryEngine()