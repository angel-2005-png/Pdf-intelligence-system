import streamlit as st
import requests

BACKEND_URL = "https://pdf-intelligence-system-production.up.railway.app"

# ── Page config ───────────────────────────────────────
st.set_page_config(
    page_title="PDF Intelligence",
    page_icon="📄",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .main { background: #f8f8fc; }

    .feature-card {
        background: white;
        border: 0.5px solid #e0e0e0;
        border-radius: 12px;
        padding: 1rem;
    }
    .user-bubble {
        background: #534AB7;
        color: #EEEDFE !important;
        padding: 10px 14px;
        border-radius: 12px 12px 4px 12px;
        margin: 4px 0;
        max-width: 75%;
        margin-left: auto;
        font-size: 14px;
        line-height: 1.6;
    }
    .bot-bubble {
        background: white;
        border: 0.5px solid #e0e0e0;
        padding: 10px 14px;
        border-radius: 12px 12px 12px 4px;
        margin: 4px 0;
        max-width: 75%;
        font-size: 14px;
        line-height: 1.6;
        color: #1a1a2e !important; 
    }
    .source-chip {
        display: inline-block;
        background: #f5f5f5;
        border: 0.5px solid #e0e0e0;
        border-radius: 999px;
        padding: 2px 10px;
        font-size: 11px;
        color: #666;
        margin: 2px;
    }
    .sidebar-stat {
        background: #f5f5f5;
        border-radius: 8px;
        padding: 8px 12px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────
if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "filename" not in st.session_state:
    st.session_state.filename = ""
if "total_chunks" not in st.session_state:
    st.session_state.total_chunks = 0

# ─────────────────────────────────────────────────────
# WELCOME SCREEN
# ─────────────────────────────────────────────────────
if not st.session_state.pdf_uploaded:

    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
        <div style='text-align:center; padding: 2rem;'>
            <div style='width:72px; height:72px; background:#EEEDFE; border-radius:16px;
                        margin: 0 auto 1.5rem; font-size:36px; line-height:72px;'>📄</div>
            <h1 style='font-size:28px; font-weight:600; color:8A5F41; margin-bottom:8px;'>
                Welcome to PDF Intelligence
            </h1>
            <p style='color:#888; font-size:15px; line-height:1.6; margin-bottom:2rem;'>
                Upload any technical manual and ask questions in plain English.
                Get instant answers with source citations.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # ── Feature cards ──────────────────────────────
        f1, f2, f3 = st.columns(3)

        with f1:
            st.markdown("""
            <div class='feature-card'>
                <div style='font-size:22px; margin-bottom:8px;'>🔍</div>
                <div style='font-size:13px; font-weight:600; color:#1a1a2e;'>Smart Retrieval</div>
                <div style='font-size:12px; color:#888; margin-top:4px;'>Finds the most relevant sections instantly</div>
            </div>
            """, unsafe_allow_html=True)

        with f2:
            st.markdown("""
            <div class='feature-card'>
                <div style='font-size:22px; margin-bottom:8px;'>💬</div>
                <div style='font-size:13px; font-weight:600; color:#1a1a2e;'>Plain English</div>
                <div style='font-size:12px; color:#888; margin-top:4px;'>Ask naturally, get clear answers</div>
            </div>
            """, unsafe_allow_html=True)

        with f3:
            st.markdown("""
            <div class='feature-card'>
                <div style='font-size:22px; margin-bottom:8px;'>📎</div>
                <div style='font-size:13px; font-weight:600; color:#1a1a2e;'>Source Cited</div>
                <div style='font-size:12px; color:#888; margin-top:4px;'>Every answer links back to the page</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── File uploader ──────────────────────────────
        uploaded_file = st.file_uploader(
            "Upload your PDF",
            type="pdf",
            label_visibility="collapsed"
        )

        if uploaded_file:
            with st.spinner("⚙️ Indexing your PDF... this may take a moment"):
                response = requests.post(
                    f"{BACKEND_URL}/upload",
                    files={"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                )
                print(response.status_code)  # ← add this
                print(response.text)  # ← add this
                data = response.json()

            if response.status_code == 200:
                st.session_state.pdf_uploaded = True
                st.session_state.filename = uploaded_file.name
                st.session_state.total_chunks = data["No.of Chunks"]
                st.rerun()
            else:
                st.error("Something went wrong. Please try again.")

# ─────────────────────────────────────────────────────
# CHAT SCREEN
# ─────────────────────────────────────────────────────
else:

    # ── Sidebar ────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"### 📄 {st.session_state.filename}")
        st.markdown("---")

        st.metric("Chunks indexed", f"{st.session_state.total_chunks:,}")
        st.metric("Model", "llama-3.1-8b-instant")
        st.metric("Retrieval", "MMR + Score Filter")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🔄 Upload new PDF", use_container_width=True):
            st.session_state.pdf_uploaded = False
            st.session_state.messages = []
            st.session_state.filename = ""
            st.session_state.total_chunks = 0
            st.rerun()

    # ── Chat header ────────────────────────────────────
    st.markdown("""
    <div style='padding: 1rem 0; border-bottom: 0.5px solid #e0e0e0; margin-bottom: 1rem;'>
        <h2 style='font-size:20px; font-weight:600; color:8A5F41; margin:0;'>
            Ask your manual anything
        </h2>
        <p style='font-size:13px; color:#888; margin:4px 0 0;'>
            Powered by RAG + Groq
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Welcome bot message ────────────────────────────
    if not st.session_state.messages:
        st.markdown("""
        <div class='bot-bubble'>
            Hi! I've indexed your manual. Ask me anything about it 👋
        </div>
        """, unsafe_allow_html=True)

    # ── Display messages ───────────────────────────────
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f"<div class='user-bubble'>{msg['content']}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='bot-bubble'>{msg['content']}</div>",
                unsafe_allow_html=True
            )
            if "sources" in msg and msg["sources"]:
                chips = "".join([
                    f"<span class='source-chip'>📄 Page {s}</span>"
                    for s in sorted(msg["sources"])
                ])
                st.markdown(chips, unsafe_allow_html=True)

    # ── Chat input ─────────────────────────────────────
    question = st.chat_input("Ask a question about your manual...")

    if question:
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.spinner("Thinking..."):
            response = requests.post(
                f"{BACKEND_URL}/ask",
                json={"question": question}
            )
            data = response.json()

        st.session_state.messages.append({
            "role": "assistant",
            "content": data["answer"],
            "sources": data.get("sources", [])
        })

        st.rerun()