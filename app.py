"""
Streamlit Frontend for Lightweight RAG Chatbot
Run with: streamlit run app.py
"""

import streamlit as st
import os
from dotenv import load_dotenv
from main import LightweightRAGChatbot

# Load environment variables
load_dotenv()

# --- Page Config ---
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="centered"
)

# --- Custom CSS ---
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0f1117;
        color: #e0e0e0;
    }

    /* Chat message bubbles */
    .user-bubble {
        background-color: #1e3a5f;
        color: #e0e0e0;
        padding: 12px 16px;
        border-radius: 16px 16px 4px 16px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        font-size: 15px;
    }

    .bot-bubble {
        background-color: #1c1f2b;
        color: #e0e0e0;
        padding: 12px 16px;
        border-radius: 16px 16px 16px 4px;
        margin: 8px 0;
        max-width: 80%;
        border-left: 3px solid #4a9eff;
        font-size: 15px;
    }

    /* Header */
    .chat-header {
        text-align: center;
        padding: 20px 0 10px 0;
    }

    .chat-header h1 {
        color: #4a9eff;
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    .chat-header p {
        color: #888;
        font-size: 0.9rem;
    }

    /* Status badge */
    .status-badge {
        display: inline-block;
        background-color: #1a3a1a;
        color: #4caf50;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin-bottom: 16px;
    }

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Input box */
    .stTextInput > div > div > input {
        background-color: #1c1f2b;
        color: #e0e0e0;
        border: 1px solid #2d3348;
        border-radius: 10px;
    }

    /* Button */
    .stButton > button {
        background-color: #4a9eff;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 8px 20px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #3a8eef;
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: #1c1f2b;
    }
</style>
""", unsafe_allow_html=True)


# --- Initialize Chatbot ---
@st.cache_resource
def load_chatbot():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    chatbot = LightweightRAGChatbot(api_key)
    docs_folder = "docs"
    if os.path.exists(docs_folder) and len(chatbot.documents) == 0:
        chatbot.load_documents_from_folder(docs_folder)
    return chatbot


# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []


# --- Header ---
st.markdown("""
<div class="chat-header">
    <h1>🤖 RAG Chatbot</h1>
    <p>Ask anything about your documents</p>
</div>
""", unsafe_allow_html=True)


# --- Sidebar ---
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")

    chatbot = load_chatbot()

    if chatbot:
        doc_count = len(chatbot.documents)
        st.markdown(f"**📄 Document chunks:** `{doc_count}`")
        st.markdown(f"**🧠 Model:** `gemini-2.5-flash`")
        st.markdown("---")

        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

        if st.button("🔄 Reload Documents"):
            chatbot.clear_database()
            chatbot.load_documents_from_folder("docs")
            st.success("Documents reloaded!")
            st.rerun()
    else:
        st.error("❌ GEMINI_API_KEY not found in .env file")

    st.markdown("---")
    st.markdown("**Supported formats:**")
    st.markdown("📄 PDF &nbsp; 📝 TXT &nbsp; 📃 DOCX")
    st.markdown("<small style='color:#666'>Place files in the `docs/` folder</small>", unsafe_allow_html=True)


# --- Chat Area ---
chat_container = st.container()

with chat_container:
    if not st.session_state.messages:
        st.markdown("""
        <div style='text-align:center; color:#555; padding: 40px 0;'>
            <div style='font-size: 3rem;'>💬</div>
            <p>Ask a question about your documents to get started.</p>
        </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-bubble">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-bubble">🤖 {msg["content"]}</div>', unsafe_allow_html=True)


# --- Input ---
st.markdown("---")
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        label="message",
        placeholder="Ask something about your documents...",
        label_visibility="collapsed",
        key="user_input"
    )

with col2:
    send = st.button("Send", use_container_width=True)

# --- Handle Send ---
if send and user_input.strip():
    chatbot = load_chatbot()

    if not chatbot:
        st.error("Chatbot not initialized. Check your GEMINI_API_KEY in .env")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Thinking..."):
            response = chatbot.query(user_input)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
