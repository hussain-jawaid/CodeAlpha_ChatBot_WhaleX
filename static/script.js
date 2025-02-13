const inputText = document.getElementById('inputText');
        const chatbox = document.getElementById('chatbox');
        const sendButton = document.getElementById('inputButton');

        function addMessage(message, isUser) {
            const messageDiv = document.createElement('div');
            messageDiv.className = isUser ? 'user-message' : 'bot-message';
            messageDiv.textContent = message;
            chatbox.appendChild(messageDiv);
            chatbox.scrollTop = chatbox.scrollHeight;
        }

        async function sendMessage() {
            const message = inputText.value.trim();
            if (message) {
                addMessage(message, true);
                inputText.value = '';

                try {
                    const response = await fetch('/get_response', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ user_input: message })
                    });

                    const data = await response.json();
                    addMessage(data.bot_response, false);
                } catch (error) {
                    console.error('Error:', error);
                    addMessage("Sorry, I'm having trouble connecting to the server.", false);
                }
            }
        }

        sendButton.addEventListener('click', sendMessage);
        inputText.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });