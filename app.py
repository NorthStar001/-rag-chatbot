"""
LexNigeria - Nigerian Constitution Intelligence Assistant
Streamlit frontend for the RAG chatbot
Run with: streamlit run app.py
"""

import streamlit as st
import os
import sys
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from main import LightweightRAGChatbot

load_dotenv()

st.set_page_config(
    page_title="NorthStar Assistance",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background-color: #0A0F1E;
    color: #F5F0E8;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    font-size: 15px;
    line-height: 1.6;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header, .stDeployButton { display: none !important; }
.stAppHeader { display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #0D1424;
    border-right: 1px solid #1E2A45;
    padding-top: 0 !important;
}

section[data-testid="stSidebar"] > div {
    padding: 0 !important;
}

/* ── Sidebar inner content ── */
.sidebar-brand {
    padding: 28px 24px 20px;
    border-bottom: 1px solid #1E2A45;
    margin-bottom: 8px;
}

.sidebar-brand-name {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 20px;
    font-weight: 700;
    color: #C9A84C;
    letter-spacing: 0.04em;
    margin-bottom: 2px;
}

.sidebar-brand-sub {
    font-size: 11px;
    color: #4A5568;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 500;
}

.sidebar-section {
    padding: 16px 24px;
    border-bottom: 1px solid #1E2A45;
}

.sidebar-label {
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #4A5568;
    margin-bottom: 12px;
}

.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.stat-key {
    font-size: 12px;
    color: #6B7A9A;
    font-weight: 400;
}

.stat-val {
    font-size: 12px;
    color: #F5F0E8;
    font-weight: 600;
    font-variant-numeric: tabular-nums;
}

.stat-val.gold { color: #C9A84C; }

/* ── Sidebar buttons ── */
section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: transparent;
    border: 1px solid #1E2A45;
    color: #6B7A9A;
    border-radius: 6px;
    padding: 8px 14px;
    font-size: 12px;
    font-weight: 500;
    font-family: 'Inter', system-ui, sans-serif;
    letter-spacing: 0.02em;
    cursor: pointer;
    text-align: left;
    transition: all 0.15s ease;
    margin-bottom: 6px;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #C9A84C;
    color: #C9A84C;
    background: rgba(201, 168, 76, 0.06);
}

/* ── Main area ── */
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Page header ── */
.page-header {
    padding: 32px 48px 0;
    border-bottom: 1px solid #1E2A45;
    margin-bottom: 0;
}

.page-title {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 26px;
    font-weight: 700;
    color: #F5F0E8;
    letter-spacing: -0.01em;
    line-height: 1.2;
}

.page-title span {
    color: #C9A84C;
}

.page-meta {
    font-size: 12px;
    color: #4A5568;
    margin-top: 6px;
    padding-bottom: 20px;
    font-weight: 400;
    letter-spacing: 0.01em;
}

/* ── Empty state ── */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 340px;
    text-align: center;
    padding: 48px;
}

.empty-icon {
    width: 52px;
    height: 52px;
    border: 1px solid #1E2A45;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 20px;
    font-size: 22px;
    color: #C9A84C;
}

.empty-title {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 18px;
    font-weight: 600;
    color: #F5F0E8;
    margin-bottom: 8px;
}

.empty-sub {
    font-size: 13px;
    color: #4A5568;
    max-width: 380px;
    line-height: 1.6;
    margin-bottom: 28px;
}

/* ── Suggestion chips ── */
.chips-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    max-width: 520px;
    margin: 0 auto;
}

.chip {
    background: #0D1424;
    border: 1px solid #1E2A45;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 12px;
    color: #6B7A9A;
    text-align: left;
    cursor: pointer;
    transition: all 0.15s ease;
    line-height: 1.4;
}

.chip:hover {
    border-color: #C9A84C;
    color: #C9A84C;
}

/* ── Chat messages ── */
.chat-area {
    padding: 24px 48px;
    min-height: 300px;
}

.message-wrap {
    margin-bottom: 20px;
}

.message-wrap.user { display: flex; justify-content: flex-end; }
.message-wrap.bot  { display: flex; justify-content: flex-start; }

.message-bubble {
    max-width: 68%;
    padding: 14px 18px;
    border-radius: 12px;
    font-size: 14px;
    line-height: 1.65;
    position: relative;
}

.message-bubble.user {
    background: #1A2340;
    color: #F5F0E8;
    border-top: 2px solid #C9A84C;
    border-bottom-right-radius: 4px;
}

.message-bubble.bot {
    background: #0D1424;
    color: #D8D4CB;
    border: 1px solid #1E2A45;
    border-top: 2px solid #2A3A5C;
    border-bottom-left-radius: 4px;
}

.message-role {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 5px;
    color: #4A5568;
}

.message-bubble.user .message-role { color: #C9A84C; text-align: right; }

/* ── Input bar ── */
.input-bar-wrap {
    padding: 16px 48px 24px;
    border-top: 1px solid #1E2A45;
    background: #0A0F1E;
}

div[data-testid="stTextInput"] input {
    background: #0D1424 !important;
    border: 1px solid #1E2A45 !important;
    border-radius: 8px !important;
    color: #F5F0E8 !important;
    font-family: 'Inter', system-ui, sans-serif !important;
    font-size: 14px !important;
    padding: 12px 16px !important;
    box-shadow: none !important;
    transition: border-color 0.15s ease !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #C9A84C !important;
    box-shadow: 0 0 0 3px rgba(201, 168, 76, 0.08) !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #2E3A55 !important;
}

/* ── Send button ── */
.main .stButton > button {
    background: #C9A84C !important;
    color: #0A0F1E !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    font-family: 'Inter', system-ui, sans-serif !important;
    letter-spacing: 0.04em !important;
    cursor: pointer !important;
    transition: background 0.15s ease !important;
    width: 100% !important;
}

.main .stButton > button:hover {
    background: #B8963E !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: #C9A84C !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0A0F1E; }
::-webkit-scrollbar-thumb { background: #1E2A45; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #2A3A5C; }
</style>
""", unsafe_allow_html=True)


# ── Init chatbot ──
def load_chatbot():
    # Try Streamlit secrets first (for deployed apps), then .env (for local dev)
    api_key = None
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except (FileNotFoundError, KeyError):
        api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key or not api_key.strip():
        return None

    return LightweightRAGChatbot(api_key)


if "messages" not in st.session_state:
    st.session_state.messages = []

chatbot = load_chatbot()

# ── Sidebar ──
app_url = os.getenv("APP_URL") or "https://lexnigeria.streamlit.app"

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-name">NorthStar Assistance</div>
        <div class="sidebar-brand-sub">Document Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">Knowledge Base</div>', unsafe_allow_html=True)

    doc_count = len(chatbot.documents) if chatbot else 0
    st.markdown(f"""
    <div class="stat-row">
        <span class="stat-key">Document chunks</span>
        <span class="stat-val gold">{doc_count:,}</span>
    </div>
    <div class="stat-row">
        <span class="stat-key">Source</span>
        <span class="stat-val">Uploaded document</span>
    </div>
    <div class="stat-row">
        <span class="stat-key">Model</span>
        <span class="stat-val">Llama 3.3 70B</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">Actions</div>', unsafe_allow_html=True)

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()

    if st.button("Clear knowledge base"):
        if chatbot:
            chatbot.clear_database()
            st.success("Knowledge base cleared. Upload a document to start again.")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">Add documents</div>', unsafe_allow_html=True)
    st.caption("Upload a PDF, DOCX, or TXT file to build the active knowledge base.")
    
    uploaded_files = st.file_uploader(
        "Choose files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        key="document_uploader"
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        upload_button_clicked = st.button("Upload to knowledge base", use_container_width=True)
    with col2:
        clear_button_clicked = st.button("Clear selection", use_container_width=True)
    
    if clear_button_clicked:
        st.info("Refresh the page to clear file selection.")
    
    if upload_button_clicked:
        if not chatbot:
            st.error("Assistant unavailable. GROQ_API_KEY is not configured.")
        elif uploaded_files:
            added_count = 0
            failed_count = 0
            for uploaded_file in uploaded_files:
                try:
                    if chatbot.add_uploaded_file(uploaded_file):
                        added_count += 1
                        st.write(f"✓ Added {uploaded_file.name}")
                    else:
                        failed_count += 1
                        st.warning(f"Could not add {uploaded_file.name}")
                except Exception as e:
                    failed_count += 1
                    st.error(f"Error adding {uploaded_file.name}: {str(e)}")

            if added_count > 0:
                st.success(f"✓ Successfully added {added_count} document(s) to the knowledge base.")
        else:
            st.info("📄 Select one or more documents to upload.")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="sidebar-section">
        <div class="sidebar-label">Deployment</div>
        <div class="stat-row">
            <span class="stat-key">Live URL</span>
            <span class="stat-val"><a href="{app_url}" target="_blank" style="color:#C9A84C;text-decoration:none;">Open</a></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-label">Accepted Formats</div>
        <div class="stat-row"><span class="stat-key">PDF</span><span class="stat-val">Supported</span></div>
        <div class="stat-row"><span class="stat-key">DOCX</span><span class="stat-val">Supported</span></div>
        <div class="stat-row"><span class="stat-key">TXT</span><span class="stat-val">Supported</span></div>
    </div>
    """, unsafe_allow_html=True)


# ── Main content ──
st.markdown("""
<div class="page-header">
    <div class="page-title"><span>NorthStar</span> Assistance</div>
    <div class="page-meta">Upload a document and ask questions about it. The assistant works from that document only.</div>
</div>
""", unsafe_allow_html=True)

SUGGESTIONS = [
    "Summarize this document",
    "What are the main points?",
    "List the key decisions or actions",
    "Extract the important dates and names",
    "What should I pay attention to first?",
]

# ── Chat area ──
st.markdown('<div class="chat-area">', unsafe_allow_html=True)

if not st.session_state.messages:
    chips_html = '<div class="chips-grid">'
    for s in SUGGESTIONS:
        chips_html += f'<div class="chip">{s}</div>'
    chips_html += '</div>'

    st.markdown(f"""
    <div class="empty-state">
        <div class="empty-icon">§</div>
        <div class="empty-title">Ask your document</div>
        <div class="empty-sub">
            Upload a PDF, DOCX, or TXT file from the sidebar and ask questions about it.
            The assistant will answer using only that uploaded content.
        </div>
        {chips_html}
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        role_label = "You" if role == "user" else "LexNigeria"
        bubble_class = "user" if role == "user" else "bot"
        st.markdown(f"""
        <div class="message-wrap {bubble_class}">
            <div class="message-bubble {bubble_class}">
                <div class="message-role">{role_label}</div>
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Input bar ──
st.markdown('<div class="input-bar-wrap">', unsafe_allow_html=True)
col1, col2 = st.columns([6, 1])

with col1:
    user_input = st.text_input(
        label="query",
        placeholder="Ask about your uploaded document...",
        label_visibility="collapsed",
        key="user_input"
    )

with col2:
    send = st.button("Send", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Handle input ──
if send and user_input.strip():
    if not chatbot:
        st.error("Assistant unavailable. GROQ_API_KEY is not configured.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner(""):
            response = chatbot.query(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
