# 🚀 Getting Started - 5 Minute Setup

Welcome! This guide will get you up and running in just 5 minutes.

## ✨ What You're Building

A smart AI assistant that:
- 📄 Reads your hospital PDF documents
- 🧠 Understands what's in them
- 💬 Answers your questions about them
- 📍 Shows you where the answer came from
- **💰 Costs $0/month** - Completely FREE!

No complicated setup. No expensive APIs. Just you, your documents, and an AI.

---

## 📋 Prerequisites (30 seconds)

You need:
- ✅ Python 3.9+ installed ([python.org](https://python.org))
- ✅ A text editor (Notepad, VS Code, etc.)
- ✅ A browser (Chrome, Firefox, Safari, Edge)

That's it! No credit card needed.

---

## 🎯 Setup (4 steps, 5 minutes)

### Step 1️⃣: Download & Install (1 minute)

```bash
# Clone the project
git clone https://github.com/harshvardhan1448/Hospital-RAG-Assistant.git
cd Hospital-RAG-Assistant

# Create virtual environment (recommended)
python -m venv venv

# Activate it
source venv/bin/activate      # On Mac/Linux
# OR
venv\Scripts\activate.bat      # On Windows

# Install dependencies (takes 1 minute)
pip install -r requirements.txt
```

✅ Done! You've installed everything needed.

---

### Step 2️⃣: Get Free API Keys (3 minutes)

#### 🔹 Get Supabase Key (Database)

1. Go to **[supabase.com](https://supabase.com)**
2. Click **"Start your project"** 
3. Sign up with email (takes 60 seconds)
4. Create a new project (just click "Create Project", wait 30 seconds)
5. Once created, click **Settings** → **API**
6. Copy these two values to a text file:
   - **Project URL** (looks like `https://abc123.supabase.co`)
   - **Anon public** (long string starting with `eyJ...`)

That's it for Supabase!

#### 🔹 Get Groq Key (AI Model)

1. Go to **[console.groq.com](https://console.groq.com)**
2. Sign up (takes 1 minute)
3. Click **API Keys** on the left
4. Click **Create New API Key**
5. Copy the key (looks like `gsk_...`)

Done! You now have all the keys you need.

✅ **No payment needed!** Free tier is unlimited.

---

### Step 3️⃣: Configure Your App (1 minute)

1. Open your project folder in a text editor
2. Find the file `.env.example`
3. Create a new file called `.env` (the same folder)
4. Copy-paste this into `.env`:

```
SUPABASE_URL=paste_your_supabase_url_here
SUPABASE_KEY=paste_your_supabase_key_here
GROQ_API_KEY=paste_your_groq_key_here
API_BASE_URL=http://localhost:8000
```

5. Replace the values with what you copied from Supabase and Groq
6. Save the file

✅ Configuration done!

---

### Step 4️⃣: Setup Database (1 minute, one-time)

This creates the table where your documents will live.

1. Go to your **Supabase Dashboard** 
   - [Go to console.supabase.com](https://console.supabase.com)
2. Select the project you created
3. On the left sidebar, click **SQL Editor**
4. Click **New Query** (or **+ icon**)
5. Open the file `supabase_setup.sql` from your project folder
6. **Copy everything** in that file
7. **Paste** it into the Supabase SQL Editor
8. Click **Run** (at the bottom right)

You should see: "Query succeeded!"

✅ Your database is ready!

---

## 🎬 Run the Application

Now the fun part! Open **two terminal windows** side by side.

### Window 1: Start the AI Backend

```bash
python main.py
```

You should see:
```
✓ Application initialized successfully
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ Backend is running!

### Window 2: Start the Web Interface

```bash
streamlit run app_ui.py
```

You should see:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

✅ A browser window should open automatically!

---

## 🎉 First Use

### 1. Upload a PDF

1. In the left sidebar, you'll see **"Upload Hospital Document (PDF)"**
2. Click the area or the **"Upload Document"** button
3. Select a hospital PDF from your computer
4. Wait for it to upload (you'll see a progress message)

### 2. Ask a Question

1. In the main area, type a question:
   ```
   What are the OPD timings?
   ```

2. Click the **"Ask"** button (or press Enter)

3. The AI reads your documents and gives you an answer with sources!

### 3. Try More Questions

```
Who is the cardiologist?
What is the MRI cost?
What is the emergency number?
Can I cancel appointments?
```

---

## ✅ Everything Working?

If you see:
- ✅ AI answers appear in the web interface
- ✅ Answers show source pages
- ✅ No red error messages
- ✅ Uploaded documents appear in the sidebar

**Congratulations! 🎊 You're all set!**

---

## 📞 Quick Help

### "I got an error about missing keys"
→ Make sure `.env` file exists and has the correct values

### "Database connection failed"  
→ Check that `SUPABASE_URL` and `SUPABASE_KEY` are correct

### "Upload hangs or takes too long"
→ First time takes longer (generating embeddings). Be patient!

### "API won't start"
→ Make sure port 8000 is not used by another app

See **TROUBLESHOOTING.md** for more help!

---

## 📚 Next Steps

Now that it's working:

1. **Test with real documents** - Upload your actual hospital PDFs
2. **Read QUICK_REFERENCE.md** - Useful commands and tips
3. **Check ARCHITECTURE.md** - Understand how it works
4. **Customize config.py** - Change how many results, chunk sizes, etc.

---

## 🎯 Example Questions to Try

Use a hospital PDF and ask:

```
"What are OPD timings?"
"Emergency number?"
"Cost of MRI scan?"
"Cardiology department location?"
"ICU cost per day?"
"Can I cancel within 24 hours?"
```

Enjoy! 🚀
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
