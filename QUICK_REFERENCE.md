# Hospital RAG Assistant - Quick Reference Guide

## 🚀 Getting Started (5 Minutes)

### Installation
```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate.bat

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup configuration
cp .env.example .env
# Edit .env with your API keys

# 4. Setup database (one-time)
# Go to https://supabase.com/dashboard
# Run SQL from supabase_setup.sql in SQL Editor

# 5. Start API backend
python main.py

# 6. In another terminal, start UI
streamlit run app_ui.py
```

**Access:**
- API Docs: http://localhost:8000/docs
- Streamlit UI: http://localhost:8501

---

## 📋 API Quick Reference

### Upload Document
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@hospital.pdf"
```

### Ask Question
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What are OPD timings?"}'
```

### Get Documents List
```bash
curl "http://localhost:8000/documents"
```

### Delete Document
```bash
curl -X DELETE "http://localhost:8000/documents/hospital.pdf"
```

---

## ⚙️ Configuration Tweaks

### For Better Quality Answers
```python
# config.py
TOP_K_CHUNKS = 5      # More context (default: 4)
CHUNK_SIZE = 1000     # Larger chunks (default: 500)
CHUNK_OVERLAP = 200   # More context (default: 100)
```

### For Faster Responses
```python
# config.py
TOP_K_CHUNKS = 3      # Less context
CHUNK_SIZE = 300      # Smaller chunks
```

### Switch LLM Provider
```bash
# .env
# For Groq (free, recommended):
LLM_PROVIDER=groq
GROQ_API_KEY=your-key

# For OpenAI:
LLM_PROVIDER=openai
OPENAI_API_KEY=your-key
```

---

## 🧪 Testing

### Test Full Pipeline
```bash
# Terminal 1: Start API
python main.py

# Terminal 2: Run tests
python test_api.py path/to/document.pdf
```

### Test Individual Components
```bash
# Test Supabase connection
python -c "from supabase_db import get_supabase_manager; print('OK')"

# Test embeddings
python -c "from ingestion import get_embeddings_client; e = get_embeddings_client(); print(e.embed_query('test')[:3])"

# Test LLM
python -c "from rag_pipeline import get_llm_client; llm = get_llm_client(); print(llm.invoke('Hello'))"
```

---

## 🐛 Common Fixes

### API won't start
```bash
# Check if port is in use
netstat -tuln | grep 8000

# Kill process on port
taskkill /PID <pid> /F  # Windows
kill -9 <pid>           # Linux/Mac

# Try different port
# Edit config.py: API_PORT = 8001
```

### No API keys working
```bash
# Reload environment
deactivate
source venv/bin/activate  # Or venv\Scripts\activate.bat

# Verify keys are set
echo $OPENAI_API_KEY
echo $GROQ_API_KEY
```

### Database connection fails
```bash
# Verify credentials
# .env should have:
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=your-anon-key

# Test connection
python -c "import supabase_db; print('OK')"
```

### Slow queries
```python
# In config.py, reduce search scope
TOP_K_CHUNKS = 3  # Fewer chunks
CHUNK_SIZE = 400  # Smaller chunks
```

---

## 📊 Example Queries

These should work if document is uploaded:

```
"What are OPD timings?"
"Who is the cardiologist?"
"What is the cost of MRI?"
"Can I cancel appointment within 24 hours?"
"What is ICU cost per day?"
"Emergency number?"
```

---

## 🔑 API Keys Setup

### Get Groq API Key (Recommended - FREE)
1. Go to https://console.groq.com
2. Sign up
3. Create API key
4. Copy to .env: `GROQ_API_KEY=...`

### Get OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Sign up / Login
3. Create new API key
4. Add payment method (required)
5. Copy to .env: `OPENAI_API_KEY=...`

### Get Supabase Credentials
1. Go to https://supabase.com
2. Create new project
3. Go to Settings → API
4. Copy "Project URL" → `SUPABASE_URL`
5. Copy "Anon public key" → `SUPABASE_KEY`

---

## 📁 Project Structure

```
NexovAi/
├── main.py              # FastAPI backend
├── ingestion.py         # PDF processing
├── rag_pipeline.py      # RAG logic
├── supabase_db.py       # Database manager
├── config.py            # Configuration
├── app_ui.py            # Streamlit UI
├── test_api.py          # API tests
├── requirements.txt     # Dependencies
├── .env.example         # Environment template
├── supabase_setup.sql   # Database setup
├── ARCHITECTURE.md      # System design
├── DEPLOYMENT.md        # Deployment guide
└── README.md            # Full documentation
```

---

## 🚢 Docker Deployment

### Build & Run
```bash
# Build image
docker build -t hospital-rag .

# Run container
docker run -p 8000:8000 \
  -e SUPABASE_URL="..." \
  -e SUPABASE_KEY="..." \
  -e OPENAI_API_KEY="..." \
  hospital-rag
```

### Using Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop
docker-compose down
```

---

## 🌐 Deployment Options

| Platform | Cost | Difficulty | Speed |
|----------|------|------------|-------|
| **Render** | Free-$7/mo | ⭐ Easy | ⚡ Fast |
| **Heroku** | Paid | ⭐ Easy | ⚡ Fast |
| **AWS EC2** | Free-$15/mo | ⭐⭐ Medium | ⚡ Variable |
| **Docker** | Varies | ⭐⭐ Medium | ⚡⚡ Good |

See `DEPLOYMENT.md` for full guides.

---

## 📈 Performance Tuning

### Faster Responses
```python
TOP_K_CHUNKS = 3          # Fewer chunks
CHUNK_SIZE = 200          # Smaller chunks
LLM_PROVIDER = "groq"     # Groq is faster
```

### Better Quality
```python
TOP_K_CHUNKS = 5          # More context
CHUNK_SIZE = 1000         # Larger chunks
LLM_PROVIDER = "openai"   # GPT-4 for quality
```

### Balanced
```python
TOP_K_CHUNKS = 4
CHUNK_SIZE = 500
LLM_PROVIDER = "groq"
```

---

## 📚 Useful Commands

```bash
# Virtual environment
python -m venv venv              # Create
source venv/bin/activate         # Activate (Mac/Linux)
venv\Scripts\activate.bat        # Activate (Windows)

# Dependencies
pip install -r requirements.txt  # Install all
pip install package-name         # Install one
pip list                         # See installed
pip freeze > requirements.txt    # Update requirements

# Running
python main.py                   # Start API
streamlit run app_ui.py         # Start UI
python test_api.py document.pdf # Test with PDF

# Debugging
python -c "import config; print(config.SUPABASE_URL)"
python -m pytest tests/          # Run tests

# Docker
docker build -t hospital-rag .   # Build image
docker run -p 8000:8000 hospital-rag  # Run
docker-compose up                # Compose start
```

---

## 🔗 Important Links

- **Supabase**: https://supabase.com
- **OpenAI**: https://platform.openai.com
- **Groq**: https://console.groq.com
- **FastAPI**: https://fastapi.tiangolo.com
- **Streamlit**: https://streamlit.io
- **LangChain**: https://python.langchain.com

---

## 💡 Pro Tips

1. **Use Groq for free LLM** - Fast and free
2. **Start with small PDFs** - Easier to test
3. **Test with test_api.py** - Verify setup
4. **Use Docker for consistency** - Works everywhere
5. **Monitor API costs** - Watch OpenAI usage
6. **Backup documents table** - Regular Supabase backups
7. **Enable caching** - Redis for production
8. **Use GPT-4 for quality** - Better answers

---

## ❓ Still Need Help?

1. Check `TROUBLESHOOTING.md` - Common issues
2. Read `README.md` - Full documentation
3. See `ARCHITECTURE.md` - System design
4. Review `DEPLOYMENT.md` - Setup options
5. Run `test_api.py` - Test everything

---

**Last Updated**: 2024
**Version**: 1.0
