const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const messages = document.getElementById('messages');
const welcomeMessage = document.getElementById('welcomeMessage');

function addMessage(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'user' ? '👤' : 'H';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = content;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);
    messages.appendChild(messageDiv);
    messages.scrollTop = messages.scrollHeight;
}

function adjustTextarea() {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;
    
    welcomeMessage.style.display = 'none';
    addMessage(message, 'user');
    messageInput.value = '';
    adjustTextarea();
    sendButton.disabled = true;
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        addMessage(data.response || 'No response received', 'assistant');
        
    } catch (error) {
        console.error('Fetch error:', error);
        addMessage('Sorry, I encountered an error. Please try again.', 'assistant');
    } finally {
        sendButton.disabled = false;
    }
}

sendButton.addEventListener('click', sendMessage);
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});
messageInput.addEventListener('input', adjustTextarea);