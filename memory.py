"""
====================================================
MEMÓRIA DA L.I.Z.A.
====================================================
"""

from database import conectar
from config import MAX_HISTORY


class MemoryManager:

    def __init__(self):
        pass

    # ==========================================
    # CARREGA HISTÓRICO
    # ==========================================

    def load_history(self, usuario):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT mensagem, resposta
            FROM memoria
            WHERE usuario=?
            ORDER BY id DESC
            LIMIT ?
            """,
            (
                usuario,
                MAX_HISTORY
            )
        )

        rows = cursor.fetchall()

        conn.close()

        history = []

        for pergunta, resposta in reversed(rows):

            history.append({
                "role": "user",
                "content": pergunta
            })

            history.append({
                "role": "assistant",
                "content": resposta
            })

        return history

    # ==========================================
    # SALVAR CONVERSA
    # ==========================================

    def save(self, usuario, pergunta, resposta):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO memoria
            (
                usuario,
                mensagem,
                resposta
            )
            VALUES
            (?, ?, ?)
            """,
            (
                usuario,
                pergunta,
                resposta
            )
        )

        conn.commit()

        conn.close()


memory = MemoryManager()