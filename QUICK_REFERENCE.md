# ⚡ Quick Reference Guide

This is your cheat sheet. Keep this handy!

---

## 🎯 5-Second Setup Reminder

```bash
cp .env.example .env              # Copy env template
# Edit .env with your API keys     # Add Supabase + Groq keys
python main.py                    # Terminal 1: Start backend
streamlit run app_ui.py           # Terminal 2: Start UI
```

Then open: **http://localhost:8501**

---

## 📍 Where Things Are

| What | Location | What It Does |
|------|----------|--------------|
| Upload button | Left sidebar | Upload PDF documents |
| Ask questions | Top of page | Type questions here |
| Results | Middle area | See AI answers |
| Chat history | Left sidebar | See past questions |
| Your documents | Left sidebar | List of uploaded PDFs |
| API docs | http://localhost:8000/docs | Test API endpoints |
| Logs | Terminal window | See what's happening |

---

## 💬 API Command Reference

### Upload a PDF
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@your_hospital.pdf"
```

### Ask a Question
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the emergency number?"}'
```

### Get List of All Documents
```bash
curl "http://localhost:8000/documents"
```

### Delete a Document
```bash
curl -X DELETE "http://localhost:8000/documents/hospital.pdf"
```

---

## ⚙️ Tweaking Settings

Edit `config.py` to customize:

### For Better Answers (Slower):
```python
TOP_K_CHUNKS = 6          # Fetch more similar chunks (default: 4)
CHUNK_SIZE = 1000         # Bigger text chunks (default: 500)
CHUNK_OVERLAP = 200       # More context sharing (default: 100)
```

### For Faster Answers (Less Accurate):
```python
TOP_K_CHUNKS = 2          # Fetch fewer chunks
CHUNK_SIZE = 300          # Smaller chunks
CHUNK_OVERLAP = 50        # Less overlap
```

### Change AI Model
The system uses:
- **Embeddings**: `all-MiniLM-L6-v2` (local, 384-dim)
- **LLM**: `llama-3.1-8b-instant` (Groq)

To change, edit `config.py`:
```python
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Can't change (local only)
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "supabase_url is required" | Add `SUPABASE_URL` to `.env` |
| "API won't start" | Port 8000 in use. Kill other Python processes |
| "Upload hangs" | Normal! First upload takes 1-2 min |
| "Can't connect to Groq" | Check `GROQ_API_KEY` in `.env` |
| "Found 0 chunks" | Document might not have answer. Try different question |
| "Database error" | Restart both terminals (backend + UI) |

---

## 📊 Understanding the Output

When you ask a question, you see:

```
Question: What are OPD timings?

Answer: The OPD timings are 9:00 AM to 5:00 PM.

Sources: page 1
📊 2 relevant chunks retrieved
```

**What this means:**
- ✅ Question was answered
- ✅ System found 2 chunks with info
- ✅ Sources show where answer came from

---

## 🔍 Example Queries to Try

Copy-paste these into the question box:

```
What are the OPD timings?
Who is the cardiologist?
What is the MRI cost?
Emergency number?
Can I cancel within 24 hours?
What is the ICU cost per day?
```

---

## 📂 Project Structure at a Glance

```
Hospital-RAG-Assistant/
├── main.py              ← Start backend
├── app_ui.py            ← Start UI
├── ingestion.py         ← Document processing
├── rag_pipeline.py      ← Question answering
├── supabase_db.py       ← Database operations
├── embeddings.py        ← Embedding creation
├── config.py            ← Settings (edit this!)
├── requirements.txt     ← Dependencies
├── .env                 ← Your API keys (don't commit!)
├── supabase_setup.sql   ← Database schema
└── README.md            ← Full documentation
```

---

## 🚀 Performance Tips

| Task | Time | Notes |
|------|------|-------|
| First upload | 1-2 min | Creates embeddings |
| 2nd+ uploads | 10-30 sec | Reuses loaded model |
| Question | 1-3 sec | Most models are cached |
| Database search | 100ms | Fast vector search |

**Tip**: First upload is slow because it downloads the embedding model. Subsequent uploads are much faster!

---

## 🔐 Security Checklist

- [ ] `.env` file created? (not `.env.example`)
- [ ] `.env` added to `.gitignore`? (it should be)
- [ ] API keys kept secret? (never in code)
- [ ] Not sharing `.env` with anyone?
- [ ] Not uploading `.env` to GitHub?

---

## 📞 Common Questions

**Q: Do I need to pay?**
A: No! Free APIs only (Supabase free tier, Groq free tier)

**Q: Is my data private?**
A: Yes! Stored in YOUR Supabase, you control access

**Q: Can I use other PDF files?**
A: Yes! Any PDF works. Hospital documents are examples

**Q: Can I add more documents?**
A: Yes! Upload as many as you want (free tier: unlimited)

**Q: What if answer is wrong?**
A: System can only answer from uploaded documents. Try different question

**Q: How much can I upload?**
A: Supabase free tier: plenty. See their pricing for limits

---

## 🎯 Next Steps

1. **Try example questions** (see list above)
2. **Upload real PDFs** and test
3. **Look at ARCHITECTURE.md** to understand how it works
4. **Check TROUBLESHOOTING.md** if issues arise
5. **Visit DEPLOYMENT.md** when ready to share

---

## 💡 Pro Tips

- 💡 Ask specific questions ("What is?" vs "Tell me about")
- 💡 Longer chunks = more context but slower
- 💡 Upload 1-2 test PDFs first
- 💡 Check API logs if something breaks
- 💡 Keep `.env` file safe!

---

## 🆘 Emergency Commands

```bash
# Kill everything and restart
taskkill /F /IM python.exe          # Windows

# Check if ports are in use
lsof -i :8000                       # Mac/Linux
netstat -ano | findstr :8000        # Windows

# Force refresh (clear cache)
rm -rf __pycache__                 # Linux/Mac
rmdir /s __pycache__               # Windows

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```
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
