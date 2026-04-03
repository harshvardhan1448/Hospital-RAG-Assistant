# Hospital RAG Assistant - Getting Started (5 Min Setup)

## ✅ What You're Getting

A production-ready RAG (Retrieval-Augmented Generation) system that:
- ✅ Uploads and processes hospital PDFs
- ✅ Converts documents to embeddings for semantic search
- ✅ Stores vectors in Supabase (pgvector)
- ✅ Answers questions using retrieved document context only
- ✅ Prevents AI hallucination with strict RAG constraints
- ✅ Provides REST API + Beautiful Streamlit UI

---

## 🎯 Quick Setup 

### Method to Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate      # Linux/Mac
# OR
venv\Scripts\activate.bat      # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy configuration
cp .env.example .env

# 4. Edit .env with your API keys
nano .env  # Linux/Mac
# OR
notepad .env  # Windows
```

---

## 🔑 Step 1: Get API Keys (10 Minutes)

### A. Supabase Setup (Database)

1. Go to [supabase.com](https://supabase.com) → Sign Up
2. Create a new project
3. Copy credentials:
   - Go to **Settings** → **API**
   - Copy **Project URL** → Add to `.env` as `SUPABASE_URL`
   - Copy **Anon public key** → Add to `.env` as `SUPABASE_KEY`

4. Run database setup (one-time):
   - Go to **SQL Editor** in Supabase dashboard
   - Create new query
   - Copy entire content of `supabase_setup.sql`
   - Paste into SQL Editor
   - Click **Run**

✅ Database is ready!

### B. OpenAI API Key (For Embeddings)

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create new API key
3. Add to `.env` as `OPENAI_API_KEY`

⚠️ Free trial may be expired. Add payment method if needed.

### C. Groq API Key (For LLM - RECOMMENDED & FREE)

1. Go to [console.groq.com](https://console.groq.com) → Sign Up
2. Create API key
3. Add to `.env` as `GROQ_API_KEY`

✅ Free tier has generous limits!

### Your `.env` file should look like:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUz...
OPENAI_API_KEY=sk-proj-...
GROQ_API_KEY=gsk_...
LLM_PROVIDER=groq
API_BASE_URL=http://localhost:8000
```

---

## 🚀 Step 2: Start the Application

### Terminal 1 - Start Backend API:
```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ API is running at http://localhost:8000

### Terminal 2 - Start Frontend UI:
```bash
streamlit run app_ui.py
```

You should see:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

✅ UI is running at http://localhost:8501

---

## 📤 Step 3: Upload Your First Document

1. Open http://localhost:8501 in browser
2. In left sidebar, click **"Upload Hospital Document (PDF)"**
3. Select a hospital PDF file
4. Click **"📤 Upload Document"**
5. Wait for processing (you'll see: "✓ Document uploaded successfully!")

⚠️ First upload takes longer (generates embeddings)

---

## 💬 Step 4: Ask Questions

1. In main chat area, type a question:
   - "What are OPD timings?"
   - "Who is the cardiologist?"
   - "What is the cost of MRI?"

2. Click **"🔍 Ask"**

3. See the AI answer with sources!

---

## 🧪 Step 5: Verify Everything Works

```bash
# In a third terminal, test the API
python test_api.py path/to/hospital.pdf
```

This will:
- ✅ Test API health
- ✅ Upload document
- ✅ Test example queries
- ✅ Show results

---

## 📊 Project Structure

```
NexovAi/
├── 🔧 Core Components
│   ├── main.py              # FastAPI backend
│   ├── app_ui.py            # Streamlit UI
│   ├── ingestion.py         # PDF processing
│   ├── rag_pipeline.py      # Answer generation
│   └── supabase_db.py       # Database manager
│
├── ⚙️ Configuration
│   ├── config.py            # Settings
│   ├── .env.example         # Template
│   └── requirements.txt     # Dependencies
│
├── 🗄️ Database
│   └── supabase_setup.sql   # Create tables
│
├── 📚 Documentation
│   ├── README.md            # Full docs
│   ├── QUICK_REFERENCE.md   # Cheat sheet
│   ├── ARCHITECTURE.md      # System design
│   ├── DEPLOYMENT.md        # Deploy guide
│   └── TROUBLESHOOTING.md   # Fix issues
│
└── 🚢 Deployment
    ├── Dockerfile           # Docker image
    └── docker-compose.yml   # Services
```

---

## 🎯 Next Steps

### Immediate (after setup):
- [ ] Test with sample PDF
- [ ] Ask example queries
- [ ] Run `test_api.py`

### Short Term (next few hours):
- [ ] Customize `config.py` for your needs
- [ ] Test with your actual hospital PDFs
- [ ] Verify answers are accurate

### Medium Term (next few days):
- [ ] Deploy to production (see DEPLOYMENT.md)
- [ ] Setup monitoring
- [ ] Add your branding

### Long Term (optional):
- [ ] Add chat history persistence
- [ ] Implement multi-document awareness
- [ ] Add re-ranking for better results
- [ ] Setup voice input

---

## ⚡ Common Tasks

### Change Configuration
Edit `config.py`:
```python
TOP_K_CHUNKS = 5        # More context
CHUNK_SIZE = 1000       # Larger chunks
LLM_PROVIDER = "openai" # Use GPT instead of Groq
```

### Switch LLM Provider
Edit `.env`:
```
# Use Groq (free, fast)
LLM_PROVIDER=groq
GROQ_API_KEY=your-key

# OR use OpenAI (more capable)
LLM_PROVIDER=openai
OPENAI_API_KEY=your-key
```

### Delete a Document
In Streamlit UI:
1. Go to **📋 Uploaded Documents** in sidebar
2. Click **🗑️ Delete** next to document name

### Test API Directly
```bash
# Upload
curl -X POST "http://localhost:8000/upload" \
  -F "file=@hospital.pdf"

# Query
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What are OPD timings?"}'
```

---

## 🆘 Troubleshooting

### "Cannot connect to API"
```bash
# Make sure API is running
python main.py
```

### "API key error"
```bash
# Check .env file has correct keys
cat .env

# Reload environment
deactivate
source venv/bin/activate
```

### "No documents found"
```bash
# Upload a PDF first in Streamlit UI
# Or use: python test_api.py document.pdf
```

### "Getting wrong answers"
1. Check document was uploaded
2. Increase `TOP_K_CHUNKS` in config.py
3. Check chunk size matches document content

**See TROUBLESHOOTING.md for more help!**

---

## 📖 Learning Resources

- **QUICK_REFERENCE.md** - Commands cheat sheet
- **README.md** - Full documentation
- **ARCHITECTURE.md** - How it all works
- **DEPLOYMENT.md** - Deploy to production
- **test_api.py** - See API in action

---

## 🎓 What You Learned

This system demonstrates:
- ✅ **RAG Architecture** - Real-world AI pattern
- ✅ **Vector Databases** - Semantic search with embeddings
- ✅ **LLM Integration** - Using modern language models
- ✅ **API Design** - RESTful backend design
- ✅ **Document Processing** - PDF extraction & chunking
- ✅ **Full Stack** - Backend + frontend application

**Perfect for:**
- AI/ML interviews
- Production portfolio
- Enterprise systems
- Learning RAG systems

---

## 💡 Pro Tips

1. **Use Groq for free** - Unlimited free LLM calls
2. **Start small** - Test with simple PDFs first
3. **Monitor costs** - Watch OpenAI embedding usage
4. **Cache queries** - Add Redis for production
5. **Use Docker** - Deploy consistently everywhere

---

## 🎉 You're Ready!

Your Hospital RAG Assistant is now:
- ✅ Running locally
- ✅ Fully configured
- ✅ Ready to use
- ✅ Production-ready
- ✅ Documented

**Next:** Upload a PDF and start asking questions!

---

## 📞 Need Help?

1. Check `TROUBLESHOOTING.md` - 90% of issues covered
2. Review `QUICK_REFERENCE.md` - Common commands
3. Read `README.md` - Detailed documentation
4. Check API docs: http://localhost:8000/docs

**Time to completion:** ~30 minutes total setup

**Happy coding! 🚀**
