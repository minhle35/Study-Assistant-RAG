# 📚 StudyBuddy RAG Assistant

An AI-powered study companion that uses Retrieval-Augmented Generation (RAG) to help students learn from their documents. Upload your study materials and get intelligent answers with source citations and personalized study tips.

## Features

- **Document Processing**: Upload and process PDF, TXT, and Markdown files
- **AI-Powered Q&A**: Ask questions about your study materials and get contextual answers
- **Source Citations**: Get references to specific documents and content snippets
- **💡Study Tips**: Receive  study recommendations based on your questions
- **Fast API Backend**: RESTful API built with FastAPI
- **Web Frontend**: Simple HTML frontend
- **Vector Search**: Document retrieval using ChromaDB

## Architecture

```
studybuddy-rag-assistant/
├── src/studybuddy/           # Main package
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── models/              # Pydantic models
│   ├── core/                # RAG engine logic
│   ├── api/                 # API routes and dependencies
│   └── utils/               # Utility functions
├── documents/               # Upload your study materials here
├── vector_db/              # ChromaDB vector storage
├── frontend.html           # Web interface
└── pyproject.toml          # Python package configuration
```

## Quick Start

### Prerequisites

- Python 3.9+
- Poetry (for dependency management)
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd studybuddy-rag-assistant
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

4. **Add your study materials**
   ```bash
   # Place your PDF, TXT, or MD files in the documents/ folder
   cp your_study_materials.pdf documents/
   ```

5. **Run the application**
   ```bash
   # Start the development server
   poetry run dev
   
   # Or run directly
   poetry run uvicorn studybuddy.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the application**
   - API Documentation: http://localhost:8000/docs
   - Web Interface: Open `frontend.html` in your browser
   - Health Check: http://localhost:8000/api/v1/health

## Usage

### Web Interface

1. Open `frontend.html` in your web browser
2. Type your question in the chat interface
3. Get AI-powered answers with source citations and study tips

### API Endpoints

#### Chat with StudyBuddy
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "What are the main concepts in machine learning?",
       "include_sources": true,
       "max_sources": 3
     }'
```

#### Upload Documents
```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
     -F "file=@your_document.pdf"
```

#### Health Check
```bash
curl "http://localhost:8000/api/v1/health"
```

## Configuration

Configure the application by setting environment variables or modifying `src/studybuddy/config.py`:

| Variable | Default | Description |
|----------|---------|-------------|
| `STUDYBUDDY_OPENAI_API_KEY` | - | Your OpenAI API key (required) |
| `STUDYBUDDY_OPENAI_MODEL` | `gpt-4o-mini` | OpenAI model to use |
| `STUDYBUDDY_CHUNK_SIZE` | `1000` | Document chunk size for processing |
| `STUDYBUDDY_MAX_SOURCES` | `3` | Maximum source documents to return |
| `STUDYBUDDY_DEBUG` | `false` | Enable debug mode |

## 📁 Supported File Types

- **PDF** (`.pdf`) - Research papers, textbooks, lecture notes
- **Text** (`.txt`) - Plain text documents
- **Markdown** (`.md`) - Formatted notes and documentation

## How It Works

1. **Document Processing**: Your documents are split into chunks and converted into vector embeddings
2. **Vector Storage**: Embeddings are stored in ChromaDB for efficient similarity search
3. **Question Processing**: When you ask a question, the system finds the most relevant document chunks
4. **Answer Generation**: OpenAI's GPT model generates contextual answers based on retrieved content
5. **Study Tips**: Additional AI-generated study recommendations are provided

## 🔧 Development

### Project Structure

```python
src/studybuddy/
├── __init__.py
├── main.py                 # FastAPI app with lifespan management
├── config.py              # Pydantic settings with environment variables
├── models/
│   ├── requests.py        # ChatRequest, DocumentUploadRequest
│   └── responses.py       # ChatResponse, SourceDocument, etc.
├── core/
│   └── rag_engine.py      # StudyBuddyRAG class with core logic
├── api/
│   ├── dependencies.py    # FastAPI dependency injection
│   └── routes/
│       ├── health.py      # Health check endpoints
│       ├── chat.py        # Chat endpoints
│       └── documents.py   # Document upload endpoints
└── utils/
    └── document_processor.py
```

### Key Components

- **StudyBuddyRAG**: Core RAG engine handling document processing and question answering
- **FastAPI App**: REST API with automatic OpenAPI documentation
- **Pydantic Models**: Type-safe request/response models
- **ChromaDB**: Vector database for document embeddings
- **LangChain**: Framework for building the RAG pipeline

### Running Tests

```bash
# Run tests (when implemented)
poetry run pytest

# Code formatting
poetry run black src/
poetry run isort src/

# Linting
poetry run flake8 src/
```

## 🛠️ Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   ```
   ValueError: OPENAI_API_KEY environment variable is required
   ```
   **Solution**: Set your OpenAI API key in the `.env` file or environment variables (in this repo, I choose to set global environment, hence there is no need for `.env`.

2. **Document Processing Fails**
   ```
   Error processing document.pdf: [Errno 2] No such file or directory
   ```
   **Solution**: Ensure the document is in the `documents/` directory and has a supported file extension.

3. **Vector Database Issues**
   ```
   ChromaDB connection error
   ```
   **Solution**: Clear the `vector_db/` directory and restart the application.

### Performance Tips

- **Chunk Size**: Adjust `chunk_size` in config for your document types (larger for academic papers, smaller for notes)
- **Model Selection**: Use `gpt-4o-mini` for cost efficiency or `gpt-4` for better quality
- **Document Organization**: Group related documents by subject for better retrieval

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Built with following resources

- Built with [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [LangChain](https://langchain.readthedocs.io/) for RAG implementation
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [OpenAI](https://openai.com/) for language model capabilities

---

**Happy Studying! 📚✨**


https://github.com/user-attachments/assets/20af4dda-cdb8-4f7b-a077-126ca5daf4e1



