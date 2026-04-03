from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import config
from ingestion import ingest_document
from rag_pipeline import answer_query
from supabase_db import get_supabase_manager


# ==================== Lifespan (replaces deprecated on_event) ====================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize on startup, cleanup on shutdown."""
    try:
        supabase = get_supabase_manager()
        await supabase.create_table_if_not_exists()
        print("✓ Application initialized successfully")
    except Exception as e:
        print(f"Warning: Could not verify Supabase connection: {str(e)}")
        print("Please ensure your .env file has correct SUPABASE_URL and SUPABASE_KEY")
    yield  # App runs here


# ==================== App ====================

app = FastAPI(
    title="Hospital RAG Assistant API",
    description="RAG-based AI assistant for hospital documents",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== Models ====================

class QueryRequest(BaseModel):
    question: str

class UploadResponse(BaseModel):
    status: str
    filename: str
    pages: int
    chunks: int
    message: Optional[str] = None

class QueryResponse(BaseModel):
    status: str
    answer: str
    sources: List[str]
    chunks_found: int
    chunks: Optional[List[dict]] = None

class HealthResponse(BaseModel):
    status: str
    message: str


# ==================== Endpoints ====================

@app.get("/", response_model=HealthResponse)
async def health_check():
    return {"status": "healthy", "message": "Hospital RAG Assistant API is running"}


@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        print(f"[UPLOAD] Starting upload for: {file.filename}")
        result = await ingest_document(file)
        print(f"[UPLOAD] Ingestion result: {result}")

        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result.get("message", "Error ingesting document"))

        print(f"[UPLOAD] Storing {len(result['documents'])} documents in Supabase")
        supabase = get_supabase_manager()
        db_result = await supabase.store_documents(result["documents"])

        if db_result["status"] == "error":
            raise HTTPException(status_code=500, detail=db_result.get("message", "Error storing documents"))

        print(f"[UPLOAD] Success: {file.filename}")
        return {
            "status": "success",
            "filename": result["filename"],
            "pages": result["pages"],
            "chunks": result["chunks"],
            "message": f"Document '{result['filename']}' uploaded successfully with {result['chunks']} chunks"
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"[UPLOAD ERROR] Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error uploading document: {str(e)}")


@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        print(f"[API] Query received: {request.question}")
        result = await answer_query(request.question)
        print(f"[API] Query processed. Chunks found: {result.get('chunks_found', 0)}")
        return result
    except Exception as e:
        print(f"[API] Error processing query: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/documents", response_model=List[dict])
async def get_documents(filename: Optional[str] = None):
    try:
        supabase = get_supabase_manager()
        return await supabase.get_all_documents(filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving documents: {str(e)}")


@app.delete("/documents/{filename}")
async def delete_document(filename: str):
    try:
        supabase = get_supabase_manager()
        result = await supabase.delete_documents_by_filename(filename)

        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result.get("message"))

        return {"status": "success", "message": f"Deleted all chunks for {filename}"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("main:app", host=config.API_HOST, port=config.API_PORT, reload=True)



@app.get("/debug")
async def debug():
    supabase = get_supabase_manager()
    result = supabase.supabase.table("documents").select("id, filename, page, chunk_index").limit(5).execute()
    count = supabase.supabase.table("documents").select("id", count="exact").execute()
    return {
        "total_rows": count.count,
        "sample": result.data,
        "supabase_url": config.SUPABASE_URL[:40] + "..."  # partial for security
    }
