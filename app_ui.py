import streamlit as st
import requests
import json
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Hospital RAG Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    .answer-box {
        background-color: #e8f5e9;
        padding: 15px;
        border-left: 4px solid #4caf50;
        border-radius: 5px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #ffebee;
        padding: 15px;
        border-left: 4px solid #f44336;
        border-radius: 5px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 15px;
        border-left: 4px solid #2196f3;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== Configuration ====================

try:
    API_BASE_URL = st.secrets.get("API_BASE_URL", os.getenv("API_BASE_URL", "http://localhost:8000"))
except Exception:
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# ==================== Helper Functions ====================

def upload_document(uploaded_file) -> dict:
    """Upload document to backend API"""
    try:
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type or "application/pdf",
            )
        }
        print(f"[UI] Uploading {uploaded_file.name} to {API_BASE_URL}/upload")
        response = requests.post(
            f"{API_BASE_URL}/upload",
            files=files,
            timeout=120
        )
        print(f"[UI] Upload response: {response.status_code} {response.text[:500]}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"status": "error", "message": f"Cannot connect to API at {API_BASE_URL}"}
    except Exception as e:
        print(f"[UI] Upload error: {type(e).__name__}: {e}")
        return {"status": "error", "message": str(e)}


def query_documents(question: str) -> dict:
    """Query documents via backend API"""
    try:
        payload = {"question": question}
        response = requests.post(
            f"{API_BASE_URL}/query",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"status": "error", "answer": f"Cannot connect to API at {API_BASE_URL}"}
    except Exception as e:
        return {"status": "error", "answer": str(e)}


def get_documents() -> list:
    """Get list of stored documents"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/documents",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except:
        return []


def delete_document(filename: str) -> dict:
    """Delete a document"""
    try:
        response = requests.delete(
            f"{API_BASE_URL}/documents/{filename}",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ==================== Session State ====================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []


# ==================== Main UI ====================

# Header
st.markdown("""
<div class="main-header">
    <h1>🏥 Hospital RAG Assistant</h1>
    <p>AI-powered document assistant that answers questions using hospital documents</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    api_url = st.text_input(
        "API Base URL",
        value=API_BASE_URL,
        help="URL where the FastAPI backend is running"
    )
    
    if api_url != API_BASE_URL:
        API_BASE_URL = api_url

    st.caption(f"Resolved API: {API_BASE_URL}")
    
    st.divider()
    
    st.header("📤 Document Upload")
    uploaded_file = st.file_uploader(
        "Upload Hospital Document (PDF)",
        type=["pdf"],
        help="Upload a PDF document to be indexed and searched"
    )
    
    if uploaded_file is not None:
        if st.button("📤 Upload Document", use_container_width=True):
            with st.spinner("Uploading and processing document..."):
                st.write(f"Uploading to: {API_BASE_URL}/upload")
                result = upload_document(uploaded_file)
                st.write(result)
                
                if result["status"] == "success":
                    st.success(f"✓ Document uploaded successfully!")
                    st.info(f"📄 Pages: {result['pages']} | Chunks: {result['chunks']}")
                    st.session_state.uploaded_files.append(result["filename"])
                else:
                    st.error(f"✗ Upload failed: {result.get('message', 'Unknown error')}")
    
    st.divider()
    
    st.header("📋 Uploaded Documents")
    documents = get_documents()
    
    if documents:
        # Group documents by filename
        doc_groups = {}
        for doc in documents:
            filename = doc.get("filename", "Unknown")
            if filename not in doc_groups:
                doc_groups[filename] = 0
            doc_groups[filename] += 1
        
        for filename, count in doc_groups.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text(f"📄 {filename}")
                st.caption(f"{count} chunks")
            with col2:
                if st.button("🗑️ Delete", key=f"del_{filename}", use_container_width=True):
                    result = delete_document(filename)
                    if result["status"] == "success":
                        st.success("Document deleted!")
                        st.rerun()
                    else:
                        st.error(f"Error: {result.get('message')}")
    else:
        st.info("📂 No documents uploaded yet")


# Main content
st.header("💬 Ask Questions")

# Chat history display
if st.session_state.chat_history:
    st.subheader("Chat History")
    for i, (question, response) in enumerate(st.session_state.chat_history):
        with st.expander(f"Q{i+1}: {question[:60]}..." if len(question) > 60 else f"Q{i+1}: {question}"):
            st.write(f"**Question:** {question}")
            st.markdown("<div class='answer-box'>", unsafe_allow_html=True)
            st.write(f"**Answer:** {response['answer']}")
            if response.get('sources'):
                st.caption(f"📍 Sources: {', '.join(response['sources'])}")
            st.markdown("</div>", unsafe_allow_html=True)


# Query input
col1, col2 = st.columns([5, 1])

with col1:
    question = st.text_input(
        "Enter your question about the hospital document:",
        placeholder="e.g., What are the OPD timings?",
        label_visibility="collapsed"
    )

with col2:
    search_button = st.button("🔍 Ask", use_container_width=True, type="primary")

# Process query
if search_button and question:
    with st.spinner("🤖 Searching and generating answer..."):
        response = query_documents(question)
        
        if response["status"] == "success":
            # Add to chat history
            st.session_state.chat_history.insert(0, (question, response))
            
            # Display answer
            st.markdown("<div class='answer-box'>", unsafe_allow_html=True)
            st.subheader("✓ Answer")
            st.write(response["answer"])
            
            if response.get("sources"):
                st.caption(f"📍 **Sources:** {', '.join(response['sources'])}")
            
            st.caption(f"📊 {response.get('chunks_found', 0)} relevant chunks retrieved")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Show retrieved chunks
            if response.get("chunks"):
                with st.expander("📌 View Retrieved Chunks"):
                    for i, chunk in enumerate(response["chunks"], 1):
                        similarity = chunk.get("similarity", 0)
                        st.markdown(f"**Chunk {i}** (Page: {chunk.get('page', 'Unknown')} | Similarity: {similarity:.4f})")
                        st.text(chunk["content"][:300] + "..." if len(chunk["content"]) > 300 else chunk["content"])
                        st.divider()
        
        else:
            st.markdown("<div class='error-box'>", unsafe_allow_html=True)
            st.error(f"✗ Error: {response.get('answer', 'Unknown error')}")
            st.markdown("</div>", unsafe_allow_html=True)

elif search_button and not question:
    st.warning("Please enter a question first!")


# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #888; font-size: 12px; margin-top: 40px;'>
    <p>🏥 Hospital RAG Assistant | Powered by LangChain, Supabase, and Groq</p>
    <p>This system answers questions ONLY based on uploaded hospital documents</p>
</div>
""", unsafe_allow_html=True)
