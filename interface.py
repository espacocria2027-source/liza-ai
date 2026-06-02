import customtkinter as ctk
import ollama
import pyttsx3
import webbrowser
import os
import json
import queue
import sounddevice as sd

from vosk import Model, KaldiRecognizer
from memoria import salvar_memoria, ler_memoria

# =========================
# CONFIG
# =========================

humor = "feliz"

# =========================
# VOZ
# =========================

engine = pyttsx3.init()

def falar(texto):
    try:
        engine.say(texto)
        engine.runAndWait()
    except:
        pass

# =========================
# MICROFONE
# =========================

modelo = Model("vosk-model-small-pt-0.3")
recognizer = KaldiRecognizer(modelo, 16000)
q = queue.Queue()

def ouvir_microfone():

    try:

        def callback(indata, frames, time, status):
            q.put(indata.copy())

        falar("Estou ouvindo")

        # pega primeiro microfone válido
        mic = None

        devices = sd.query_devices()

        for i, d in enumerate(devices):
            if d["max_input_channels"] > 0:
                mic = i
                break

        if mic is None:
            chat.insert("end", "Nenhum microfone encontrado\n\n")
            return

        with sd.InputStream(
            device=mic,
            samplerate=16000,
            channels=1,
            dtype="float32",
            callback=callback
        ):

            while True:

                data = q.get()

                if recognizer.AcceptWaveform(data.tobytes()):

                    resultado = json.loads(recognizer.Result())
                    texto = resultado.get("text", "")

                    if texto:

                        entrada.delete(0, "end")
                        entrada.insert(0, texto)

                        falar("Texto capturado")
                        break

    except Exception as erro:

        chat.insert("end", f"Erro microfone: {erro}\n\n")
# =========================
# ENVIAR
# =========================

def enviar():

    global humor

    mensagem = entrada.get().strip()

    if mensagem == "":
        return

    chat.insert("end", f"Você: {mensagem}\n\n")
    entrada.delete(0, "end")

    comando = mensagem.lower()

    resposta = ""

    # =========================
    # MEMÓRIA
    # =========================

    if comando.startswith("lembrar"):

        texto = comando.replace("lembrar", "").strip()
        salvar_memoria(texto)
        resposta = f"Vou lembrar que {texto}"

    elif comando == "mostrar memória":

        resposta = ler_memoria()

    # =========================
    # HUMOR
    # =========================

    elif comando == "modo feliz":
        humor = "feliz"
        resposta = "Agora estou feliz."

    elif comando == "modo sério":
        humor = "sério"
        resposta = "Agora estou séria."

    elif comando == "modo engraçado":
        humor = "engraçado"
        resposta = "Agora estou engraçada."

    # =========================
    # INTERNET
    # =========================

    elif comando.startswith("pesquisar"):

        pesquisa = comando.replace("pesquisar", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={pesquisa}")
        resposta = f"Pesquisando {pesquisa}"

    elif comando == "abrir google":
        webbrowser.open("https://google.com")
        resposta = "Abrindo Google"

    elif comando == "abrir youtube":
        webbrowser.open("https://youtube.com")
        resposta = "Abrindo YouTube"

    # =========================
    # PROGRAMAS
    # =========================

    elif comando == "abrir calculadora":
        os.system("calc")
        resposta = "Abrindo calculadora"

    elif comando == "abrir paint":
        os.system("mspaint")
        resposta = "Abrindo Paint"

    elif comando == "abrir bloco de notas":
        os.system("notepad")
        resposta = "Abrindo bloco de notas"

    # =========================
    # IA
    # =========================

    else:

        try:

            memoria = ler_memoria()

            resposta_ia = ollama.chat(
                model="llama3",
                messages=[
                    {
                        "role": "system",
                        "content": f"""
Você é L.I.Z.A.

Uma inteligência artificial feminina.

Você fala português do Brasil.

Seu humor atual é {humor}.

Memórias do usuário:
{memoria}
"""
                    },
                    {
                        "role": "user",
                        "content": mensagem
                    }
                ]
            )

            resposta = resposta_ia["message"]["content"]

        except Exception as erro:

            resposta = f"Erro: {erro}"

    # =========================
    # MOSTRAR
    # =========================

    chat.insert("end", f"L.I.Z.A: {resposta}\n\n")
    chat.see("end")
    falar(resposta)

# =========================
# INTERFACE
# =========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("L.I.Z.A")
janela.geometry("900x650")

titulo = ctk.CTkLabel(
    janela,
    text="L.I.Z.A",
    font=("Arial", 32)
)
titulo.pack(pady=20)

chat = ctk.CTkTextbox(
    janela,
    width=850,
    height=450
)
chat.pack(pady=10)

chat.insert("end", "L.I.Z.A: Olá! Como posso ajudar?\n\n")

entrada = ctk.CTkEntry(
    janela,
    width=700,
    placeholder_text="Digite uma mensagem..."
)
entrada.pack(pady=10)

entrada.bind("<Return>", lambda event: enviar())

# =========================
# BOTÕES (CORRIGIDO)
# =========================

frame_botoes = ctk.CTkFrame(janela)
frame_botoes.pack(pady=10)

botao = ctk.CTkButton(
    frame_botoes,
    text="Enviar",
    command=enviar,
    width=150
)
botao.grid(row=0, column=0, padx=10)

botao_microfone = ctk.CTkButton(
    frame_botoes,
    text="🎤 Falar",
    command=ouvir_microfone,
    width=150
)
botao_microfone.grid(row=0, column=1, padx=10)

janela.mainloop()