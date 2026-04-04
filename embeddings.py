from typing import List

from sentence_transformers import SentenceTransformer

import config

_model = None


def get_model() -> SentenceTransformer:
    """Load SentenceTransformer lazily so startup stays fast."""
    global _model
    if _model is None:
        print(f"[EMBEDDING] Loading model: {config.EMBEDDING_MODEL}")
        _model = SentenceTransformer(config.EMBEDDING_MODEL)
    return _model


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed a list of strings using SentenceTransformer."""
    if not texts:
        return []
    model = get_model()
    vectors = model.encode(texts, normalize_embeddings=True)
    return vectors.tolist()


def embed_query(query: str) -> List[float]:
    """Embed a single query string."""
    model = get_model()
    vector = model.encode(query, normalize_embeddings=True)
    return vector.tolist()