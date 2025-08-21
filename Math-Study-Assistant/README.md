# Math Assistant - RAG-Powered Mathematical Tutor

A Retrieval-Augmented Generation (RAG) system that creates an intelligent math tutor by combining PDF textbook ingestion, vector search, and AI-powered question answering. The system processes mathematical textbooks and provides step-by-step solutions with proper citations.

## Features

- **PDF Textbook Ingestion**: Automatically extracts and chunks mathematical content from PDF textbooks
- **Vector Search**: Uses Pinecone for efficient semantic search of mathematical concepts
- **Dual AI Support**: Compatible with both OpenAI GPT models and Google Gemini
- **Citation System**: Provides proper source citations with page numbers
- **Chunking Strategy**: Optimized text chunking with overlap for mathematical context preservation
- **Educational Focus**: Designed specifically for mathematical tutoring with step-by-step explanations

## Architecture

The system consists of three main components:

1. **Document Processing**: PDF extraction, text chunking, and embedding generation
2. **Vector Storage**: Pinecone index for storing and retrieving mathematical content
3. **Question Answering**: AI-powered response generation with source citations

## Prerequisites

### API Keys Required

```bash
OPENAI_API_KEY=""        # For OpenAI implementation
PINECONE_API_KEY=""      # For vector storage
GEMINI_API_KEY=""        # For Google Gemini implementation
```

### Python Dependencies

```bash
pip install pypdf pinecone openai tiktoken orjson python-dotenv google.generativeai
```

## Configuration

### OpenAI Implementation
- **Embedding Model**: `text-embedding-3-small` (1536 dimensions)
- **Generation Model**: `gpt-3.5-turbo`
- **Index Name**: `math-index`

### Google Gemini Implementation
- **Embedding Model**: `models/embedding-001` (768 dimensions)  
- **Generation Model**: `gemini-1.5-flash`
- **Index Name**: `math-index-gemini`

### Tunable Parameters

```python
TOP_K = 10              # Number of chunks to retrieve
MIN_SIM = 0.1           # Minimum similarity threshold
CHUNK_TOKENS = 400      # Tokens per chunk
CHUNK_OVERLAP = 49      # Overlap between chunks
MAX_CHUNK_TEXT = 2000   # Max characters per chunk (Gemini)
```

## Usage

### 1. Environment Setup

```python
import os
os.environ["OPENAI_API_KEY"] = "your-openai-key"
os.environ["PINECONE_API_KEY"] = "your-pinecone-key" 
os.environ["GEMINI_API_KEY"] = "your-gemini-key"
```

### 2. Initialize the System

For OpenAI implementation:
```python
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec

client = OpenAI(api_key=OPENAI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX)
```

For Gemini implementation:
```python
import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)
```

### 3. Ingest a Textbook

```python
# Ingest PDF and create searchable chunks
n = ingest_pdf_safe(
    "/path/to/textbook.pdf", 
    source="Textbook Name", 
    namespace="math_textbook"
)
print(f"Indexed {n} chunks")
```

### 4. Ask Questions

```python
result = answer_query("""
Ages of students in a class:
Given the data: 19, 21, 22, 20, 24, 22, 20, 19, 21
a) Find the mean, median, and mode
b) Compute the range, variance, and standard deviation
""", namespace="math_textbook")

print(result['answer'])
```

## Key Functions

### Document Processing

- `pdf_to_pages(path)`: Extracts text from PDF pages
- `chunk_text(text, page)`: Creates overlapping text chunks
- `ingest_pdf_safe()`: Complete PDF ingestion pipeline

### Retrieval & QA

- `retrieve(query, namespace)`: Semantic search for relevant content
- `answer_query(query, namespace)`: End-to-end question answering
- `build_messages()`: Constructs prompts with retrieved context

### Utilities

- `num_tokens(text)`: Estimates token count
- `flatten_embedding()`: Handles embedding format variations
- `safe_split_text()`: Ensures chunks don't exceed size limits

## Response Format

Each answer includes:
- **Step-by-step solution**: Detailed mathematical explanation
- **Citations**: Source references with page numbers `[Source, p.Page]`
- **Disclaimer**: Educational use reminder

```python
{
    "answer": "Step-by-step solution with calculations...",
    "citations": [{"source": "Textbook Name", "page": 42}],
    "disclaimer": "Educational use only. Always double-check solutions."
}
```

## System Prompts

The assistant is configured with educational-focused prompts:

```
You are a helpful **math tutor assistant**.
Rules: use provided textbook sources (not required), explain step by step, 
and cite like [Source, p.Page] if textbook is used.
```

## Best Practices

### For Mathematical Content
- Use textbooks with clear mathematical notation
- Ensure PDFs have extractable text (not image-only)
- Consider subject-specific namespaces for organization

### For Performance
- Adjust `TOP_K` based on content complexity
- Fine-tune similarity thresholds for your domain
- Monitor chunk sizes to balance context and relevance

### For Accuracy
- Always include the educational disclaimer
- Encourage users to verify solutions
- Provide step-by-step explanations for transparency

## Limitations

- PDF text extraction quality depends on source formatting
- Mathematical notation may not render perfectly in plain text
- AI responses should always be verified for accuracy
- System performance depends on the quality of ingested textbooks

## License

Educational use only. This system is designed for learning and should not replace professional mathematical instruction or verification.

## Contributing

When extending this system:
1. Maintain educational focus and safety guidelines
2. Preserve citation and disclaimer functionality  
3. Test with diverse mathematical content types
4. Consider accessibility and clarity in responses