# Math Study Assistant

An intelligent AI-powered study assistant that provides step-by-step solutions and explanations for Math, SQL, and Astronomy questions. Built with FastAPI, Google Gemini AI, and Pinecone vector database for enhanced learning experiences.

## 🚀 Features

- **Multi-Subject Support**: Get help with Math, SQL, and Astronomy
- **AI-Powered Responses**: Powered by Google Gemini 2.0 Flash for accurate, detailed answers
- **Step-by-Step Solutions**: Clear, educational explanations with proper methodology
- **Vector Search**: Intelligent retrieval of relevant textbook content using Pinecone
- **Session Management**: Maintains conversation context across multiple questions
- **Modern Web Interface**: Clean, responsive chat interface with real-time interactions
- **Citation Support**: References to source materials when applicable
- **Educational Focus**: Designed specifically for learning and understanding

## 🏗️ Architecture

```
Math-Study-Assistant/
├── main.py              # FastAPI backend server
├── Gemini.py            # Core AI logic and vector search
├── index.html           # Web interface
├── styles.css           # UI styling
├── script.js            # Frontend functionality
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container configuration
└── README.md           # This file
```

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **AI Model**: Google Gemini 2.0 Flash
- **Vector Database**: Pinecone
- **Caching**: Redis
- **Frontend**: HTML5, CSS3, JavaScript
- **PDF Processing**: PyPDF
- **Containerization**: Docker

## 📋 Prerequisites

Before running this application, you'll need:

- Python 3.8+
- Google Gemini API key
- Pinecone API key
- Redis instance
- PDF textbooks for knowledge base (optional)

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Math-Study-Assistant
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
REDIS_URL=your_redis_url_here
PINECONE_INDEX=your_pinecone_index_name
```

### 4. Initialize Vector Database

The application will automatically create the Pinecone index if it doesn't exist. You can ingest PDF textbooks using the functions in `Gemini.py`:

```python
from Gemini import ingest_pdf_safe

# Ingest a math textbook
ingest_pdf_safe("path/to/math_textbook.pdf", "Mathematics Textbook", "math-namespace")

# Ingest SQL materials
ingest_pdf_safe("path/to/sql_guide.pdf", "SQL Guide", "sql-namespace")

# Ingest astronomy materials
ingest_pdf_safe("path/to/astronomy_book.pdf", "Astronomy Textbook", "astro-namespace")
```

### 5. Run the Application

#### Option A: Direct Python Execution

```bash
# Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Option B: Docker Deployment

```bash
# Build the Docker image
docker build -t math-study-assistant .

# Run the container
docker run -p 8000:8000 --env-file .env math-study-assistant
```

### 6. Access the Web Interface

Open `index.html` in your web browser or serve it using a local server:

```bash
# Using Python's built-in server
python -m http.server 8080

# Then navigate to http://localhost:8080
```

## 🎯 Usage

### Web Interface

1. **Select Subject**: Choose between Math, SQL, or Astronomy from the dropdown
2. **Ask Questions**: Type your question in the chat input
3. **Get Answers**: Receive step-by-step explanations with citations
4. **Clear Chat**: Start fresh conversations using the "Clear Chat" button

### API Endpoints

The application exposes the following REST API endpoints:

#### POST `/answer`
Submit a question and receive an AI-generated answer.

**Request Body:**
```json
{
  "question": "Explain the Pythagorean theorem",
  "namespace": "math-namespace"
}
```

**Response:**
```json
{
  "session_id": "uuid-string",
  "answer": "Step-by-step explanation...",
  "citations": [
    {
      "source": "Mathematics Textbook",
      "page": 45
    }
  ],
  "disclaimer": "Educational use only. Always double-check solutions."
}
```

## 🔍 How It Works

### 1. Question Processing
- User submits a question through the web interface
- The question is embedded using Google's embedding model
- Vector similarity search is performed against the knowledge base

### 2. Context Retrieval
- Relevant textbook passages are retrieved from Pinecone
- Context is ranked by similarity score
- Top-k most relevant passages are selected

### 3. AI Generation
- Context and question are formatted for Gemini AI
- System prompts ensure educational, step-by-step responses
- Previous conversation history is maintained for context

### 4. Response Delivery
- Generated answer is returned with citations
- Session is updated in Redis for future context
- Response is displayed in the web interface

## 🎨 Customization

### Adding New Subjects

1. Update the subject selector in `index.html`
2. Add new system prompts in `Gemini.py`
3. Create corresponding Pinecone namespaces
4. Update the handler function to route to new subjects

### Styling

Modify `styles.css` to customize the appearance:
- Color scheme and themes
- Layout and spacing
- Typography and fonts
- Responsive design breakpoints

### AI Behavior

Adjust the system prompts in `Gemini.py` to modify:
- Response style and format
- Educational approach
- Citation requirements
- Safety and content filtering

## 🔒 Security & Privacy

- API keys are stored in environment variables
- No sensitive data is logged or stored permanently
- Session data expires after 1 hour
- Educational use disclaimer is included in all responses

## 🐛 Troubleshooting

### Common Issues

1. **API Key Errors**
   - Verify your Gemini and Pinecone API keys are correct
   - Ensure API keys have proper permissions

2. **Redis Connection Issues**
   - Check Redis URL format and connectivity
   - Verify Redis instance is running

3. **Vector Search Problems**
   - Ensure Pinecone index exists and is properly configured
   - Check namespace names match your ingested data

4. **CORS Errors**
   - Update CORS origins in `main.py` to match your frontend URL
   - Ensure proper CORS middleware configuration

### Debug Mode

Enable debug logging by setting the log level in your FastAPI configuration:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 Educational Use

This application is designed for educational purposes:

- **Students**: Get help understanding complex concepts
- **Teachers**: Use as a supplementary teaching tool
- **Self-Learners**: Practice and verify understanding
- **Researchers**: Explore AI-assisted learning methodologies

**Important**: Always verify solutions independently. The AI provides guidance but should not replace critical thinking and verification.

## 🤝 Contributing

We welcome contributions! Please consider:

- Adding new subjects or knowledge domains
- Improving the AI response quality
- Enhancing the user interface
- Adding new features like progress tracking
- Optimizing performance and scalability

## 📄 License

This project is provided for educational use. Please respect the terms of service for all integrated APIs (Google Gemini, Pinecone, etc.).

## 🙏 Acknowledgments

- Google Gemini AI for powerful language model capabilities
- Pinecone for vector database infrastructure
- FastAPI for robust web framework
- The open-source community for various supporting libraries

---

**Happy Learning! 🎓** 