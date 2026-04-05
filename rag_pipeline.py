import re
from typing import List, Dict, Tuple
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from embeddings import embed_query
from supabase_db import get_supabase_manager
import config


TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> set[str]:
    return set(TOKEN_PATTERN.findall((text or "").lower()))


def _is_timing_query(query: str) -> bool:
    q = (query or "").lower()
    keywords = {
        "time", "timing", "timings", "hours", "schedule", "open", "close",
        "opd", "clinic", "monday", "tuesday", "wednesday", "thursday",
        "friday", "saturday", "sunday"
    }
    tokens = _tokenize(q)
    return bool(tokens.intersection(keywords))


def _expand_query(query: str) -> List[str]:
    """Generate query variants with common medical synonyms for better retrieval."""
    variants = [query]
    q_lower = query.lower()
    
    # Synonym mappings for medical terms
    synonyms = {
        "timing": ["hour", "hours", "time"],
        "timings": ["hours", "time", "schedule"],
        "opd": ["outpatient", "outpatient department", "clinic"],
        "closed": ["not available", "unavailable", "open"],
        "available": ["open", "active", "operating"]
    }
    
    for word, alternatives in synonyms.items():
        if word in q_lower:
            for alt in alternatives:
                variants.append(q_lower.replace(word, alt))
    
    return list(set(variants))  # Remove duplicates


def _rerank_chunks(query: str, chunks: List[dict]) -> List[dict]:
    """Combine vector similarity with token overlap for more stable top results."""
    query_tokens = _tokenize(query)
    scored = []
    
    # For timing queries, weight lexical overlap more heavily
    is_timing = _is_timing_query(query)
    vector_weight = 0.6 if is_timing else 0.8
    overlap_weight = 0.4 if is_timing else 0.2

    for chunk in chunks:
        similarity = float(chunk.get("similarity", 0) or 0)
        chunk_tokens = _tokenize(chunk.get("content", ""))
        
        # Calculate overlap as a ratio of query tokens found
        overlap_score = len(query_tokens.intersection(chunk_tokens)) / max(len(query_tokens), 1)
        
        # Combined score with timing-aware weighting
        score = (vector_weight * similarity) + (overlap_weight * overlap_score)
        scored.append((score, chunk))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [item[1] for item in scored]


def get_query_embedding(query: str) -> list:
    return embed_query(query)


def get_llm_client() -> ChatGroq:
    return ChatGroq(
        model="llama-3.1-8b-instant",   # <-- updated model
        api_key=config.GROQ_API_KEY,
        temperature=0.3
    )

async def retrieve_relevant_chunks(query: str, k: int = config.TOP_K_CHUNKS) -> List[dict]:
    """Retrieve top-k most relevant document chunks for the query.
    
    If initial retrieval yields low-confidence results for timing queries,
    tries expanded query variants for better matching.
    """
    try:
        query_embedding = get_query_embedding(query)
        supabase = get_supabase_manager()
        chunks = await supabase.similarity_search(query_embedding, k=k)
        reranked = _rerank_chunks(query, chunks)
        
        # For timing queries with poor results, try expanded variants
        if _is_timing_query(query) and reranked:
            best_score = float(reranked[0].get("similarity", 0) or 0)
            if best_score < 0.5:  # Low confidence threshold
                print(f"[DEBUG] Low confidence ({best_score:.3f}) for timing query, trying expansions...")
                variants = _expand_query(query)
                all_chunks = dict()  # Deduplicate by content
                
                for variant in variants:
                    if variant == query:
                        continue  # Already tried
                    var_embedding = get_query_embedding(variant)
                    var_chunks = await supabase.similarity_search(var_embedding, k=k)
                    for chunk in var_chunks:
                        key = chunk["content"][:100]  # Use content prefix as key
                        if key not in all_chunks or chunk.get("similarity", 0) > all_chunks[key].get("similarity", 0):
                            all_chunks[key] = chunk
                
                # Combine and rerank all results
                combined = list(all_chunks.values()) + chunks
                reranked = _rerank_chunks(query, combined)
        
        return reranked
    except Exception as e:
        print(f"Error retrieving chunks: {str(e)}")
        import traceback
        traceback.print_exc()
        return []


async def generate_rag_answer(query: str, retrieved_chunks: List[dict]) -> Tuple[str, List[str]]:
    """
    Generate answer using RAG pipeline.
    Returns: (answer, source_pages)
    """
    try:
        if not retrieved_chunks:
            return "I don't have that information in the provided document.", []

        # Build context from retrieved chunks
        context_parts = []
        seen_pages = set()

        for i, chunk in enumerate(retrieved_chunks, 1):
            page = chunk.get("page", "Unknown")
            context_parts.append(f"--- Chunk {i} (Page: {page}) ---\n{chunk['content']}")
            if page and page != "Unknown":
                seen_pages.add(f"page {page}")

        context_text = "\n\n".join(context_parts)

        query_type_hint = "timing/schedule" if _is_timing_query(query) else "general"

        # RAG Prompt
        prompt_template = PromptTemplate(
            input_variables=["context", "question", "query_type_hint"],
            template="""You are a hospital assistant AI. Answer questions ONLY using the provided document context.

RULES:
1. Use ONLY information from the context below
2. Never use general knowledge
3. If the answer is not in the context, say exactly: "I don't have that information in the provided document."
4. Be concise and accurate with numbers, names, and timings
5. If query_type_hint is timing/schedule and timings exist in context, quote exact time ranges and relevant days.

Query Type Hint: {query_type_hint}

Context:
{context}

Question: {question}

Answer:"""
        )

        llm = get_llm_client()
        prompt = prompt_template.format(
            context=context_text,
            question=query,
            query_type_hint=query_type_hint
        )
        response = llm.invoke(prompt)
        answer = response.content.strip()

        sources = sorted(seen_pages) if seen_pages else ["Unknown"]
        return answer, sources

    except Exception as e:
        print(f"Error generating answer: {str(e)}")
        return f"Error processing query: {str(e)}", []


async def answer_query(query: str) -> Dict:
    """Complete RAG pipeline: retrieve → generate → return."""
    try:
        chunks = await retrieve_relevant_chunks(query)

        if not chunks:
            return {
                "status": "success",
                "answer": "I don't have that information in the provided document.",
                "sources": [],
                "chunks_found": 0,
                "chunks": []
            }

        answer, sources = await generate_rag_answer(query, chunks)

        return {
            "status": "success",
            "answer": answer,
            "sources": sources,
            "chunks_found": len(chunks),
            "chunks": [
                {
                    "content": chunk["content"][:200] + "..." if len(chunk["content"]) > 200 else chunk["content"],
                    "page": chunk.get("page", "Unknown"),
                    "similarity": chunk.get("similarity", 0)
                }
                for chunk in chunks
            ]
        }

    except Exception as e:
        return {
            "status": "error",
            "answer": f"Error processing query: {str(e)}",
            "sources": [],
            "chunks_found": 0,
            "chunks": []
        }