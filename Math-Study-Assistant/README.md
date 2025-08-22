# Math Assistant - ChatGPT-like Interface

A modern, responsive web interface for your AI math assistant backend. This interface provides a ChatGPT-like experience with real-time chat functionality, session management, and beautiful UI design.

## Features

- 🎨 **Modern UI Design**: Clean, responsive interface with smooth animations
- 💬 **Real-time Chat**: Instant message sending and receiving
- 📱 **Mobile Responsive**: Works perfectly on desktop, tablet, and mobile devices
- ⏱️ **Typing Indicators**: Visual feedback when the AI is processing
- 🔄 **Session Management**: Maintains conversation context across requests
- 🧹 **Clear Chat**: Easy way to start fresh conversations
- ⌨️ **Keyboard Shortcuts**: Enter to send, Shift+Enter for new lines
- 📊 **Character Counter**: Track message length with visual feedback
- 🔔 **Notifications**: Success and error notifications
- 🎯 **Math Formatting**: Support for inline and block math expressions

## File Structure

```
TypicalMathAssistant/
├── math.py              # Your FastAPI backend
├── math_knowledge.pdf   # Math knowledge base
├── index.html          # Main HTML interface
├── styles.css          # CSS styling
├── script.js           # JavaScript functionality
└── README.md           # This file
```

## Setup Instructions

### 1. Backend Setup

Make sure your FastAPI backend is running:

```bash
# Install dependencies (if not already done)
pip install fastapi uvicorn redis langchain openai faiss-cpu

# Set environment variables
export OPENAI_API_KEY="your-openai-api-key"
export REDIS_URL="your-redis-url"

# Run the backend
uvicorn math:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup

The frontend files are ready to use. Simply open `index.html` in your web browser, or serve them using a local server:

```bash
# Using Python's built-in server
python -m http.server 8080

# Using Node.js (if you have it installed)
npx serve .

# Using PHP (if you have it installed)
php -S localhost:8080
```

### 3. Configuration

Update the API URL in `script.js` if your backend is running on a different port:

```javascript
const API_BASE_URL = 'http://localhost:8000'; // Change this if needed
```

## Usage

1. **Open the Interface**: Navigate to `index.html` in your browser
2. **Start Chatting**: Type your math question in the input field
3. **Send Messages**: Press Enter or click the send button
4. **Clear Chat**: Use the "Clear Chat" button to start fresh
5. **View History**: Scroll through your conversation history

## API Endpoints

The interface communicates with your FastAPI backend using these endpoints:

- `POST /ask` - Send a question and get an answer
- `POST /clear_session` - Clear the current session

## Features in Detail

### Message Formatting

The interface supports various formatting options:

- **Line Breaks**: Automatically converted to `<br>` tags
- **Code Blocks**: Text between backticks (`code`) is formatted as inline code
- **Math Expressions**: 
  - Inline math: `$x^2 + y^2 = z^2$`
  - Block math: `$$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$`

### Responsive Design

The interface adapts to different screen sizes:

- **Desktop**: Full-width layout with optimal spacing
- **Tablet**: Adjusted padding and font sizes
- **Mobile**: Compact layout with touch-friendly buttons

### Session Management

- Each browser session maintains conversation context
- Sessions are stored in Redis with a 10-minute TTL
- Clear chat functionality resets both frontend and backend state

### Error Handling

- Network errors are displayed as user-friendly messages
- Loading states prevent multiple simultaneous requests
- Graceful degradation when backend is unavailable

## Customization

### Styling

You can customize the appearance by modifying `styles.css`:

- **Colors**: Update CSS variables for theme colors
- **Fonts**: Change the font family in the body selector
- **Layout**: Adjust spacing and sizing in the container classes

### Functionality

Modify `script.js` to add new features:

- **Message Formatting**: Extend the `formatMessageContent` function
- **API Integration**: Add new endpoints or modify request handling
- **UI Interactions**: Add new event listeners or UI components

## Browser Compatibility

The interface works on all modern browsers:

- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

## Troubleshooting

### Common Issues

1. **CORS Errors**: Make sure your FastAPI backend has CORS enabled
2. **Connection Refused**: Verify the backend is running on the correct port
3. **Session Issues**: Check that Redis is properly configured and running

### Debug Mode

Open the browser's developer console (F12) to see detailed error messages and API responses.

## Contributing

Feel free to enhance the interface by:

- Adding new UI components
- Improving accessibility
- Adding more formatting options
- Optimizing performance
- Adding unit tests

## License

This interface is provided as-is for use with your math assistant backend. 