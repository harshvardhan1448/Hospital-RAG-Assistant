import os
from dotenv import load_dotenv

# Try to load from Streamlit secrets first (for Cloud), then fallback to .env
try:
    import streamlit as st
    SUPABASE_URL = st.secrets.get("SUPABASE_URL")
    SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
except:
    # Fallback to .env file (for local development)
    load_dotenv()
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SUPABASE_TABLE = "documents"

# Embedding Configuration - sentence-transformers (free, local, no API key)
# Using minimal model for Render free tier deployment
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # 22MB, 384 dimensions - lightweight & efficient
EMBEDDING_DIMENSION = 384

# RAG Configuration
TOP_K_CHUNKS = 15  # Use 15 (works with RPC), not 8 or 30
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000