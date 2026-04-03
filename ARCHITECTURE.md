# Hospital RAG Assistant - Architecture & System Design

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          USER INTERACTION LAYER                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │               Streamlit Web UI (app_ui.py)                      │  │
│  │  ┌──────────────────┐              ┌──────────────────────────┐ │  │
│  │  │ Document Upload  │              │    Question Input       │ │  │
│  │  │    Interface     │              │    Chat History View    │ │  │
│  │  │ File Management  │              │   Retrieved Chunks      │ │  │
│  │  └──────────────────┘              └──────────────────────────┘ │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                  ↓                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                       API COMMUNICATION (HTTP)                          │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼─────────────────────────────────────┐
│                       FASTAPI BACKEND (main.py)                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  Endpoint: POST /upload                                         │  │
│  │  - Receives PDF file                                            │  │
│  │  - Delegates to ingestion service                               │  │
│  │  - Returns status and metadata                                  │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                  ↓                                      │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  Endpoint: POST /query                                          │  │
│  │  - Receives user question                                       │  │
│  │  - Delegates to RAG pipeline                                    │  │
│  │  - Returns answer with sources                                  │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                    DOCUMENT PROCESSING PIPELINE                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │          Ingestion Service (ingestion.py)                        │  │
│  │  ┌────────────────┐  ┌────────────┐  ┌──────────────────────┐  │  │
│  │  │  PDF Extractor │→ │   Chunker  │→ │ Embedding Generator  │  │  │
│  │  │ PyPDF2 Parser  │  │ LangChain  │  │  OpenAI API          │  │  │
│  │  └────────────────┘  └────────────┘  └──────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                  │                                      │
│                                  ▼                                      │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │     Database Manager (supabase_db.py)                            │  │
│  │  - Store documents with embeddings                              │  │
│  │  - Perform similarity search                                    │  │
│  │  - Manage document lifecycle                                    │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                         RAG PIPELINE (rag_pipeline.py)                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Query Processing Flow:                                          │   │
│  │                                                                 │   │
│  │  1. Query Embedding                                            │   │
│  │     Query Text ──→ OpenAI API ──→ Vector Embedding             │   │
│  │                                                                 │   │
│  │  2. Retrieval                                                  │   │
│  │     Query Vector ──→ Similarity Search ──→ Top-K Chunks        │   │
│  │                                                                 │   │
│  │  3. Generation                                                 │   │
│  │     (Query + Context) ──→ LLM (Groq/OpenAI) ──→ Answer         │   │
│  │                                                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼─────────────────────────────────────┐
│                  EXTERNAL SERVICES & DATABASES                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────────────  ┌──────────────────────────────────────┐ │
│  │  OpenAI Embeddings API     │  Supabase PostgreSQL + pgvector     │ │
│  │  - text-embedding-3-small  │  - Vector storage (embeddings)      │ │
│  │  - 1536 dimensions         │  - Cosine similarity search         │ │
│  │  - Semantic understanding  │  - Document chunks storage          │ │
│  └──────────────────────────  │  - Metadata indexing                │ │
│                               └──────────────────────────────────────┘ │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  LLM (Groq or OpenAI)                                            │  │
│  │  - Answer generation from context                               │  │
│  │  - Groq: Free, Fast (Mixtral-8x7b)                              │  │
│  │  - OpenAI: GPT-3.5-turbo or GPT-4                               │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

### Document Upload Flow

```
User Action: Upload Hospital PDF
         │
         ▼
    ┌─────────────────────┐
    │  Extract Text       │ (PyPDF2)
    │  from PDF           │
    └──────────┬──────────┘
         │
         ▼
    ┌─────────────────────┐
    │  Split into         │ (LangChain RecursiveCharacterTextSplitter)
    │  Chunks             │ - Chunk size: 500 chars
    │                     │ - Overlap: 100 chars
    └──────────┬──────────┘
         │
         ▼
    ┌─────────────────────┐
    │  Generate           │ (OpenAI API)
    │  Embeddings         │ - Model: text-embedding-3-small
    │  for each chunk     │ - Dimension: 1536
    └──────────┬──────────┘
         │
         ▼
    ┌─────────────────────┐
    │  Store in DB        │ (Supabase)
    │  - Content          │ - With pgvector extension
    │  - Embedding        │ - Create IVFFLAT index
    │  - Metadata         │
    └──────────┬──────────┘
         │
         ▼
User: Success! Document Ready for Queries
```

### Query Processing Flow

```
User Action: Ask Question
         │
         ▼
    ┌─────────────────────┐
    │  Embed Query        │ (OpenAI API)
    │  to Vector          │ - Same model as documents
    │                     │ - 1536 dimensions
    └──────────┬──────────┘
         │
         ▼
    ┌─────────────────────┐
    │  Vector Similarity  │ (Supabase)
    │  Search             │ - Cosine distance <=>
    │  Retrieve Top-K     │ - K = 4 (configurable)
    └──────────┬──────────┘
         │
         ▼
    ┌─────────────────────┐
    │  Format Context     │ (Python)
    │  Prepare Prompt     │ - Combine top chunks
    │                     │ - Add query
    └──────────┬──────────┘
         │
         ▼
    ┌─────────────────────┐
    │  Call LLM           │ (Groq or OpenAI)
    │  Generate Answer    │ - Process prompt
    │  from Context       │ - Generate response
    └──────────┬──────────┘
         │
         ▼
    ┌─────────────────────┐
    │  Format Response    │ (Python)
    │  - Answer           │ - Extract sources
    │  - Sources          │ - Include metadata
    │  - Metadata         │
    └──────────┬──────────┘
         │
         ▼
User: Receives Answer with Sources
```

## Component Interaction

### 1. Upload Endpoint (`/upload`)

```
Request: POST /upload
├── File: hospital_document.pdf
└── MultipartForm data

Processing:
├── FastAPI validates file type
├── ingestion.ingest_document()
│   ├── extract_text_from_pdf() → text extraction
│   ├── chunk_text() → split into chunks
│   ├── generate_embeddings() → OpenAI API call
│   └── prepare_documents_for_storage() → format data
├── supabase_manager.store_documents()
│   └── Insert documents table with embeddings

Response: 
{
  "status": "success",
  "filename": "hospital_document.pdf",
  "pages": 10,
  "chunks": 45
}
```

### 2. Query Endpoint (`/query`)

```
Request: POST /query
└── JSON: {"question": "What are OPD timings?"}

Processing:
├── rag_pipeline.answer_query()
│   ├── retrieve_relevant_chunks()
│   │   ├── get_query_embedding() → OpenAI API
│   │   └── supabase_similarity_search() → pgvector search
│   └── generate_rag_answer()
│       ├── Format context from chunks
│       ├── Create RAG prompt
│       ├── Call LLM (Groq/OpenAI)
│       └── Extract sources

Response:
{
  "status": "success",
  "answer": "The OPD timings are 9:00 AM to 5:00 PM, Monday to Friday.",
  "sources": ["PAGE 3"],
  "chunks_found": 4
}
```

## Key Design Decisions

### 1. Chunking Strategy
- **RecursiveCharacterTextSplitter**: Preserves semantic structure
- **Chunk Size**: 500 characters (good balance for RAG)
- **Overlap**: 100 characters (context continuity)

### 2. Embedding Model
- **OpenAI text-embedding-3-small**: Fast, lightweight, 1536 dims
- **Alternative**: Use text-embedding-3-large (3072 dims) for higher quality

### 3. Similarity Search
- **Cosine Distance** (<=> operator): Standard for semantic similarity
- **Top-K=4**: Good trade-off between precision and context
- **IVFFLAT Index**: Fast approximate nearest neighbor search

### 4. LLM Selection
- **Groq (Default)**: Fast, free, good for HAP (Mixtral-8x7b)
- **OpenAI (Optional)**: More capabilities (GPT-4), payment required
- **Constraint**: Only answers from retrieved context

### 5. Database Choice
- **Supabase PostgreSQL**: pgvector for vector storage
- **Advantages**: Managed, easy setup, good for RAG, RLS support
- **Performance**: Suitable for 10k-1M documents

## Security Model

### Row Level Security (RLS)
```
- Development: Permissive (allows all)
- Production: Implement strict policies
  * Users can only read/delete their own documents
  * Admin can manage all documents
```

### API Security
- CORS enabled (configure for production)
- Input validation on all endpoints
- No secrets in logs
- Environment variables for sensitive data

## Performance Optimization

### Indexing Strategy
```
- IVFFLAT index on embeddings (fast similarity search)
- B-tree index on filename (document filtering)
- GIN index on content (optional full-text search)
```

### Query Optimization
```
- Vector dimension: 1536 (optimal for 3-small model)
- Top-K default: 4 (faster than k=10, good context)
- Batch processing: Insert 100 chunks at a time
```

### Caching (Future Enhancement)
```
- Cache popular queries
- Cache document embeddings in memory
- Redis for distributed caching
```

## Scalability Considerations

### Current Limitations
- Single Supabase project
- No distributed caching
- No query queuing

### Scaling Path
1. **Phase 1** (1-10k docs): Current architecture sufficient
2. **Phase 2** (10k-100k docs): Add Redis caching, batch processing
3. **Phase 3** (100k+ docs): Distributed Supabase, endpoint management

## Error Handling & Resilience

### Graceful Degradation
- If embedding fails → return error to user
- If LLM call fails → retry with exponential backoff
- If DB connection fails → queue and retry

### User Feedback
- Clear error messages
- Don't expose internal stack traces
- Log errors for debugging

## Monitoring & Observability

### Key Metrics to Track
- Document upload success rate
- Query latency (p50, p99)
- LLM token usage
- Vector search performance
- Error rates by endpoint

---

**Last Updated**: 2024
**Version**: 1.0
