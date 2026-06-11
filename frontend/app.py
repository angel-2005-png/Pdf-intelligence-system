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
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Sidebar ───────────────────────────────────────────
    with st.sidebar:
        st.markdown("### 📄 DRDO Procurement Manual 2025")
        st.markdown("---")
        st.markdown("""
        <div style='font-size:13px; color:#888; margin-bottom:4px;'>Chunks indexed</div>
        <div style='font-size:22px; font-weight:600; color:#534AB7; margin-bottom:12px;'>1,332</div>

        <div style='font-size:13px; color:#888; margin-bottom:4px;'>Model</div>
        <div style='font-size:16px; font-weight:500; margin-bottom:12px;'>llama-text-embed-v2</div>

        <div style='font-size:13px; color:#888; margin-bottom:4px;'>LLM</div>
        <div style='font-size:16px; font-weight:500; margin-bottom:12px;'>llama-3.1-8b</div>

        <div style='font-size:13px; color:#888; margin-bottom:4px;'>Retrieval</div>
        <div style='font-size:16px; font-weight:500; margin-bottom:12px;'>Pinecone + Score Filter</div>
        """, unsafe_allow_html=True)
    if st.button("🔄 Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ── Chat header ───────────────────────────────────────
st.markdown("""
<div style='padding: 1rem 0; border-bottom: 0.5px solid #e0e0e0; margin-bottom: 1rem;'>
    <h2 style='font-size:20px; font-weight:600; color:093C5D; margin:0;'>
        Ask the DRDO Procurement Manual anything
    </h2>
    <p style='font-size:13px; color:#888; margin:4px 0 0;'>
        Powered by RAG + Groq + Pinecone
    </p>
</div>
""", unsafe_allow_html=True)

# ── Welcome message ───────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class='bot-bubble'>
        Hi! I'm ready to answer questions about the DRDO Procurement Manual 2025. Ask me anything! 👋
    </div>
    """, unsafe_allow_html=True)

# ── Display messages ──────────────────────────────────
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

# ── Chat input ────────────────────────────────────────
question = st.chat_input("Ask a question about the DRDO Procurement Manual...")

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