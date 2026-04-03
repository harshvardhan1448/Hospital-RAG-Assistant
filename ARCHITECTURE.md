# 🏗️ System Architecture

## How Everything Works Together

Here's a simple explanation of how the system works:

### 🎯 The Big Picture

```
   You                You ask                System finds              System
  Upload              a question            answer in docs            replies
  Document    ——→       ——→         ——→                    ——→
```

---

## 🔄 Complete Data Flow

### When You Upload a Document:

```
Your PDF File
    ↓
📄 Extract Text from PDF
   (Using PyPDF2)
    ↓
✂️ Break into Small Chunks
   (500 characters each)
    ↓
🧠 Create Embeddings for Each Chunk
   (Local AI fingerprints - no API call!)
    ↓
💾 Store in Supabase Database
   (With embeddings attached)
    ↓
✅ Done! Ready for questions
```

### When You Ask a Question:

```
Your Question: "What are OPD timings?"
    ↓
🧠 Create Embedding of Your Question
   (Same AI model, local)
    ↓
🔍 Search Database for Similar Chunks
   (Find chunks with similar meaning)
    ↓
📋 Get Top 4 Most Similar Chunks
    ↓
📝 Send Chunks + Question to AI Model
   (Groq LLM)
    ↓
💬 AI Generates Answer Using Only Those Chunks
    ↓
📍 Show Answer + Source Pages to You
```

---

## 🏢 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    YOUR WEB BROWSER                             │
│      (Local: http://localhost:8501 or deployed Streamlit URL)   │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  Streamlit Interface (app_ui.py)                       │   │
│  │  • Upload documents                                    │   │
│  │  • Ask questions                                       │   │
│  │  • See chat history                                    │   │
│  └────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP Requests
                             ↓
┌────────────────────────────────────────────────────────────────┐
│          FASTAPI BACKEND (your_computer:8000)                  │
│                  (main.py)                                     │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  When you UPLOAD a document:                                  │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ 1. Receive PDF file                                 │    │
│  │ 2. Call ingestion.py                                │    │
│  │    • Extract text (PyPDF2)                          │    │
│  │    • Split into chunks (LangChain)                  │    │
│  │    • Create embeddings (local hashing embedder)     │    │
│  │ 3. Save to database                                 │    │
│  │ 4. Return success                                   │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                                │
│  When you ASK a question:                                     │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ 1. Receive question                                 │    │
│  │ 2. Call rag_pipeline.py                             │    │
│  │    • Create embedding of question                   │    │
│  │    • Search database for similar chunks             │    │
│  │    • Send chunks to Groq AI                         │    │
│  │    • Get answer back                                │    │
│  │ 3. Return answer to you                             │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                                │
└────────────────┬─────────────────────────┬────────────────────┘
                 │                         │
                 ↓                         ↓
        ┌──────────────────┐     ┌──────────────────────┐
        │   SUPABASE DB    │     │ GROQ AI MODEL        │
        │ (PostgreSQL)     │     │ (llama-3.1-8b)       │
        │                  │     │                      │
        │ • Your documents │     │ • Reads chunks       │
        │ • Embeddings     │     │ • Generates answer   │
        │ • Vector search  │     │ • Free, very fast    │
        └──────────────────┘     └──────────────────────┘
```

---

## 🎯 Key Components Explained

### 1. **File: `ingestion.py`** - Document Upload

What it does:
- Takes your PDF file
- Extracts all the text
- Breaks text into chunks (like dividing a book into pages)
- Creates an "embedding" for each chunk (AI fingerprint)
- Saves everything to Supabase

### 2. **File: `rag_pipeline.py`** - Question Answering

What it does:
- Takes your question
- Creates an embedding of your question
- Searches Supabase for similar chunks
- Sends the question + closest chunks to Groq AI
- Gets the answer back

### 3. **File: `supabase_db.py`** - Database Manager

What it does:
- Stores all your documents
- Stores all embeddings (AI fingerprints)
- Performs similarity searches
- Keeps everything organized

### 4. **File: `app_ui.py`** - Web Interface

What it does:
- Shows you the upload button
- Shows you the chat interface
- Displays results
- Manages document list

### 5. **File: `config.py`** - Settings

Key settings:
- How big each chunk should be (500 chars)
- How many chunks to search (4 chunks)
- Which embedding model to use
- Which AI model to use

---

## 💾 What Gets Stored Where

### On Your Computer (`config.py`, `.env`, source code):
- API keys (kept secret)
- Settings and preferences
- Python code

### On Supabase (Cloud Database):
- Your PDF documents (text content)
- Embeddings (AI fingerprints, 384 numbers each)
- Metadata (page numbers, file names)
- Nothing sensitive, nothing that identifies you

### In Memory (While Running):
- Current embeddings being processed
- Similarity search results
- Chat history

---

## 🔐 Why It's Secure

1. **Your PDF documents** are stored in YOUR Supabase database
   - You control who can access it
   - Supabase has strong security

2. **Embeddings never leave your database**
   - Created locally
   - Only numbers (not the actual text)
   - Can't identify the document content

3. **API keys are local-only**
   - Never in code (always in `.env`)
   - `.env` is in `.gitignore` (never uploaded)

4. **AI uses only what you uploaded**
   - Can't access other documents
   - Can't access the internet
   - Only answers from your documents

---

## ⚡ Performance Notes

- **First upload**: Takes longer (1-2 min for 10-page PDF)
  - Creates embeddings for all chunks
  
- **Subsequent uploads**: Faster (reuses model in memory)

- **Questions**: Usually 1-2 seconds
  - Embedding generation: 50ms
  - Database search: 100ms
  - AI answer generation: 500ms

- **Embedding model**: Local hashing embedder
     - 384 dimensions
     - No external download or model hosting
     - Fast and deterministic

---

## 🔗 Technology Choices (Why Free?)

| Part | Technology | Why? |
|------|-----------|------|
| Embeddings | Local hashing embedder | Runs locally, no API calls, free |
| LLM (AI) | Groq | Free tier, fast, 8B parameters |
| Database | Supabase | Free tier, PostgreSQL, pgvector |
| Server | FastAPI | Lightweight, fast, Python-native |
| UI | Streamlit | No frontend coding needed, fast |

---

## 🚀 Scaling Considerations

This system works well for:
- ✅ Individual users
- ✅ Small hospitals/clinics
- ✅ 10-100 PDF documents
- ✅ 10-100 questions per day

For larger deployments:
- Add caching layer
- Use GPU for embeddings
- Distribute database across regions
- Add authentication/permissions
- Monitor API usage
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
