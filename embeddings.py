import hashlib
import math
import re
from typing import List

import config

TOKEN_PATTERN = re.compile(r"[A-Za-z0-9]+")


def _tokenize(text: str) -> List[str]:
    return TOKEN_PATTERN.findall(text.lower())


def _hash_token(token: str) -> int:
    digest = hashlib.sha256(token.encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big") % config.EMBEDDING_DIMENSION


def _build_embedding(text: str) -> List[float]:
    vector = [0.0] * config.EMBEDDING_DIMENSION
    tokens = _tokenize(text)

    if not tokens:
        return vector

    for token in tokens:
        vector[_hash_token(token)] += 1.0

    norm = math.sqrt(sum(value * value for value in vector))
    if norm:
        vector = [value / norm for value in vector]

    return vector


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed a list of strings using a local deterministic hashing vectorizer."""
    print(f"[EMBEDDING] Using local hashing embedder for {len(texts)} texts")
    return [_build_embedding(text) for text in texts]


def embed_query(query: str) -> List[float]:
    """Embed a single query string."""
    return _build_embedding(query)


def get_model():
    """Compatibility hook for the previous embedding interface."""
    return None