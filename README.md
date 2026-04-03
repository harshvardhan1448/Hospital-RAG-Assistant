# 🏥 Hospital RAG Assistant

An AI-powered Retrieval-Augmented Generation (RAG) system that answers questions about hospital documents using embeddings, vector search, and large language models.

## 📋 Project Overview

This system implements a complete RAG pipeline that:
- ✅ Ingests PDF hospital documents
- ✅ Extracts and chunks text intelligently
- ✅ Generates embeddings for semantic search
- ✅ Stores vectors in Supabase (pgvector)
- ✅ Retrieves relevant context using similarity search
- ✅ Generates accurate answers using LLMs (Groq/OpenAI)
- ✅ Prevents hallucination by only using document context
- ✅ Provides a user-friendly Streamlit UI

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (Streamlit)              │
├─────────────────────────────────────────────────────────────┤
│                    FastAPI Backend (main.py)               │
├──────────────────────┬──────────────────────┬───────────────┤
│   Document Ingestion │   RAG Pipeline       │  DB Manager   │
│   (ingestion.py)     │   (rag_pipeline.py)  │  (supabase_db)│
├─────────────────────────────────────────────────────────────┤
│  OpenAI Embeddings   │    Groq/OpenAI LLM   │ Supabase      │
│  (Text Embeddings)   │  (Answer Generation) │ (pgvector)    │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
1. Document Upload
   PDF → Extract Text → Chunk → Generate Embeddings → Store in DB

2. Query Processing
   Question → Generate Embedding → Vector Search → Retrieve Top-K → LLM → Answer
```

## 📁 Project Structure

```
NexovAi/
├── main.py                 # FastAPI backend (upload/query endpoints)
├── ingestion.py            # PDF processing & chunking
├── rag_pipeline.py         # RAG logic & LLM integration
├── supabase_db.py          # Supabase vector database manager
├── app_ui.py               # Streamlit frontend
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── .env.example             # Environment variables template
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- A Supabase account (free tier available)
- OpenAI API key (for embeddings)
- Groq API key (free, for LLM) OR OpenAI API key

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Supabase

1. **Create Supabase Project**
   - Go to [supabase.com](https://supabase.com)
   - Create a new project
   - Copy your `SUPABASE_URL` and `SUPABASE_KEY` (anon key)

2. **Create Table with pgvector**
   - In Supabase dashboard, go to SQL Editor
   - Run the following SQL:

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create documents table
CREATE TABLE IF NOT EXISTS documents (
  id BIGSERIAL PRIMARY KEY,
  filename TEXT NOT NULL,
  chunk_index INTEGER,
  content TEXT,
  embedding vector(1536),
  page TEXT,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create index for vector similarity search
CREATE INDEX documents_embedding_idx ON documents 
USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Create RPC function for similarity search
CREATE OR REPLACE FUNCTION match_documents(
  query_embedding vector,
  match_count int DEFAULT 5
) RETURNS TABLE (
  id bigint,
  content text,
  similarity float8,
  page text,
  metadata jsonb
) LANGUAGE plpgsql AS $$
BEGIN
  RETURN QUERY
  SELECT
    documents.id,
    documents.content,
    1 - (documents.embedding <=> query_embedding) as similarity,
    documents.page,
    documents.metadata
  FROM documents
  ORDER BY documents.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
```

### 3. Configure Environment

Copy `.env.example` to `.env` and fill in:

```bash
cp .env.example .env
```

Edit `.env`:
```
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-anon-key
GROQ_API_KEY=your-groq-api-key
OPENAI_API_KEY=your-openai-api-key
```

Get API Keys:
- **Groq**: [console.groq.com](https://console.groq.com) (Free)
- **OpenAI**: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### 4. Run the Application

**Terminal 1 - Start FastAPI Backend:**
```bash
python main.py
```
API will be available at `http://localhost:8000`

**Terminal 2 - Start Streamlit Frontend:**
```bash
streamlit run app_ui.py
```
UI will be available at `http://localhost:8501`

## 📘 API Usage

### Upload Document

```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@hospital_document.pdf"
```

**Response:**
```json
{
  "status": "success",
  "filename": "hospital_document.pdf",
  "pages": 10,
  "chunks": 45,
  "message": "Document uploaded successfully with 45 chunks"
}
```

### Ask Question

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the OPD timings?"}'
```

**Response:**
```json
{
  "status": "success",
  "answer": "The OPD (Out Patient Department) timings are 9:00 AM to 5:00 PM, Monday to Friday.",
  "sources": ["PAGE 3", "PAGE 5"],
  "chunks_found": 4,
  "chunks": [
    {
      "content": "OPD Timings: 9:00 AM - 5:00 PM (Mon-Fri)...",
      "page": "PAGE 3"
    }
  ]
}
```

### Get All Documents

```bash
curl "http://localhost:8000/documents"
```

### Delete Document

```bash
curl -X DELETE "http://localhost:8000/documents/hospital_document.pdf"
```

## 🧪 Testing with Example Queries

The system should answer these hospital document queries:

```
✓ "What are OPD timings?"
✓ "Who is the cardiologist?"
✓ "What is the cost of MRI?"
✓ "Can I cancel appointment within 24 hours?"
✓ "What is ICU cost per day?"
✓ "Emergency number?"
```

### Example Results

**Query:** "What is the ICU cost per day?"
```
Answer: The ICU cost is $600 per day.
Sources: [PAGE 5]
```

**Query:** "Emergency number?"
```
Answer: The emergency number is 1066.
Sources: [PAGE 2]
```

## ⚙️ Configuration Options

Edit `config.py` to customize:

```python
# Document Processing
CHUNK_SIZE = 500          # Characters per chunk
CHUNK_OVERLAP = 100       # Overlap between chunks

# Retrieval
TOP_K_CHUNKS = 4          # Top-k chunks to retrieve

# Embeddings
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSION = 1536

# LLM
LLM_PROVIDER = "groq"     # Options: groq, openai

# API
API_PORT = 8000
API_HOST = "0.0.0.0"
```

## 🔐 Security Considerations

1. **API Keys**: Keep `.env` file secure, never commit to git
2. **Supabase RLS**: Configure Row Level Security policies in production
3. **Rate Limiting**: Add rate limiting middleware for production
4. **Input Validation**: All inputs are validated
5. **No Hallucination**: Model only answers from retrieved context

## 🎨 Features

### Core Features ✅
- PDF document upload
- Intelligent text chunking
- Vector embeddings with OpenAI
- Semantic similarity search
- RAG-based answer generation
- Source attribution

### UI Features ✅
- Clean Streamlit interface
- Chat history
- Document management
- Retrieved chunks preview
- Real-time processing feedback

### Bonus Features (Optional)
- [ ] Re-ranking with BM25
- [ ] Hybrid search (keyword + semantic)
- [ ] Multi-document awareness
- [ ] Chat memory/context
- [ ] Voice input

## 🐛 Troubleshooting

### API Connection Error
```
Error: Cannot connect to API at http://localhost:8000
```
Solution: Make sure FastAPI backend is running on correct port

### Supabase Connection Error
```
Error: Invalid Supabase credentials
```
Solution: Check SUPABASE_URL and SUPABASE_KEY in .env

### OpenAI API Error
```
Error: Invalid OpenAI API key
```
Solution: Verify OPENAI_API_KEY is correct and has available credits

### No Results for Query
```
"I don't have that information in the provided document."
```
This is correct behavior - the information is not in the document

## 📊 Performance Tips

1. **Chunk Size**: Smaller chunks = more precise, larger = better context
2. **Embedding Model**: text-embedding-3-small is fast and accurate
3. **Top-K**: Higher k = more context but slower, usually 4-5 is optimal
4. **Batch Upload**: Upload large documents in batches for better indexing

## 🤝 Contributing

To improve this system:
1. Add better chunking strategies
2. Implement hybrid search
3. Add BM25 reranking
4. Support for more document types
5. Multi-language support

## 📄 License

MIT License

## 📞 Support

For issues or questions, please check:
- Supabase Docs: https://supabase.com/docs
- LangChain Docs: https://python.langchain.com
- FastAPI Docs: https://fastapi.tiangolo.com

---

**Built with:** LangChain • Supabase • FastAPI • Streamlit • OpenAI/Groq
