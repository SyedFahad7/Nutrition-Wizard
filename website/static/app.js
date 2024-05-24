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
        botMessage.innerHTML = "<strong>Bot:</strong> " + JSON.stringify(data.message); // Corrected this line
        chatWindow.appendChild(botMessage);
    })
    .catch(error => console.error('Error:', error));
}

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function(stream) {
            var mediaRecorder = new MediaRecorder(stream);
            var audioChunks = [];

            mediaRecorder.addEventListener("dataavailable", function(event) {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", function() {
                var audioBlob = new Blob(audioChunks);
                var formData = new FormData();
                formData.append('audio', audioBlob);

                fetch('/voice_input', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    var chatWindow = document.getElementById("chat-window");
                    var botMessage = document.createElement("div");
                    botMessage.className = "message";
                    botMessage.innerHTML = "<strong>Bot:</strong> " + data.text;
                    chatWindow.appendChild(botMessage);

                    fetchRecipe(data.text); // Use the recognized text as input
                })
                .catch(error => console.error('Error:', error));
            });

            mediaRecorder.start();
            setTimeout(function() {
                mediaRecorder.stop();
            }, 5000);
        })
        .catch(function(err) {
            console.error('Error:', err);
        });
}
