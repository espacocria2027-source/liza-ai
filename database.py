import sqlite3

def conectar():
    return sqlite3.connect("liza.db")

def criar_tabela():

    conn = conectar()
    cursor = conn.cursor()

    # Memória
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mensagem TEXT,
        resposta TEXT
    )
    """)

    # Usuários
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE,
        senha TEXT
    )
    """)

    conn.commit()
    conn.close()