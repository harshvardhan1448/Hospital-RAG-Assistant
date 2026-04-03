# 🏥 Hospital RAG Assistant

An intelligent AI-powered Retrieval-Augmented Generation (RAG) system that answers questions about hospital documents. **100% Free to run** - uses no paid APIs!

## 📋 What This Does

This system lets you upload hospital PDF documents and ask questions about them. The AI reads your documents and answers using **only the information found in them** - no hallucinations, no making things up.

Deployment status: the backend is live on Render, and the deployed UI should point to the Render API instead of localhost.

**Key Features:**
- 📄 Upload PDF hospital documents
- 🤖 Ask questions in natural language
- 🔍 AI searches documents for answers
- ✅ Always cites where the answer came from
- 💰 **Completely FREE** - uses free APIs only
- 🖥️ Works locally on your machine
- 🎨 Beautiful web interface

## 🏗️ How It Works

```
You Upload PDF
      ↓
System Breaks Into Chunks
      ↓
Creates Embeddings (AI Text Fingerprints)
      ↓
Stores in Database
      ↓

You Ask a Question
      ↓
System Creates Embedding of Your Question
      ↓
Finds Similar Chunks in Database
      ↓
Sends Chunks to AI Model
      ↓
AI Generates Answer (Only From Your Documents)
      ↓
You Get Answer With Source Pages
```

## 📁 What's Inside

```
Hospital-RAG-Assistant/
├── main.py                 # API Server (handles uploads & questions)
├── app_ui.py               # Web Interface (Streamlit)
├── ingestion.py            # Document Processing
├── rag_pipeline.py         # AI Logic & Answering
├── supabase_db.py          # Database Manager
├── embeddings.py           # Embedding Generator
├── config.py               # Settings
├── requirements.txt        # Python Libraries
├── supabase_setup.sql      # Database Setup
├── .env.example            # Configuration Template
└── README.md               # This file
```

## 🎯 Tech Stack (All Free!)

| Component | Technology | Why? |
|-----------|-----------|------|
| **Embeddings** | Local hashing embedder | No download, no API calls |
| **AI Model** | Groq (Llama 3.1) | Free, very fast, up to 4000+ tokens/min |
| **Database** | Supabase (PostgreSQL) | Free tier, unlimited usage |
| **Vector Search** | pgvector | Built-in, fast similarity search |
| **Web Server** | FastAPI | Fast, production-ready, lightweight |
| **Web UI** | Streamlit | Beautiful, requires no frontend skills |

> **💰 Cost: low to $0/month** - Supabase and Groq can stay on free tiers; hosting depends on your deployment plan.

## 🚀 Get Started in 5 Minutes

### Step 1: Prerequisites

You need:
- Python 3.9 or newer
- A computer that can run Python
- Internet connection (for API setup only)

### Step 2: Download & Setup

```bash
# Clone the project
git clone https://github.com/harshvardhan1448/Hospital-RAG-Assistant.git
cd Hospital-RAG-Assistant

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Get Free API Keys (5 minutes)

#### A. Supabase (Database) - 100% Free

1. Go to **[supabase.com](https://supabase.com)** → Click "Sign Up"
2. Sign up with GitHub, Google, or Email
3. Create new project
4. Once created, go to **Settings** → **API**
5. Copy these two values:
   - **Project URL** → This is `SUPABASE_URL`
   - **Anon public** key → This is `SUPABASE_KEY`

#### B. Groq (AI Model) - 100% Free

1. Go to **[console.groq.com](https://console.groq.com)**
2. Sign up (takes 1 minute)
3. Click **API Keys** → **Create New API Key**
4. Copy it → This is `GROQ_API_KEY`

That's it! No payment needed, free tier is unlimited.

### Step 4: Configure Environment

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your keys
```

Your `.env` should look like:
```
SUPABASE_URL=https://abc123.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIs...
GROQ_API_KEY=gsk_abc123...
API_BASE_URL=https://hospital-rag-assistant-z1df.onrender.com
```

### Step 5: Setup Database (One-Time)

1. Go to your **Supabase Dashboard**
2. Click **SQL Editor** → **New Query**
3. Copy entire content from **`supabase_setup.sql`**
4. Paste into the query box
5. Click **Run**

Done! Your database is ready.

### Step 6: Run the Application

Open **two terminal windows**:

**Terminal 1 - Start the API Server:**
```bash
python main.py
```

You should see:
```
✓ Application initialized successfully
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 - Start the Web Interface:**
```bash
streamlit run app_ui.py
```

You should see:
```
You can now view your Streamlit app in your browser
Local URL: http://localhost:8501
```

### Step 7: Use It!

Open your browser to the deployed Streamlit app, or if running locally, use **http://localhost:8501**

1. Upload a hospital PDF document
2. Ask a question (e.g., "What are the OPD timings?")
3. Get instant answer with source pages!

## 📖 API Usage (For Developers)

### Upload a Document

```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@hospital.pdf"
```

Response:
```json
{
  "status": "success",
  "filename": "hospital.pdf",
  "pages": 5,
  "chunks": 25,
  "message": "Document uploaded successfully with 25 chunks"
}
```

### Ask a Question

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the emergency number?"}'
```

Response:
```json
{
  "status": "success",
  "answer": "The emergency number is 1066.",
  "sources": ["page 1"],
  "chunks_found": 2,
  "chunks": [...]
}
```

### Get Documents

```bash
curl "http://localhost:8000/documents"
```

### Delete Document

```bash
curl -X DELETE "http://localhost:8000/documents/hospital.pdf"
```

## 🧪 Test It Out

Try these questions with a hospital document:

- "What are the OPD timings?"
- "Who is the cardiologist?"
- "What is the MRI cost?"
- "Can I cancel a 24-hour appointment?"
- "What is the ICU cost per day?"

## ⚙️ Configuration

Edit `config.py` to customize behavior:

```python
# How much text in each chunk
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# How many results to show
TOP_K_CHUNKS = 4

# Embedding model is handled locally by the hashing embedder
EMBEDDING_MODEL = "local-hashing"
EMBEDDING_DIMENSION = 384

# Database table name
SUPABASE_TABLE = "documents"
```

## 🔒 Security & Privacy

✅ **Your documents stay private:**
- Documents are stored only in YOUR Supabase database
- You control access with your API keys
- No third-party sees your documents
- Embeddings never sent to OpenAI

✅ **API Keys are safe:**
- `.env` file is in `.gitignore` (never uploaded)
- Never hardcode secrets in code
- Use environment variables

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
