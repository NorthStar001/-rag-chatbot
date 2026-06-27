# LexNigeria

LexNigeria is a lightweight retrieval-augmented generation (RAG) chatbot for answering questions about the 1999 Constitution of the Federal Republic of Nigeria. It combines a Streamlit frontend with a Python-based retrieval pipeline and Groq LLM inference to provide grounded, document-based answers.

## What it does

- Accepts questions about the Nigerian Constitution.
- Searches a local knowledge base built from constitutional documents.
- Returns answers grounded in the retrieved text rather than relying on open-ended model memory.
- Supports PDF, DOCX, and TXT uploads directly from the UI.

## Features

- Streamlit web interface with a polished chat experience
- Local document ingestion from the docs folder or direct uploads
- Sentence-aware chunking and TF-IDF retrieval
- Groq API integration for answer generation
- Sidebar summary for document counts and deployment info

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
- docs/ — default source documents
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
   - Optional: `APP_URL=https://your-app-url.streamlit.app`

## Run locally

Start the app with:

```bash
streamlit run app.py
```

## Using the app

- Ask constitutional questions in the chat box.
- Use the sidebar to clear the chat, reload the default documents, or upload your own documents.
- Uploaded PDF, DOCX, and TXT files are added to the knowledge base for future queries.

## Deployment

This app is ready to be deployed on Streamlit Cloud or similar services. Make sure to set the `GROQ_API_KEY` environment variable in your hosting platform.

## Notes

If you encounter issues with folder access, make sure the docs and rag_db directories exist in the project root.
