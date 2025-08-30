
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const clearChatButton = document.getElementById('clearChat');
const typingIndicator = document.getElementById('typingIndicator');
const loadingOverlay = document.getElementById('loadingOverlay');
const charCount = document.getElementById('charCount');
const subjectSelect = document.getElementById('subject');
const assistantTitle = document.getElementById('assistantTitle');


const API_BASE_URL = 'https://kp2ar7bpxi.execute-api.us-east-2.amazonaws.com';


let isProcessing = false;
let sessionId = null;


document.addEventListener('DOMContentLoaded', function () {
    setupEventListeners();
    autoResizeTextarea();
    updateCharCount();
});


function setupEventListeners() {

    sendButton.addEventListener('click', sendMessage);


    messageInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });


    messageInput.addEventListener('input', function () {
        autoResizeTextarea();
        updateCharCount();
        updateSendButton();
    });

    subjectSelect.addEventListener('change', () => {
        const subject = subjectSelect.value;
        assistantTitle.textContent =
            subject === 'math'
                ? "Math Assistant"
                : subject === 'sql'
                    ? "SQL Assistant"
                    : subject === 'astro'
                        ? "Astronomy Assistant"
                        : "AI Assistant";


        const icon = document.getElementById('assistantIcon');
        if (subject === 'math') {
            icon.className = 'fas fa-calculator';
        } else if (subject === 'sql') {
            icon.className = 'fas fa-database';
        } else if (subject === 'astro') {
            icon.className = 'fas fa-star';
        } else {
            icon.className = 'fas fa-robot'; // Default icon
        }

        const message = document.getElementById('messageInput');
        if (subject === 'math') {
            message.placeholder = "Ask me a math question...";
        } else if (subject === 'sql') {
            message.placeholder = "Ask me a SQL question...";
        } else if (subject === 'astro') {
            message.placeholder = "Ask me an astronomy question...";
        } else {
            message.placeholder = "Ask me anything...";
        }


        // Replace welcome message
        clearChatMessages();
        addMessage(
            subject === 'math'
                ? "Hello! I'm your AI Math Assistant. I can help you with:\n- Solving mathematical problems\n- Explaining concepts\n- Step-by-step solutions"
                : subject === 'sql'
                    ? "Hello! I'm your AI SQL Assistant. I can help you with:\n- Writing and optimizing SQL queries\n- Explaining database concepts\n- Providing step-by-step query breakdowns"
                    : subject === 'astro'
                        ? "Hello! I'm your AI Astronomy Assistant. I can help you with:\n- Understanding celestial objects and phenomena\n- Explaining space concepts and terminology\n- Guiding you through stargazing and astronomy basics"
                        : "Hello! I'm your AI Assistant.",
            'assistant'
        );

    });



    clearChatButton.addEventListener('click', clearChat);


    messageInput.focus();
}

function clearChatMessages() {
    const messages = chatMessages.querySelectorAll('.message');
    messages.forEach(m => m.remove());
}

function autoResizeTextarea() {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
}


function updateCharCount() {
    const count = messageInput.value.length;
    charCount.textContent = `${count}/2000`;


    if (count > 1800) {
        charCount.style.color = '#dc3545';
    } else if (count > 1500) {
        charCount.style.color = '#ffc107';
    } else {
        charCount.style.color = '#6c757d';
    }
}

// Update send button state
function updateSendButton() {
    const hasText = messageInput.value.trim().length > 0;
    sendButton.disabled = !hasText || isProcessing;
}

// Send message function
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || isProcessing) return;

    isProcessing = true;
    updateSendButton();

    // Add user message to chat
    addMessage(message, 'user');

    // Clear input
    messageInput.value = '';
    autoResizeTextarea();
    updateCharCount();

    // Show typing indicator
    showTypingIndicator();

    const subjectSelect = document.getElementById('subject');

    try {
        // Make API call
        const response = await fetch(`${API_BASE_URL}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: message, subject: subjectSelect.value, session_id: sessionId }),  // <-- Fixed key here
            credentials: 'include' // Include cookies for session management
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        sessionId = data.session_id;

        // Hide typing indicator
        hideTypingIndicator();

        // Add assistant response
        addMessage(data.answer, 'assistant');

    } catch (error) {
        console.error('Error sending message:', error);
        hideTypingIndicator();
        addErrorMessage('Sorry, I encountered an error while processing your request. Please try again.');
    } finally {
        isProcessing = false;
        updateSendButton();
    }
}


function addMessage(content, role) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';

    const icon = document.createElement('i');
    icon.className = role === 'user' ? 'fas fa-user' : 'fas fa-robot';
    avatar.appendChild(icon);

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';

    const messageText = document.createElement('div');
    messageText.className = 'message-text';

    // Format the content (handle line breaks and basic formatting)
    const formattedContent = formatMessageContent(content);
    messageText.innerHTML = formattedContent;

    const messageTime = document.createElement('div');
    messageTime.className = 'message-time';
    messageTime.textContent = getCurrentTime();

    messageContent.appendChild(messageText);
    messageContent.appendChild(messageTime);

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);

    // Insert before typing indicator if present, else append
    if (chatMessages.contains(typingIndicator)) {
        chatMessages.insertBefore(messageDiv, typingIndicator);
    } else {
        chatMessages.appendChild(messageDiv);
    }

    // Scroll to bottom
    scrollToBottom();
}

// Add error message
function addErrorMessage(content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant-message error-message';

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';

    const icon = document.createElement('i');
    icon.className = 'fas fa-exclamation-triangle';
    avatar.appendChild(icon);

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';

    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.style.borderLeft = '4px solid #dc3545';
    messageText.style.backgroundColor = '#fff5f5';
    messageText.textContent = content;

    const messageTime = document.createElement('div');
    messageTime.className = 'message-time';
    messageTime.textContent = getCurrentTime();

    messageContent.appendChild(messageText);
    messageContent.appendChild(messageTime);

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);

    // Insert before typing indicator if present, else append
    if (chatMessages.contains(typingIndicator)) {
        chatMessages.insertBefore(messageDiv, typingIndicator);
    } else {
        chatMessages.appendChild(messageDiv);
    }

    // Scroll to bottom
    scrollToBottom();
}

// Format message content (handle line breaks, code blocks, etc.)
function formatMessageContent(content) {
    // Replace line breaks with <br> tags
    let formatted = content.replace(/\n/g, '<br>');

    // Basic code block detection (text between backticks)
    formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Math expression detection (basic LaTeX-like syntax)
    formatted = formatted.replace(/\$\$([^$]+)\$\$/g, '<div class="math-block">$$$1$$</div>');
    formatted = formatted.replace(/\$([^$]+)\$/g, '<span class="math-inline">\$ $1 \$</span>');  // <-- fixed capturing group usage

    return formatted;
}

// Show typing indicator
function showTypingIndicator() {
    typingIndicator.style.display = 'block';
    scrollToBottom();
}

// Hide typing indicator
function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

// Clear chat function
async function clearChat() {
    if (isProcessing) return;

    try {

        // Clear chat messages (keep welcome message)
        const messages = chatMessages.querySelectorAll('.message:not(:first-child)');
        messages.forEach(message => {
            if (!message.querySelector('.typing-dots')) {
                message.remove();
            }
        });

        // Hide typing indicator if visible
        hideTypingIndicator();

        // Show success message
        showNotification('Chat history cleared successfully!', 'success');

    } catch (error) {
        console.error('Error clearing chat:', error);
        showNotification('Failed to clear chat history. Please try again.', 'error');
    }
}

// Get current time formatted
function getCurrentTime() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

// Scroll to bottom of chat
function scrollToBottom() {
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 1001;
        animation: slideInRight 0.3s ease-out;
        max-width: 300px;
    `;

    // Set background color based on type
    switch (type) {
        case 'success':
            notification.style.backgroundColor = '#28a745';
            break;
        case 'error':
            notification.style.backgroundColor = '#dc3545';
            break;
        default:
            notification.style.backgroundColor = '#17a2b8';
    }

    // Add to page
    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-in';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .math-block {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 6px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-family: 'Courier New', monospace;
        text-align: center;
        overflow-x: auto;
    }
    
    .math-inline {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 4px;
        padding: 0.125rem 0.25rem;
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
    }
    
    code {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 4px;
        padding: 0.125rem 0.25rem;
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
        color: #e83e8c;
    }
`;
document.head.appendChild(style);

// Handle page visibility changes (pause/resume processing)
document.addEventListener('visibilitychange', function () {
    if (document.hidden && isProcessing) {
        // Page is hidden, could pause processing if needed
    }
});

// Handle beforeunload (warn if processing)
window.addEventListener('beforeunload', function (e) {
    if (isProcessing) {
        e.preventDefault();
        e.returnValue = 'You have a message being processed. Are you sure you want to leave?';
    }
});