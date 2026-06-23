"""
LexNigeria - Lightweight RAG Chatbot using Groq API with sklearn embeddings
Improved: sentence-aware chunking, query expansion, retry logic, tighter prompting
Install: pip install groq scikit-learn pypdf python-docx python-dotenv
"""

from groq import Groq
import os
import re
import time
import pickle
from dotenv import load_dotenv
import pypdf
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class LightweightRAGChatbot:
    def __init__(self, api_key):
        """Initialize RAG chatbot with Groq API"""
        self.client = Groq(api_key=api_key)
        self.model_id = 'llama-3.1-70b-versatile'

        self.vectorizer = TfidfVectorizer(
            max_features=8000,
            ngram_range=(1, 3),
            stop_words='english',
            sublinear_tf=True,
            min_df=1,
            max_df=0.95
        )

        self.documents = []
        self.metadatas = []
        self.vectors = None
        self.db_path = "./rag_db"

        os.makedirs(self.db_path, exist_ok=True)
        self._load_database()

        print("RAG system initialized!")

    def _save_database(self):
        db_file = os.path.join(self.db_path, "database.pkl")
        with open(db_file, 'wb') as f:
            pickle.dump({
                'documents': self.documents,
                'metadatas': self.metadatas,
                'vectorizer': self.vectorizer,
                'vectors': self.vectors
            }, f)
        print(f"Database saved to {db_file}")

    def _load_database(self):
        db_file = os.path.join(self.db_path, "database.pkl")
        if os.path.exists(db_file):
            try:
                with open(db_file, 'rb') as f:
                    data = pickle.load(f)
                self.documents = data['documents']
                self.metadatas = data['metadatas']
                self.vectorizer = data['vectorizer']
                self.vectors = data['vectors']
                print(f"Loaded {len(self.documents)} documents from existing database")
            except Exception as e:
                print(f"Could not load existing database: {e}")

    def add_documents(self, texts, metadatas=None):
        if not texts:
            return

        if metadatas is None:
            metadatas = [{"source": f"doc_{i}"} for i in range(len(texts))]

        self.documents.extend(texts)
        self.metadatas.extend(metadatas)

        print("Computing vectors...")
        self.vectors = self.vectorizer.fit_transform(self.documents)
        self._save_database()
        print(f"Added {len(texts)} chunks (Total: {len(self.documents)})")

    def add_text_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self._process_and_add_content(content, file_path)
        except Exception as e:
            print(f"Error reading text file {file_path}: {e}")

    def add_pdf_file(self, file_path):
        try:
            reader = pypdf.PdfReader(file_path)
            content = ""
            for page in reader.pages:
                content += page.extract_text() + "\n"
            self._process_and_add_content(content, file_path)
        except Exception as e:
            print(f"Error reading PDF file {file_path}: {e}")

    def add_docx_file(self, file_path):
        try:
            doc = docx.Document(file_path)
            content = "\n".join([para.text for para in doc.paragraphs])
            self._process_and_add_content(content, file_path)
        except Exception as e:
            print(f"Error reading DOCX file {file_path}: {e}")

    def _process_and_add_content(self, content, source):
        if not content.strip():
            print(f"Warning: Empty content in {source}")
            return
        chunks = self._chunk_text(content)
        if chunks:
            self.add_documents(chunks, [{"source": source}] * len(chunks))

    def load_documents_from_folder(self, folder_path):
        print(f"\nScanning documents in '{folder_path}'...")
        supported_extensions = {
            '.txt': self.add_text_file,
            '.pdf': self.add_pdf_file,
            '.docx': self.add_docx_file
        }

        count = 0
        for root, _, files in os.walk(folder_path):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in supported_extensions:
                    file_path = os.path.join(root, file)
                    print(f"Processing: {file_path}")
                    supported_extensions[ext](file_path)
                    count += 1

        if count == 0:
            print(f"No supported documents found in '{folder_path}'")
        else:
            print(f"\nSuccessfully processed {count} file(s)")

    def _chunk_text(self, text, target_chunk_size=800, overlap_sentences=2):
        """Sentence-aware chunking — no sentence is cut in half"""
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)

        sentence_endings = re.compile(r'(?<=[.!?])\s+(?=[A-Z])')
        sentences = sentence_endings.split(text)

        refined = []
        for s in sentences:
            parts = s.split('\n\n')
            refined.extend([p.strip() for p in parts if p.strip()])
        sentences = refined

        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_len = len(sentence)
            current_chunk.append(sentence)
            current_length += sentence_len

            if current_length >= target_chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = current_chunk[-overlap_sentences:] if len(current_chunk) > overlap_sentences else []
                current_length = sum(len(s) for s in current_chunk)

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return [c for c in chunks if len(c) > 80]

    def _expand_query(self, question):
        """Add legal synonyms to improve TF-IDF recall"""
        expansions = {
            'rights': 'rights freedoms entitlements',
            'president': 'president executive commander-in-chief',
            'senate': 'senate senator upper chamber',
            'governor': 'governor state executive',
            'law': 'law legislation statute act',
            'court': 'court tribunal judiciary judge',
            'election': 'election voting ballot electoral',
            'citizen': 'citizen national person individual',
            'power': 'power authority jurisdiction function',
            'amendment': 'amendment alteration modification',
            'remove': 'remove impeach dismiss recall',
            'qualify': 'qualify eligible requirement qualification',
        }

        expanded = question
        for word, synonyms in expansions.items():
            if word.lower() in question.lower():
                expanded += ' ' + synonyms
        return expanded

    def query(self, question, n_results=5, min_score=0.05):
        """Query the RAG system"""
        try:
            if len(self.documents) == 0:
                return "No documents in the knowledge base. Please add documents first."

            expanded_question = self._expand_query(question)
            question_vector = self.vectorizer.transform([expanded_question])
            similarities = cosine_similarity(question_vector, self.vectors)[0]

            top_indices = np.argsort(similarities)[-n_results:][::-1]
            relevant_docs = [
                (self.documents[i], similarities[i])
                for i in top_indices
                if similarities[i] > min_score
            ]

            if not relevant_docs:
                return (
                    "I could not find relevant sections in the Constitution to answer that question. "
                    "Please try rephrasing, or ask something more specific about the Nigerian Constitution."
                )

            context_parts = []
            for i, (doc, score) in enumerate(relevant_docs, 1):
                context_parts.append(f"[Section {i}]\n{doc}")
            context = "\n\n".join(context_parts)

            prompt = f"""You are LexNigeria, a precise legal assistant specialising in the 1999 Constitution of the Federal Republic of Nigeria (as amended).

Your role:
- Answer questions using ONLY the constitutional text provided below.
- Be accurate, clear, and structured. Use plain language where possible.
- If the answer spans multiple sections, synthesise them clearly.
- If the provided context does not contain enough information to answer the question, say so explicitly — do not speculate or draw from outside knowledge.
- Always ground your answer in the constitutional text. Where relevant, reference the section or provision.

Constitutional Context:
{context}

Question: {question}

Answer:"""

            return self._call_groq_with_retry(prompt)

        except Exception as e:
            return f"An error occurred while processing your question: {e}"

    def _call_groq_with_retry(self, prompt, max_retries=3, delay=2):
        """Call Groq API with automatic retry on rate limit errors"""
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_id,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1024,
                    temperature=0.1,
                )
                return response.choices[0].message.content
            except Exception as e:
                error_str = str(e)
                is_retryable = any(code in error_str for code in ['429', '503', 'rate_limit', 'UNAVAILABLE'])

                if is_retryable and attempt < max_retries - 1:
                    wait = delay * (attempt + 1)
                    print(f"API rate limited. Retrying in {wait}s... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait)
                else:
                    if is_retryable:
                        return (
                            "The service is currently busy. "
                            "Please wait a moment and try your question again."
                        )
                    raise e

    def clear_database(self):
        self.documents = []
        self.metadatas = []
        self.vectors = None
        self._save_database()
        print("Database cleared!")

    def chat(self):
        """Interactive chat loop"""
        print("\n" + "="*60)
        print("LexNigeria — Nigerian Constitution Assistant")
        print("="*60)
        print("Commands: 'quit' to exit | 'count' for doc count | 'clear' to reset")
        print("-" * 60)

        while True:
            question = input("\nYou: ").strip()

            if question.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if question.lower() == 'count':
                print(f"Total chunks in database: {len(self.documents)}")
                continue

            if question.lower() == 'clear':
                confirm = input("Clear all documents? (y/n): ").strip().lower()
                if confirm == 'y':
                    self.clear_database()
                continue

            if not question:
                continue

            try:
                answer = self.query(question)
                print(f"\nLexNigeria: {answer}")
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    print("Starting LexNigeria...")
    load_dotenv()

    API_KEY = os.getenv("GROQ_API_KEY")
    if not API_KEY:
        print("\nGROQ_API_KEY not found in environment")
        API_KEY = input("Enter your Groq API key: ").strip()
        if not API_KEY:
            print("API key is required. Exiting...")
            exit(1)

    chatbot = LightweightRAGChatbot(API_KEY)

    docs_folder = "docs"
    if os.path.exists(docs_folder):
        if len(chatbot.documents) > 0:
            response = input(f"\nFound existing database with {len(chatbot.documents)} chunks. Reload documents? (y/n): ").strip().lower()
            if response == 'y':
                chatbot.clear_database()
                chatbot.load_documents_from_folder(docs_folder)
        else:
            chatbot.load_documents_from_folder(docs_folder)
    else:
        print(f"\nFolder '{docs_folder}' not found. Creating it...")
        os.makedirs(docs_folder)
        response = input("\nContinue without documents? (y/n): ").strip().lower()
        if response != 'y':
            print("Exiting. Add documents and restart!")
            exit(0)

    chatbot.chat()
