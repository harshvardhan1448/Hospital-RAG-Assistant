import os
import requests
from typing import List
import time

# Use Hugging Face Inference API (free, no local model loading needed)
HF_API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
HF_API_KEY = os.getenv("HF_API_KEY", "")  # Optional for higher rate limits

def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed texts using Hugging Face Inference API."""
    if not texts:
        return []
    
    print(f"[EMBEDDING] Starting embedding for {len(texts)} texts")
    
    headers = {}
    if HF_API_KEY:
        headers["Authorization"] = f"Bearer {HF_API_KEY}"
    
    payload = {
        "inputs": texts,
        "options": {"wait_for_model": True}
    }
    
    try:
        print(f"[EMBEDDING] Calling HF API at {HF_API_URL}")
        start_time = time.time()
        response = requests.post(HF_API_URL, json=payload, headers=headers, timeout=120)
        elapsed = time.time() - start_time
        print(f"[EMBEDDING] HF API response: {response.status_code} (took {elapsed:.1f}s)")
        
        response.raise_for_status()
        result = response.json()
        print(f"[EMBEDDING] Successfully embedded {len(texts)} texts")
        return result
    except requests.exceptions.Timeout:
        print(f"[EMBEDDING ERROR] HF API timeout after 120s")
        raise Exception("HF API request timed out. Please try again.")
    except Exception as e:
        print(f"[EMBEDDING ERROR] {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise Exception(f"Failed to generate embeddings: {str(e)}")

def embed_query(query: str) -> List[float]:
    """Embed a single query using Hugging Face Inference API."""
    result = embed_texts([query])
    return result[0] if result else []

def get_model():
    """Dummy function for compatibility - not needed with API."""
    return None