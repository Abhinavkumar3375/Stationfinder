document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("user-input").addEventListener("keypress", function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const userInput = document.getElementById("user-input").value.trim();
    if (!userInput) return;

    appendMessage(userInput, 'user');
    document.getElementById("user-input").value = '';

    fetch('/chatbot_response', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        appendMessage(data.response, 'bot');
    })
    .catch(error => {
        console.error('Error:', error);
        appendMessage("Sorry, something went wrong.", 'bot');
    });
}

function appendMessage(message, sender) {
    const messageList = document.getElementById("chat-messages");
    const newMessage = document.createElement("li");
    newMessage.className = sender;
    newMessage.textContent = message;
    messageList.appendChild(newMessage);
    messageList.scrollTop = messageList.scrollHeight;
}
