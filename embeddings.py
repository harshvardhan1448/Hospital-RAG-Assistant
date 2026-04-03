import os
import requests
from typing import List

# Use Hugging Face Inference API (free, no local model loading needed)
HF_API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
HF_API_KEY = os.getenv("HF_API_KEY", "")  # Optional for higher rate limits

def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed texts using Hugging Face Inference API."""
    if not texts:
        return []
    
    headers = {}
    if HF_API_KEY:
        headers["Authorization"] = f"Bearer {HF_API_KEY}"
    
    payload = {
        "inputs": texts,
        "options": {"wait_for_model": True}
    }
    
    try:
        response = requests.post(HF_API_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[EMBEDDING] Error: {str(e)}")
        raise Exception(f"Failed to generate embeddings: {str(e)}")

def embed_query(query: str) -> List[float]:
    """Embed a single query using Hugging Face Inference API."""
    result = embed_texts([query])
    return result[0] if result else []

def get_model():
    """Dummy function for compatibility - not needed with API."""
    return None