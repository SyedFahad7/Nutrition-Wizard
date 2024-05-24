function sendMessage() {
    var userInput = document.getElementById("user-input").value;
    var chatWindow = document.getElementById("chat-window");

    if (userInput.trim() === "") return;

    var userMessage = document.createElement("div");
    userMessage.className = "message";
    userMessage.innerHTML = "<strong>You:</strong> " + userInput;
    chatWindow.appendChild(userMessage);

    document.getElementById("user-input").value = "";

    fetchRecipe(userInput);
}

function fetchRecipe(foodItem) {
    fetch('/recipe?foodItem=' + foodItem)
    .then(response => response.json())
    .then(data => {
        var chatWindow = document.getElementById("chat-window");
        var botMessage = document.createElement("div");
        botMessage.className = "message";
        botMessage.innerHTML = "<strong>Bot:</strong> " + data.message;
        chatWindow.appendChild(botMessage);
    })
    .catch(error => console.error('Error:', error));
}
