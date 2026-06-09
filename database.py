import sqlite3

def conectar():
    return sqlite3.connect("liza.db")

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        mensagem TEXT,
        resposta TEXT
    )
    """)

    conn.commit()
    conn.close()