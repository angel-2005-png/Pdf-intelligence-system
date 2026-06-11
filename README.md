# PDF Intelligence System 

> Ask questions about any technical document using AI

## Live Demo
https://pdf-intelligence-system-obyotp3xoetknirquxsqph.streamlit.app/

## How It Works
PDF → Chunking → Pinecone Vector DB → Retrieval → Groq LLM → Answer

## Tech Stack
- **Backend:** FastAPI + LangChain
- **Vector DB:** Pinecone
- **Embeddings:** llama-text-embed-v2
- **LLM:** Groq (llama-3.1-8b)
- **Frontend:** Streamlit
- **Deployment:** Railway + Streamlit Cloud

## Architecture
User asks question → question embedded → Pinecone similarity search
→ top relevant chunks retrieved → Groq generates answer with citations
