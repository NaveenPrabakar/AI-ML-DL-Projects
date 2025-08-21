# Medical Study Assistant - RAG System

A Retrieval-Augmented Generation (RAG) system designed for educational healthcare reference using OpenAI embeddings, Pinecone vector database, and GPT-4o for intelligent question answering from medical textbooks.

## Features

- **PDF Ingestion**: Convert medical textbooks and documents into searchable vector embeddings
- **Intelligent Chunking**: Smart text segmentation with configurable overlap for better context retention
- **Risk Classification**: Automatic query risk assessment (LOW/MED/HIGH) for appropriate response handling
- **Source Citation**: Automatic citation of sources with page numbers for transparency
- **Educational Safeguards**: Built-in disclaimers and restrictions to avoid medical advice

## Architecture

```
PDF Documents → Text Extraction → Chunking → Embeddings → Pinecone Vector DB
                                                              ↓
User Query → Risk Classification → Vector Search → Context Retrieval → GPT-4o → Response
```

## Prerequisites

- Python 3.7+
- OpenAI API key
- Pinecone API key
- Required Python packages (see installation)

## Installation

```bash
pip install pypdf pinecone openai tiktoken orjson python-dotenv
```

## Configuration

Set your API keys as environment variables:

```python
import os
os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"
os.environ["PINECONE_API_KEY"] = "your_pinecone_api_key_here"
```

### Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `EMBED_MODEL` | "text-embedding-3-small" | OpenAI embedding model |
| `GEN_MODEL` | "gpt-4o-mini" | GPT model for response generation |
| `TOP_K` | 8 | Number of similar chunks to retrieve |
| `MIN_SIM` | 0.3 | Minimum similarity threshold |
| `CHUNK_TOKENS` | 1000 | Tokens per text chunk |
| `CHUNK_OVERLAP` | 200 | Overlap between adjacent chunks |

## Usage

### 1. Initialize the System

```python
from medical_study_assistant import *

# Initialize OpenAI and Pinecone clients
client = OpenAI(api_key=OPENAI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
```

### 2. Ingest Medical Documents

```python
# Ingest a PDF textbook
num_chunks = ingest_pdf(
    path="/path/to/medical_textbook.pdf",
    source="Harrison's Internal Medicine (21e)",
    namespace="harrison21",
    year=2024
)
print(f"Indexed {num_chunks} chunks")
```

### 3. Query the System

```python
# Ask a medical question
result = answer_query(
    query="What are the symptoms of melanoma?",
    namespace="harrison21"
)

print("Risk Level:", result["risk"])
print("Answer:", result["answer"])
print("Citations:", result["citations"])
```

## Response Structure

```python
{
    "risk": "MED",  # LOW/MED/HIGH risk classification
    "answer": "Detailed answer with citations...",
    "citations": [
        {"source": "Harrison's (21e)", "page": 5},
        {"source": "Harrison's (21e)", "page": 8}
    ],
    "disclaimer": "Educational use only. Not medical advice..."
}
```

## Risk Classification

The system automatically classifies queries into three risk levels:

- **LOW**: Definitions, anatomy, basic concepts
- **MED**: Medical conditions, diagnostic criteria
- **HIGH**: Emergency situations, dosing, treatment recommendations

## Safety Features

### Educational Safeguards
- Automatic disclaimer inclusion
- No diagnosis or treatment recommendations
- Source citation requirements
- Risk-appropriate response modulation

### System Prompts
- **System Prompt**: Restricts responses to provided sources only
- **Risk Prompt**: Ensures appropriate risk classification
- **Disclaimer**: Consistent educational-only messaging

## Fine-tuning Support

Generate training data for model fine-tuning:

```python
# Build fine-tuning examples
ft_example = build_ft_example(question, context_chunks)

# Write JSONL format for OpenAI fine-tuning
write_jsonl(examples, "training_data.jsonl")
```

## API Reference

### Core Functions

#### `ingest_pdf(path, source, namespace, year)`
Processes and indexes a PDF document.
- **path**: File path to PDF
- **source**: Source identifier for citations
- **namespace**: Pinecone namespace for organization
- **year**: Publication year

#### `answer_query(query, namespace)`
Retrieves relevant context and generates an answer.
- **query**: User's question
- **namespace**: Pinecone namespace to search

#### `classify_risk(query)`
Classifies query risk level.
- Returns: "LOW", "MED", or "HIGH"

### Utility Functions

#### `pdf_to_pages(path)`
Extracts text from PDF pages.

#### `chunk_text(text, page, tokens, overlap)`
Splits text into overlapping chunks.

#### `retrieve(query, namespace, k)`
Performs vector similarity search.

## Example Workflow

```python
# 1. Setup
import os
os.environ["OPENAI_API_KEY"] = "sk-..."
os.environ["PINECONE_API_KEY"] = "..."

# 2. Ingest textbook
chunks = ingest_pdf(
    "/content/dermatology_textbook.pdf",
    source="Dermatology Atlas",
    namespace="derm_atlas"
)

# 3. Query system
result = answer_query(
    "What are the ABCDE criteria for melanoma?",
    namespace="derm_atlas"
)

# 4. Display results
print(f"Risk: {result['risk']}")
print(f"Answer: {result['answer']}")
for cite in result['citations']:
    print(f"Source: {cite['source']}, Page: {cite['page']}")
```

## Limitations

- **Educational Use Only**: Not for clinical decision-making
- **Source Dependent**: Responses limited to ingested documents
- **No Real-time Updates**: Requires manual re-ingestion for updates
- **Context Window**: Limited by chunk size and retrieval count

## Security Considerations

- Store API keys securely (environment variables, secrets management)
- Implement rate limiting for production use
- Validate input queries for malicious content
- Monitor usage and costs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

This project is intended for educational and research purposes. Ensure compliance with medical data regulations and OpenAI/Pinecone terms of service.

## Support

For questions or issues:
- Check existing documentation
- Review configuration parameters
- Verify API key permissions
- Monitor Pinecone index status

---

**Disclaimer**: This system is for educational purposes only and does not provide medical advice. Always consult qualified healthcare professionals for medical concerns.