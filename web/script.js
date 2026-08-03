// ======================================================
// L.I.Z.A Web Client
// ======================================================

const chat = document.getElementById("chat");
const input = document.getElementById("message");
const send = document.getElementById("send");
const typing = document.getElementById("typing");

const assistantTemplate = document.getElementById("assistantTemplate");
const userTemplate = document.getElementById("userTemplate");

// ======================================================
// Remover tela inicial
// ======================================================

function removeWelcome() {

    const welcome = document.querySelector(".welcome");

    if (welcome) {

        welcome.remove();

    }

}

// ======================================================
// Scroll
// ======================================================

function scrollBottom() {

    chat.scrollTop = chat.scrollHeight;

}

// ======================================================
// Mensagem usuário
// ======================================================

function addUserMessage(text) {

    removeWelcome();

    const clone = userTemplate.content.cloneNode(true);

    clone.querySelector(".message-content").textContent = text;

    chat.appendChild(clone);

    scrollBottom();

}

// ======================================================
// Mensagem IA
// ======================================================

function addAssistantMessage(text) {

    removeWelcome();

    const clone = assistantTemplate.content.cloneNode(true);

    clone.querySelector(".message-content").textContent = text;

    const copy = clone.querySelector(".copy");

    copy.onclick = () => {

        navigator.clipboard.writeText(text);

        copy.innerText = "Copiado!";

        setTimeout(() => {

            copy.innerText = "📋 Copiar";

        },1500);

    };

    chat.appendChild(clone);

    scrollBottom();

}

// ======================================================
// Digitação
// ======================================================

function showTyping(){

    typing.style.display="flex";

}

function hideTyping(){

    typing.style.display="none";

}

// ======================================================
// Enviar
// ======================================================

async function sendMessage(){

    const text=input.value.trim();

    if(text==="") return;

    addUserMessage(text);

    input.value="";

    showTyping();

    try{

        const response = await fetch("/chat",{

            method:"POST",

            headers:{

                "Content-Type":"application/json"

            },

            body:JSON.stringify({

                usuario:"Beto",

                message:text

            })

        });

        if(!response.ok){

            throw new Error(

                "Erro HTTP "+response.status

            );

        }

        const data = await response.json();

        hideTyping();

        addAssistantMessage(

            data.text ??

            data.response ??

            data.message ??

            "Sem resposta."

        );

    }

    catch(e){

        hideTyping();

        console.error(e);

        addAssistantMessage(

            "Erro ao conectar com a L.I.Z.A."

        );

    }

}

// ======================================================
// Enter
// ======================================================

send.onclick = sendMessage;

input.addEventListener(

    "keydown",

    function(e){

        if(

            e.key==="Enter"

            &&

            !e.shiftKey

        ){

            e.preventDefault();

            sendMessage();

        }

    }

);

// ======================================================
// Auto Resize
// ======================================================

input.addEventListener("input",()=>{

    input.style.height="auto";

    input.style.height=input.scrollHeight+"px";

});

// ======================================================
// Nova conversa
// ======================================================

const newChat=document.getElementById("newChat");

if(newChat){

    newChat.onclick=()=>{

        chat.innerHTML=`

<div class="welcome">

<img src="assets/avatar.png">

<h2>Olá!</h2>

<p>Como posso ajudar você hoje?</p>

</div>

`;

    };

}