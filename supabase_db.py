from supabase import create_client
from typing import List, Optional
import config


class SupabaseManager:
    def __init__(self):
        self.supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

    async def create_table_if_not_exists(self) -> dict:
        """Verify connection — actual table creation is done via supabase_setup.sql."""
        try:
            self.supabase.table(config.SUPABASE_TABLE).select("id").limit(1).execute()
            return {"status": "success", "message": "Supabase connection verified"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def store_documents(self, documents: List[dict]) -> dict:
        """Store document chunks and embeddings in Supabase in batches."""
        try:
            docs_to_insert = [
                {
                    "filename": doc["filename"],
                    "chunk_index": doc["chunk_index"],
                    "content": doc["content"],
                    "embedding": list(doc["embedding"]),
                    "page": doc.get("page", "Unknown"),
                    "metadata": doc.get("metadata", {})
                }
                for doc in documents
            ]

            batch_size = 50
            total_inserted = 0

            for i in range(0, len(docs_to_insert), batch_size):
                batch = docs_to_insert[i:i + batch_size]
                self.supabase.table(config.SUPABASE_TABLE).insert(batch).execute()
                total_inserted += len(batch)

            return {
                "status": "success",
                "documents_stored": total_inserted,
                "message": f"Successfully stored {total_inserted} document chunks"
            }
        except Exception as e:
            return {"status": "error", "message": f"Error storing documents: {str(e)}"}

    async def similarity_search(self, query_embedding: List[float], k: int = config.TOP_K_CHUNKS) -> List[dict]:
        """
        Perform cosine similarity search using pgvector in Supabase.
        """
        try:
            print(f"[DEBUG] Query embedding length: {len(query_embedding)}")
            print(f"[DEBUG] Sample values: first={query_embedding[0]}, last={query_embedding[-1]}")
            
            # Convert embedding to PostgreSQL vector format: "[val1,val2,...,val384]"
            vector_str = "[" + ",".join(str(float(x)) for x in query_embedding) + "]"
            print(f"[DEBUG] Vector string length: {len(vector_str)}")
            print(f"[DEBUG] Vector string first 100 chars: {vector_str[:100]}")
            
            # Call RPC function with vector string
            print(f"[DEBUG] Calling RPC with match_count={k}")
            response = self.supabase.rpc(
                "match_documents",
                {
                    "query_embedding": vector_str,
                    "match_count": k
                }
            ).execute()

            print(f"[DEBUG] RPC response type: {type(response)}")
            print(f"[DEBUG] RPC response: {response}")
            print(f"[DEBUG] RPC response.data type: {type(response.data) if hasattr(response, 'data') else 'N/A'}")
            print(f"[DEBUG] RPC returned {len(response.data) if response.data else 0} results")

            if not response.data:
                print("[DEBUG] No results from RPC similarity search")
                return []

            return [
                {
                    "content": r["content"],
                    "page": r.get("page", "Unknown"),
                    "metadata": r.get("metadata", {}),
                    "similarity": r.get("similarity", 0)
                }
                for r in response.data
            ]

        except Exception as e:
            print(f"[ERROR] similarity_search failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return []

    async def get_all_documents(self, filename: Optional[str] = None) -> List[dict]:
        """Retrieve document list without embedding column (too large)."""
        try:
            query = self.supabase.table(config.SUPABASE_TABLE).select(
                "id, filename, chunk_index, page, content, created_at"
            )
            if filename:
                query = query.eq("filename", filename)
            response = query.execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error retrieving documents: {str(e)}")
            return []

    async def delete_documents_by_filename(self, filename: str) -> dict:
        """Delete all chunks for a given filename."""
        try:
            self.supabase.table(config.SUPABASE_TABLE).delete().eq("filename", filename).execute()
            return {"status": "success", "message": f"Deleted documents for {filename}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}


# Singleton
supabase_manager = None

def get_supabase_manager() -> SupabaseManager:
    global supabase_manager
    if supabase_manager is None:
        supabase_manager = SupabaseManager()
    return supabase_manager