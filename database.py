import sqlite3


DATABASE = "liza.db"


def conectar():
    return sqlite3.connect(DATABASE)


def criar_tabela():

    conn = conectar()
    cursor = conn.cursor()

    # ===========================
    # Usuários
    # ===========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        usuario TEXT UNIQUE,

        senha TEXT

    )
    """)

    # ===========================
    # Histórico de Conversas
    # ===========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memoria (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        usuario TEXT,

        mensagem TEXT,

        resposta TEXT,

        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ===========================
    # Notas
    # ===========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notas (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        usuario TEXT,

        texto TEXT,

        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ===========================
    # Fatos do usuário
    # ===========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_facts (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        usuario TEXT,

        chave TEXT,

        valor TEXT,

        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ===========================
    # Objetivos
    # ===========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_goals (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        usuario TEXT,

        objetivo TEXT,

        status TEXT DEFAULT 'ativo',

        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ===========================
    # Preferências
    # ===========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_preferences (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        usuario TEXT,

        chave TEXT,

        valor TEXT

    )
    """)

    # ===========================
    # Tarefas
    # ===========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        usuario TEXT,

        titulo TEXT,

        descricao TEXT,

        status TEXT,

        prioridade INTEGER,

        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ===========================
    # Ações Executadas
    # ===========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS action_history (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        usuario TEXT,

        acao TEXT,

        parametros TEXT,

        sucesso INTEGER,

        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()