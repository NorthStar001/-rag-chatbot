# NorthStar Assistance

NorthStar Assistance is a lightweight document-based assistant powered by a Streamlit frontend, a Python retrieval pipeline, and Groq LLM inference. It is designed to answer questions from a single uploaded document at a time, keeping the knowledge source focused and avoiding cross-document confusion.

## What it does

- Accepts questions about a document uploaded by the user.
- Builds a temporary knowledge base from that uploaded file.
- Returns answers grounded strictly in the uploaded document content.
- Supports PDF, DOCX, and TXT uploads directly from the UI.

## Features

- Streamlit web interface with a polished chat experience
- Uploaded-document-only knowledge mode
- Sentence-aware chunking and TF-IDF retrieval
- Groq API integration for answer generation
- Sidebar controls for clearing the knowledge base and managing the session

## Tech stack

- Python
- Streamlit
- Groq
- scikit-learn
- pypdf
- python-docx
- python-dotenv

## Project structure

- app.py — Streamlit frontend
- main.py — chatbot logic and document ingestion
- rag_db/ — serialized knowledge base cache

## Setup

1. Clone the repository.
2. Create and activate a virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
3. Install dependencies:
   - `pip install -r requirements.txt`
4. Create a `.env` file with your Groq API key:
   - `GROQ_API_KEY=your_key_here`

## Run locally

Start the app with:

```bash
streamlit run app.py
```

## Using the app

- Upload a PDF, DOCX, or TXT file from the sidebar.
- Ask questions about that uploaded document.
- The assistant will answer using only that document’s content.
- Use the sidebar to clear the current knowledge base and start fresh.

## Notes

This version is intentionally document-first. It does not rely on any preloaded default knowledge base, so uploaded content is the only active source for responses.
