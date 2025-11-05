/**
 * Listy AI Assistant Integration
 * Your friendly European travel assistant
 */

class ListyAssistant {
    constructor() {
        this.isOpen = false;
        this.widget = null;
        this.messagesContainer = null;
        this.init();
    }

    init() {
        // Create floating button if it doesn't exist
        if (!document.querySelector('.listy-float')) {
            this.createFloatingButton();
        }

        // Override existing openListy function
        window.openListy = () => this.toggleWidget();

        // Load widget HTML
        this.loadWidget();
    }

    createFloatingButton() {
        const button = document.createElement('button');
        button.className = 'listy-float';
        button.innerHTML = '<i class="fas fa-comments"></i>';
        button.title = 'Chat with Listy, your travel assistant!';
        button.onclick = () => this.toggleWidget();

        // Add styles
        const styles = `
            .listy-float {
                position: fixed;
                bottom: 30px;
                right: 30px;
                z-index: 1000;
                background: linear-gradient(45deg, #ff6b6b, #ffa500);
                color: white;
                border: none;
                border-radius: 50%;
                width: 70px;
                height: 70px;
                font-size: 1.5rem;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                cursor: pointer;
                animation: listy-pulse 2s infinite;
                transition: all 0.3s ease;
            }
            .listy-float:hover {
                transform: scale(1.05);
            }
            @keyframes listy-pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
        `;

        if (!document.getElementById('listy-styles')) {
            const styleSheet = document.createElement('style');
            styleSheet.id = 'listy-styles';
            styleSheet.textContent = styles;
            document.head.appendChild(styleSheet);
        }

        document.body.appendChild(button);
    }

    async loadWidget() {
        try {
            const response = await fetch('/listy/widget/');
            const data = await response.json();

            // Create widget container
            const widgetDiv = document.createElement('div');
            widgetDiv.innerHTML = data.widget_html;
            document.body.appendChild(widgetDiv);

            this.widget = document.getElementById('listy-widget');
            this.messagesContainer = document.getElementById('listy-messages');

            // Setup event listeners
            this.setupEventListeners();

        } catch (error) {
            console.error('Error loading Listy widget:', error);
        }
    }

    setupEventListeners() {
        const input = document.getElementById('listy-input');
        const sendButton = document.getElementById('listy-send');
        const minimizeButton = document.getElementById('listy-minimize');

        // Send message on button click
        sendButton.addEventListener('click', () => this.sendMessage());

        // Send message on Enter key
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });

        // Minimize widget
        minimizeButton.addEventListener('click', () => this.toggleWidget());

        // Auto-focus input when widget opens
        input.addEventListener('focus', () => {
            input.placeholder = "Ask me about Hamburg, Barcelona, Prague...";
        });
    }

    toggleWidget() {
        if (!this.widget) return;

        this.isOpen = !this.isOpen;
        this.widget.style.display = this.isOpen ? 'flex' : 'none';

        if (this.isOpen) {
            document.getElementById('listy-input').focus();

            // Add current page context
            this.addContextMessage();
        }
    }

    addContextMessage() {
        const currentUrl = window.location.pathname;
        let contextMessage = '';

        if (currentUrl.includes('/guide/')) {
            const cityName = document.title.split(' ')[1] || 'this city';
            contextMessage = `I see you're reading about ${cityName}! What would you like to know? 🌟`;
        } else if (currentUrl === '/') {
            contextMessage = `Welcome to ListAcross.eu! Which European city interests you most? 🗺️`;
        }

        if (contextMessage && this.messagesContainer.children.length === 1) {
            this.addMessage(contextMessage, 'listy');
        }
    }

    async sendMessage() {
        const input = document.getElementById('listy-input');
        const message = input.value.trim();

        if (!message) return;

        // Add user message
        this.addMessage(message, 'user');
        input.value = '';

        // Show typing indicator
        this.showTypingIndicator();

        try {
            // Get current page context
            const context = this.getCurrentContext();

            const response = await fetch('/listy/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    message: message,
                    context: context
                })
            });

            const data = await response.json();

            // Remove typing indicator
            this.removeTypingIndicator();

            // Add Listy's response
            this.addMessage(data.message, 'listy');

        } catch (error) {
            console.error('Error sending message to Listy:', error);
            this.removeTypingIndicator();
            this.addMessage("Oops! I'm having trouble connecting right now. Try again in a moment! 😅", 'listy');
        }
    }

    getCurrentContext() {
        const currentUrl = window.location.pathname;
        let context = {};

        if (currentUrl.includes('/guide/')) {
            // Extract city from title or URL
            const titleParts = document.title.split(' ');
            if (titleParts.length > 1) {
                context.current_city = titleParts[1];
            }
        }

        context.page_type = currentUrl.includes('/guide/') ? 'city_guide' : 'homepage';
        context.url = currentUrl;

        return context;
    }

    addMessage(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `listy-message ${sender === 'user' ? 'user-message' : ''}`;

        const avatar = sender === 'user' ? '👤' : '😊';

        messageDiv.innerHTML = `
            <div class="listy-avatar-small">${avatar}</div>
            <div class="message-content">${message}</div>
        `;

        this.messagesContainer.appendChild(messageDiv);
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'listy-message typing-message';
        typingDiv.innerHTML = `
            <div class="listy-avatar-small">😊</div>
            <div class="message-content typing-indicator">
                <span>Listy is typing</span>
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;

        this.messagesContainer.appendChild(typingDiv);
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    removeTypingIndicator() {
        const typingMessage = this.messagesContainer.querySelector('.typing-message');
        if (typingMessage) {
            typingMessage.remove();
        }
    }

    getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];

        return cookieValue || document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }
}

// Initialize Listy when the page loads
document.addEventListener('DOMContentLoaded', function () {
    // Wait a bit for the page to fully load
    setTimeout(() => {
        window.listy = new ListyAssistant();
    }, 1000);
});

// Global function for backwards compatibility
function openListy() {
    if (window.listy) {
        window.listy.toggleWidget();
    } else {
        alert('Hi! I\'m Listy! 😊 I\'m starting up right now and will be ready in just a moment!');
    }
}