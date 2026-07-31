const API_URL = "https://liza-ai-1.onrender.com";

const chat = document.getElementById("chat");
const input = document.getElementById("message");
const send = document.getElementById("send");
const typing = document.getElementById("typing");

// =========================
// Adicionar mensagem
// =========================

function addMessage(text, sender) {

    const div = document.createElement("div");

    div.className = `message ${sender}`;

    div.innerHTML = `
        <div class="message-body">
            <div class="message-content">
                ${text}
            </div>
        </div>
    `;

    chat.appendChild(div);

    chat.scrollTop = chat.scrollHeight;
}

// =========================
// Enviar mensagem
// =========================

async function sendMessage() {

    const text = input.value.trim();

    if (!text) return;

    addMessage(text, "user");

    input.value = "";

    typing.style.display = "flex";

    try {

        const response = await fetch(API_URL + "/chat", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                usuario: "Beto",

                message: text

            })

        });

        const data = await response.json();

        typing.style.display = "none";

        // Ajuste caso sua API retorne outro nome
        const resposta =
            data.text ||
            data.response ||
            data.message ||
            "Sem resposta.";

        addMessage(resposta, "assistant");

    } catch (e) {

        typing.style.display = "none";

        addMessage(

            "Erro ao conectar com a L.I.Z.A.",

            "assistant"

        );

        console.error(e);

    }

}

// =========================
// Eventos
// =========================

send.addEventListener("click", sendMessage);

input.addEventListener("keydown", function(e){

    if(e.key === "Enter" && !e.shiftKey){

        e.preventDefault();

        sendMessage();

    }

});