import os
from dotenv import load_dotenv

load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_TABLE = "documents"

# LLM Configuration - Groq (free)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Embedding Configuration - sentence-transformers (free, local, no API key)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # 384 dimensions
EMBEDDING_DIMENSION = 384

# RAG Configuration
TOP_K_CHUNKS = 4
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000