from database import conectar


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

MAX_MEMORY_MESSAGES = 6


# ==========================================================
# CARREGAR MEMÓRIA
# ==========================================================

def carregar_memoria(usuario):

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
            MAX_MEMORY_MESSAGES
        )
    )

    rows = cursor.fetchall()

    conn.close()

    historico = []

    for pergunta, resposta in reversed(rows):

        historico.append({
            "role": "user",
            "content": pergunta
        })

        historico.append({
            "role": "assistant",
            "content": resposta
        })

    return historico


# ==========================================================
# SALVAR MEMÓRIA
# ==========================================================

def salvar_memoria(
    usuario,
    mensagem,
    resposta
):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO memoria
        (usuario, mensagem, resposta)
        VALUES (?, ?, ?)
        """,
        (
            usuario,
            mensagem,
            resposta
        )
    )

    conn.commit()

    conn.close()