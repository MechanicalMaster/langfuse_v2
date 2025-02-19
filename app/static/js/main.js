const API_BASE_URL = '/api/v1';

// Generate a random session ID
const sessionId = Math.random().toString(36).substring(7);

// Theme management
function toggleTheme() {
    const body = document.body;
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Initialize theme from localStorage
const savedTheme = localStorage.getItem('theme') || 'light';
document.body.setAttribute('data-theme', savedTheme);

// Message handling
function addMessage(content, isUser = false) {
    const messagesDiv = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const timestamp = new Date().toLocaleTimeString();
    messageDiv.innerHTML = `
        ${content}
        <div class="timestamp">${timestamp}</div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message
    addMessage(message, true);
    input.value = '';
    
    // Show typing indicator
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'typing-indicator';
    typingIndicator.innerHTML = `
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    `;
    document.getElementById('chatMessages').appendChild(typingIndicator);
    
    try {
        const response = await fetch(`${API_BASE_URL}/chat/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        });
        
        // Remove typing indicator
        typingIndicator.remove();
        
        if (response.ok) {
            const data = await response.json();
            addMessage(data.response);
        } else {
            const errorData = await response.json();
            addMessage(errorData.detail || 'Sorry, there was an error processing your message.');
        }
    } catch (error) {
        // Remove typing indicator
        typingIndicator.remove();
        console.error('Error:', error);
        addMessage('Network error. Please check your connection and try again.');
    }
}

// Event Listeners
document.getElementById('messageInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Add welcome message function
function addWelcomeMessage() {
    const messagesDiv = document.getElementById('chatMessages');
    const welcomeDiv = document.createElement('div');
    welcomeDiv.className = 'welcome-message';
    welcomeDiv.innerHTML = `
        <h2>👋 Welcome to Policy Chatbot!</h2>
        <p>I'm here to help you understand your policy documents. You can:</p>
        <p>1. Upload your policy documents using the "Upload Policy" button</p>
        <p>2. Ask me questions about your policies</p>
        <p>3. Get instant, accurate responses based on your documents</p>
        <p>How can I assist you today?</p>
    `;
    messagesDiv.appendChild(welcomeDiv);
}

// Call welcome message when page loads
document.addEventListener('DOMContentLoaded', () => {
    addWelcomeMessage();
}); 