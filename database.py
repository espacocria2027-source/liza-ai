import sqlite3

def conectar():
    return sqlite3.connect("liza.db")


def criar_tabela():

    conn = conectar()
    cursor = conn.cursor()

    # usuários
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE,
        senha TEXT
    )
    """)

    # memória
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        mensagem TEXT,
        resposta TEXT
    )
    """)

    # notas (ELITE 3)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        texto TEXT
    )
    """)

    conn.commit()
    conn.close()