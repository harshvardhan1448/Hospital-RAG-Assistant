from typing import List, Dict, Tuple
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from embeddings import embed_query
from supabase_db import get_supabase_manager
import config


def get_query_embedding(query: str) -> list:
    return embed_query(query)


def get_llm_client() -> ChatGroq:
    return ChatGroq(
        model="llama-3.1-8b-instant",   # <-- updated model
        api_key=config.GROQ_API_KEY,
        temperature=0.3
    )

async def retrieve_relevant_chunks(query: str, k: int = config.TOP_K_CHUNKS) -> List[dict]:
    """Retrieve top-k most relevant document chunks for the query."""
    try:
        query_embedding = get_query_embedding(query)
        supabase = get_supabase_manager()
        chunks = await supabase.similarity_search(query_embedding, k=k)
        return chunks
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

        # RAG Prompt
        prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are a hospital assistant AI. Answer questions ONLY using the provided document context.

RULES:
1. Use ONLY information from the context below
2. Never use general knowledge
3. If the answer is not in the context, say exactly: "I don't have that information in the provided document."
4. Be concise and accurate with numbers, names, and timings

Context:
{context}

Question: {question}

Answer:"""
        )

        llm = get_llm_client()
        prompt = prompt_template.format(context=context_text, question=query)
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