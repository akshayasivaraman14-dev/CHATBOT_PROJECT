async function sendMessage() {
    let input = document.getElementById("user-input");
    let message = input.value;

    if (!message) return;

    let chatBox = document.getElementById("chat-box");

    // user message
    chatBox.innerHTML += `<div class="user">🧑 ${message}</div>`;

    input.value = "";

    // send to backend
    let response = await fetch("/ask", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: message})
    });

    let data = await response.json();

    // bot reply
    chatBox.innerHTML += `<div class="bot">🤖 ${data.reply}</div>`;
}