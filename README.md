# NorthStar Assistance

NorthStar Assistance is a document-grounded chat application that helps users ask questions about a single uploaded document using a lightweight retrieval-augmented generation (RAG) pipeline. The project combines a Streamlit-based interface with Python document processing and Groq-powered language model inference to deliver answers that are grounded in the uploaded content.

## Overview

This repository provides a practical example of building a focused document assistant for legal, academic, or business use cases where answers should stay tightly tied to a specific source document. Instead of relying on general knowledge, the system retrieves the most relevant passages from the provided document and uses them as context for the model.

## Key Features

- Upload and analyze PDF, DOCX, and TXT documents directly through the web app
- Build a local knowledge base from the uploaded content
- Perform semantic-style retrieval using TF-IDF vector search
- Split documents into sentence-aware chunks to preserve context
- Generate answers with Groq LLM inference while grounding responses in the document
- Clear the current knowledge base from the sidebar when starting a new session
- Persist the processed database locally in the repository’s data folder

## Technologies Used

- Python
- Streamlit
- Groq API
- scikit-learn
- pypdf
- python-docx
- python-dotenv
- NumPy

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/NorthStar001/-rag-chatbot.git
   cd -rag-chatbot
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your environment:
   Create a `.env` file in the project root with your Groq API key:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

   If you deploy the app on Streamlit Cloud, you can also configure this value in Streamlit secrets.

## Usage

Run the application locally:

```bash
streamlit run app.py
```

Then:
- Open the app in your browser
- Upload a supported document from the sidebar
- Ask a question about that document
- Review the answer generated from the retrieved content

## Example Workflow

```text
1. Upload a PDF or TXT file
2. The app processes the document into chunks
3. The retrieval layer finds the most relevant sections
4. The LLM generates an answer grounded in those sections
```

## Project Structure

```text
app.py                # Streamlit user interface and app wiring
main.py               # RAG pipeline, document ingestion, retrieval, and Groq integration
requirements.txt     # Python dependencies
rag_db/               # Local storage for the processed knowledge base
.env.example         # Example environment variable file
```

## Configuration Requirements

- A valid Groq API key is required for answer generation
- The application expects the key to be available through either:
  - a `.env` file locally, or
  - Streamlit secrets in a deployed environment
- Optional environment variable support exists for app URL configuration during deployment

## Roadmap

Potential future improvements include:
- Support for multi-document conversations and cross-document retrieval
- Source citation and highlighted evidence in responses
- Conversation memory for follow-up questions
- Better chunking and ranking strategies for larger documents
- A more advanced UI for document management and chat history

## Author

Maintained by NorthStar001.
