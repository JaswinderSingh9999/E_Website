
document.getElementById("openChat").onclick = () => {
    document.getElementById("chatBox").style.display = "flex";
};

document.getElementById("closeChat").onclick = () => {
    document.getElementById("chatBox").style.display = "none";
};

document.getElementById("sendBtn").onclick = sendMsg;

// ✅ Press Enter to send
document.getElementById("msgInput").addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        sendMsg();
    }
});

function addMsg(type, text) {
    let area = document.getElementById("chatArea");

    // ✅ Prevent HTML injection
    let safeText = text.replace(/</g, "&lt;").replace(/>/g, "&gt;");

    let msg = `<div class="${type} msg">${safeText}</div>`;
    area.innerHTML += msg;

    area.scrollTop = area.scrollHeight;
}

async function sendMsg() {
    let input = document.getElementById("msgInput");
    let text = input.value.trim();

    if (!text) return;

    addMsg("user", text);
    input.value = "";

    // ✅ Show typing indicator
    addMsg("bot", "Typing...");
    
    try {
        let res = await fetch("/chat-api/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: text })
        });

        let data = await res.json();

        // ❌ Remove "Typing..."
        let chatArea = document.getElementById("chatArea");
        chatArea.lastChild.remove();

        addMsg("bot", data.reply);

    } catch (error) {
        console.error("Error:", error);

        let chatArea = document.getElementById("chatArea");
        chatArea.lastChild.remove();

        addMsg("bot", "⚠️ Server error, try again");
    }
}
