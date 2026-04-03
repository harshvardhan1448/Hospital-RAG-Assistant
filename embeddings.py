from sentence_transformers import SentenceTransformer
import config

_model = None

def get_model() -> SentenceTransformer:
    """Load once, reuse everywhere."""
    global _model
    if _model is None:
        _model = SentenceTransformer(config.EMBEDDING_MODEL)
    return _model

def embed_texts(texts: list) -> list:
    """Embed a list of strings."""
    return get_model().encode(texts, show_progress_bar=False).tolist()

def embed_query(query: str) -> list:
    """Embed a single query string."""
    return get_model().encode([query], show_progress_bar=False)[0].tolist()