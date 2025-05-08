function adicionarMensagem(tipo, texto) {
    const chat = document.getElementById("chat");
    const msg = document.createElement("div");
    msg.className = "mensagem " + tipo;
    msg.innerText = texto;
    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
}

function enviar() {
    const input = document.getElementById("mensagem");
    const mensagem = input.value.trim();
    if (!mensagem) return;

    adicionarMensagem("usuario", "Você: " + mensagem);
    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mensagem })
    })
    .then(res => res.json())
    .then(data => adicionarMensagem("bot", "Bot: " + data.resposta));
}

document.getElementById("mensagem").addEventListener("keypress", function(e) {
    if (e.key === "Enter") enviar();
});