# =========================
# MEMÓRIA DA L.I.Z.A
# =========================

ARQUIVO_MEMORIA = "memoria.txt"

def salvar_memoria(texto):

    with open(ARQUIVO_MEMORIA, "a", encoding="utf-8") as arquivo:

        arquivo.write(texto + "\n")

def ler_memoria():

    try:

        with open(ARQUIVO_MEMORIA, "r", encoding="utf-8") as arquivo:

            return arquivo.read()

    except FileNotFoundError:

        return ""

def limpar_memoria():

    with open(ARQUIVO_MEMORIA, "w", encoding="utf-8") as arquivo:

        arquivo.write("")