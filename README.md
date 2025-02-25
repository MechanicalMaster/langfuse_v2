# Policy Chatbot with FAISS-Based Retrieval and Observability

## Overview

This project is a memory-persistent chatbot that retrieves answers from a FAISS vector store populated with embeddings from uploaded policy documents. The chatbot maintains conversation context using LangChain and LangGraph, and provides observability through Langfuse. The system includes a simple web-based frontend for chatting and a dedicated page for uploading policy documents.

## Features

- **Conversational Flow**: Persistent memory and multi-turn conversation using LangChain and LangGraph.
- **FAISS Vector Store**: Efficient similarity search for policy document embeddings.
- **Document Upload**: Upload `.txt` policy documents (max 25KB) to populate the FAISS store.
- **Observability**: Integration with Langfuse for logging, monitoring, and performance tracking.
- **Minimalist Web Interface**: Simple chat interface with dark/light mode and message timestamps.

## Project Structure

```
.env.example
.gitignore
app/__init__.py
app/api/__init__.py
app/api/chat.py
app/api/documents.py
app/api/models.py
app/core/config.py
app/core/observability.py
app/core/security.py
app/main.py
app/services/chat_service.py
app/services/document_service.py
app/services/vector_store.py
app/static/css/style.css
app/static/index.html
app/static/js/main.js
app/static/js/upload.js
app/static/policy.html
code.md
plan.md
project_structure.md
railway.toml
requirements.txt
spec.md
```

## Core Components

### 1. **Vector Store Service (`vector_store.py`)**
- Uses FAISS for efficient similarity search.
- Manages document embeddings using OpenAI.
- Handles persistent storage of FAISS indices.

### 2. **Chat Service (`chat_service.py`)**
- Manages conversation state and context.
- Integrates with Langfuse for observability.
- Uses LangChain for chat prompt management and LLM interactions.

### 3. **Document Processing**
- Supports `.txt` file uploads (max 25KB).
- Chunks documents for better retrieval.
- Stores metadata with each chunk.

### 4. **Frontend Components**
- **Chat Interface**: Real-time message updates, dark/light mode, and message timestamps.
- **Upload Interface**: Drag & drop support, progress indicators, and file validation.

### 5. **API Layer**
- RESTful endpoints for chat interactions and document uploads.
- Error handling middleware and CORS support.

## Technology Stack

- **Backend**: FastAPI
- **LLM Integration**: LangChain
- **Vector Store**: FAISS
- **Embeddings & Chat**: OpenAI
- **Observability**: Langfuse

## Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key
- Langfuse API keys

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/policy-chatbot.git
   cd policy-chatbot
   ```

2. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file based on `.env.example` and populate it with your API keys:
   ```bash
   cp .env.example .env
   ```

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Access the chat interface at `http://localhost:8000` and the upload interface at `http://localhost:8000/static/policy.html`.

## Usage

### Chat Interface

- **Send Messages**: Type your message in the input box and press Enter or click the Send button.
- **Dark/Light Mode**: Toggle the theme using the theme toggle button.
- **Upload Policy**: Navigate to the upload page to upload policy documents.

### Upload Interface

- **Upload Policy Documents**: Drag & drop or click to upload `.txt` files (max 25KB).
- **Validation**: The system will validate file type and size before processing.

## Observability

The system integrates with Langfuse for observability. All interactions, including file uploads and chat queries, are logged with metadata for performance monitoring and debugging.

## Deployment

The project can be deployed using Docker. A `railway.toml` file is provided for deployment on Railway.

```bash
docker build -t policy-chatbot .
docker run -p 8000:8000 policy-chatbot
```

## Documentation

- **API Documentation**: Available in the `spec.md` file.
- **Implementation Plan**: Detailed in `plan.md`.
- **Code Summary**: Overview of the codebase in `code.md`.

## Future Enhancements

- **Enhanced Retrieval**: Explore advanced retrieval strategies (e.g., combining keyword and vector-based search).
- **Scalability**: Improve the system to handle larger documents and more concurrent users.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Note**: This project is for educational and demonstration purposes. Ensure you handle API keys and sensitive information securely.
