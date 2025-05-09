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

    console.log("Enviando para o backend:", mensagem);

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mensagem })
    })
    .then(res => res.json())
    .then(data => {
        console.log("Resposta do backend:", data);
        adicionarMensagem("bot", "Bot: " + data.resposta);
    })
    .catch(err => console.error("Erro ao enviar mensagem:", err));
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("mensagem").addEventListener("keypress", function(e) {
        if (e.key === "Enter") enviar();
    });
});
