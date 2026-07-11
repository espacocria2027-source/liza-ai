import pyttsx3
import webbrowser
import os
import ollama
import pyautogui

# =========================
# CONFIGURAÇÕES
# =========================

humor = "feliz"
arquivo_memoria = "memoria.txt"

# =========================
# VOZ
# =========================

engine = pyttsx3.init()

def falar(texto):
    print("L.I.Z.A:", texto)
    engine.say(texto)
    engine.runAndWait()

# =========================
# MEMÓRIA
# =========================

def salvar_memoria(texto):
    with open(arquivo_memoria, "a", encoding="utf-8") as arquivo:
        arquivo.write(texto + "\n")

def ler_memoria():
    try:
        with open(arquivo_memoria, "r", encoding="utf-8") as arquivo:
            return arquivo.read()
    except:
        return "Memória vazia"

# =========================
# IA
# =========================

def perguntar_ia(pergunta):

    memoria = ler_memoria()

    prompt_sistema = f"""
Você é L.I.Z.A.

Uma inteligência artificial feminina.

Você fala português do Brasil.

Seu humor atual é: {humor}

Você é amigável, inteligente e prestativa.

Memórias do usuário:

{memoria}

Use essas informações quando forem úteis.
"""

    resposta = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": prompt_sistema
            },
            {
                "role": "user",
                "content": pergunta
            }
        ]
    )

    return resposta["message"]["content"]

# =========================
# COMANDOS
# =========================

def executar_comando(comando):

    global humor

    comando = comando.lower()

    if comando.startswith("lembrar"):

        memoria = comando.replace("lembrar", "").strip()

        salvar_memoria(memoria)

        falar(f"Vou lembrar que {memoria}")

    elif "memória" in comando:

        falar(ler_memoria())

    elif comando == "youtube":

        falar("Abrindo YouTube")

        webbrowser.open("https://youtube.com")

    elif comando == "google":

        falar("Abrindo Google")

        webbrowser.open("https://google.com")

    elif comando.startswith("pesquisar"):

        pesquisa = comando.replace("pesquisar", "").strip()

        falar(f"Pesquisando {pesquisa}")

        webbrowser.open(
            f"https://www.google.com/search?q={pesquisa}"
        )

    elif "bloco de notas" in comando:

        falar("Abrindo bloco de notas")

        os.system("notepad")

    elif "menu windows" in comando:

        falar("Abrindo menu windows")

        pyautogui.hotkey("ctrl", "esc")

    elif "fechar janela" in comando:

        falar("Fechando janela")

        pyautogui.hotkey("alt", "f4")

    elif comando.startswith("escrever"):

        texto = comando.replace("escrever", "").strip()

        falar("Escrevendo")

        pyautogui.write(texto)

    elif comando == "enter":

        falar("Pressionando enter")

        pyautogui.press("enter")

    elif "print" in comando:

        falar("Função de print desativada temporariamente")

    elif "modo feliz" in comando:

        humor = "feliz"

        falar("Agora estou feliz")

    elif "modo sério" in comando:

        humor = "sério"

        falar("Agora estou mais séria")

    elif "modo engraçado" in comando:

        humor = "engraçado"

        falar("Agora estou divertida")

    elif "sair" in comando:

        falar("Encerrando sistema")

        exit()

    else:

        resposta = perguntar_ia(comando)

        falar(resposta)

# =========================
# INICIAR
# =========================

falar("L I Z A iniciada")

# =========================
# LOOP PRINCIPAL
# =========================

while True:

    comando = input("Você: ")

    executar_comando(comando)