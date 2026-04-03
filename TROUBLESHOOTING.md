# 🔧 Troubleshooting Guide

Got a problem? Find it here and fix it!

---

## 🎯 Common Issues & Fixes

### "Cannot connect to API"

**Error message:**
```
Error: Cannot connect to API at http://localhost:8000
```

**What it means:** Backend server isn't running

**Fix:**
1. Open a terminal
2. Navigate to your project folder
3. Run: `python main.py`
4. Wait for: `✓ Application initialized successfully`
5. Don't close this terminal!

---

### "supabase_url is required"

**Error message:**
```
Warning: Could not verify Supabase connection: supabase_url is required
```

**What it means:** Your `.env` file is missing

**Fix:**
1. Make sure you have a file named `.env` (not `.env.example`)
2. In `.env`, add your Supabase credentials:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-key-here
   GROQ_API_KEY=your-groq-key
   API_BASE_URL=http://localhost:8000
   ```
3. Save the file
4. Restart the backend: `python main.py`

---

### "ModuleNotFoundError: No module named XXX"

**Error message:**
```
ModuleNotFoundError: No module named 'supabase'
```

**What it means:** Missing Python libraries

**Fix:**
```bash
# Install all dependencies
pip install -r requirements.txt

# If still broken, reinstall:
pip install -r requirements.txt --force-reinstall
```

---

### "Port 8000 is already in use"

**Error message:**
```
ERROR: Address already in use
Port 8000 is already in use
```

**What it means:** Another program is using port 8000

**Fix (Windows):**
```bash
# Find and kill the process
taskkill /F /IM python.exe

# Or change the port in main.py and rerun
```

**Fix (Mac/Linux):**
```bash
# Find the process
lsof -i :8000

# Kill it
kill -9 [PID]

# Or restart your computer
```

---

### "Upload takes forever" or "Hangs"

**What's happening:** First upload generates embeddings (normal!)

**Fix:**
1. **This is expected!** First PDF takes 1-2 minutes
2. **Wait patiently** - Terminal will show progress
3. **Second uploads** are much faster (1-10 seconds)
4. If it takes >5 minutes, something's wrong. Kill and restart.

---

### "0 relevant chunks retrieved"

**Error message:**
```
Answer: I don't have that information in the provided document.
📊 0 relevant chunks retrieved
```

**What it means:** System couldn't find the answer in your documents

**Fix:**
1. **Is the answer in your PDF?** Double-check the document
2. **Try a different question** with different words
3. **Make sure document is uploaded** (check left sidebar)
4. **Try simpler questions** (e.g., "What number?" instead of "What is the numerical value of X?")

---

### "Invalid API Key"

**Error message:**
```
GROQ_API_KEY is invalid
SUPABASE_KEY is invalid
```

**What it means:** Your API keys are wrong or expired

**Fix:**
1. **For Groq Key:**
   - Go to https://console.groq.com
   - Generate a new key
   - Copy to `.env`

2. **For Supabase Key:**
   - Go to your Supabase Dashboard
   - Settings → API
   - Copy "Anon public" key
   - Paste into `.env`

3. **Restart everything:**
   ```bash
   # Terminal 1
   python main.py
   ```

---

### "Database creation failed" or "Table doesn't exist"

**Error message:**
```
Error: relation "documents" does not exist
```

**What it means:** You skipped the database setup step

**Fix:**
1. Go to your Supabase Dashboard
   - https://console.supabase.com
2. Click **SQL Editor**
3. Click **New Query**
4. Copy entire content of `supabase_setup.sql` file
5. Paste into the SQL editor
6. Click **Run**
7. Should see: "Query succeeded!"
8. Restart your backend

---

### "Streamlit won't start"

**Error message:**
```
CommandNotFoundError: No module named streamlit
```

**What it means:** Streamlit not installed

**Fix:**
```bash
pip install streamlit

# Or reinstall everything
pip install -r requirements.txt
```

Then:
```bash
streamlit run app_ui.py
```

---

### "Browser doesn't open automatically"

**What to do:**
1. **Check your terminal** for this line:
   ```
   Local URL: http://localhost:8501
   ```
2. **Copy that URL**
3. **Open your browser**
4. **Paste and press Enter**

---

## 🎯 Network & Connection Issues

### "Cannot reach Supabase"

**Error message:**
```
Error connecting to Supabase database
```

**What it means:** Internet connection or Supabase is down

**Fix:**
1. Check your internet connection
2. Try accessing Supabase dashboard directly
   - https://console.supabase.com
3. If Supabase is down, wait and try again
4. Check Supabase status: https://status.supabase.com

---

### "Cannot reach Groq API"

**Error message:**
```
Error: Failed to connect to Groq API
```

**What it means:** Internet issue or Groq is unavailable

**Fix:**
1. Check your internet
2. Verify `GROQ_API_KEY` is correct
3. Try this in a terminal to check internet:
   ```bash
   ping google.com
   ```
4. Check Groq status on Twitter @groq_dev

---

## 🛠️ Advanced Debugging

### Check what's running on port 8000

**Windows:**
```bash
netstat -ano | findstr :8000
```

**Mac/Linux:**
```bash
lsof -i :8000
```

### See detailed error logs

**Add to main.py:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Then run:
```bash
python main.py
```

### Test API directly

```bash
# In a new terminal, test health check
curl http://localhost:8000/

# Should return:
# {"status":"healthy","message":"Hospital RAG Assistant API is running"}
```

---

## 💾 Database Issues

### Reset database (delete all documents)

⚠️ **Warning: This deletes everything!**

1. Go to Supabase Dashboard
2. SQL Editor → New Query
3. Run:
   ```sql
   DELETE FROM documents;
   ```
4. Click Run

---

### View what's in database

```bash
# In Supabase SQL Editor:
SELECT COUNT(*) FROM documents;
SELECT filename, COUNT(*) as chunks FROM documents GROUP BY filename;
```

---

## 🚀 Performance Issues

### "Everything is slow"

**Possible causes:**
1. **First upload?** Normal - takes 1-2 min
2. **Embedding model loading?** Normal - first question takes longer
3. **Too many documents?** Try deleting old ones
4. **Low RAM?** Close other programs

**Fix:**
```bash
# Check system resources
# Make sure you have at least 2GB free RAM
# Close Firefox, Chrome, etc.
# Restart backend and UI
```

---

### "Embedding model won't download"

**Error:**
```
Warning: Downloading  (some model)...
```

**What to do:**
1. This is normal! First time downloading
2. Takes 1-2 minutes
3. Wait patiently
4. Next time will be instant

---

## 📋 Cannot Find Help?

Still stuck? Check:

1. **README.md** - Full documentation
2. **GETTING_STARTED.md** - Step-by-step setup
3. **QUICK_REFERENCE.md** - Common commands
4. **ARCHITECTURE.md** - How system works

**Or:** Add `--verbose` to commands for more details!

---

## ✅ Verification Checklist

If things seem broken, go through this:

- [ ] `.env` file exists with correct keys?
- [ ] Backend running (`python main.py`)?
- [ ] UI running (`streamlit run app_ui.py`)?
- [ ] Can access http://localhost:8501?
- [ ] At least one PDF uploaded?
- [ ] Questions are being asked correctly?
- [ ] Terminal shows errors? Read error messages!
- [ ] Restarted everything recently?

If all checked, it should work!

---

## 📞 Last Resort

If nothing works:

1. **Kill everything:**
   ```bash
   # Close both terminals (Ctrl+C)
   # Or: taskkill /F /IM python.exe
   ```

2. **Clean start:**
   ```bash
   rm -rf __pycache__
   pip install -r requirements.txt --force-reinstall
   ```

3. **Restart from scratch:**
   ```bash
   python main.py           # Terminal 1
   streamlit run app_ui.py  # Terminal 2
   ```

Good luck! 🍀
```

**Solutions:**
1. Verify FastAPI is running:
   ```bash
   python main.py
   # Should show: Uvicorn running on http://0.0.0.0:8000
   ```

2. Check if port 8000 is in use:
   ```bash
   # Windows (PowerShell)
   Get-NetTCPConnection -LocalPort 8000
   
   # Linux/Mac
   lsof -i :8000
   ```

3. Kill process on port 8000:
   ```bash
   # Windows
   taskkill /PID <pid> /F
   
   # Linux/Mac
   kill -9 <PID>
   ```

4. Try different port:
   ```bash
   # Edit config.py
   API_PORT = 8001  # Change to different port
   ```

### Problem: API responds but returns error

**Error:**
```
{
  "status": "error",
  "message": "..."
}
```

**Check the error message:**
- "Supabase" error → Fix database credentials
- "OpenAI" error → Check API key
- "Groq" error → Check API key
- "Connection" error → Check internet connection

---

## Database (Supabase) Issues

### Problem: "Invalid Supabase credentials"

**Error:**
```
Error: Could not connect to Supabase
```

**Solutions:**
1. Verify credentials in `.env`:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key-abc123xyz
   ```

2. Check credentials format:
   - URL should start with `https://`
   - Key should be long alphanumeric string
   - No quotes around values in .env

3. Get correct credentials:
   - Go to [supabase.com](https://supabase.com) dashboard
   - Select your project
   - Settings → API
   - Copy "Project URL" and "Anon public key"

4. Test connection:
   ```bash
   python -c "from supabase_db import get_supabase_manager; print('OK')"
   ```

### Problem: "Table does not exist"

**Error:**
```
Error: relation "documents" does not exist
```

**Solutions:**
1. Run the Supabase setup SQL:
   - Open `supabase_setup.sql`
   - Go to Supabase dashboard → SQL Editor
   - Create new query → paste content → Run

2. Verify table was created:
   ```
   SELECT table_name FROM information_schema.tables WHERE table_schema='public'
   ```

3. Check extensions:
   ```
   SELECT extname FROM pg_extension WHERE extname='vector'
   ```

### Problem: "pgvector extension not found"

**Error:**
```
Error: type "vector" does not exist
```

**Solutions:**
1. Enable pgvector in Supabase:
   - Dashboard → SQL Editor
   - Run: `CREATE EXTENSION IF NOT EXISTS vector;`

2. Verify extension:
   ```
   SELECT * FROM pg_extension WHERE extname = 'vector';
   ```

---

## LLM (Language Model) Issues

### Problem: "Groq API Error"

**Error:**
```
Error: Invalid Groq API key
```

**Solutions:**
1. Get free Groq API key:
   - Go to [console.groq.com](https://console.groq.com)
   - Sign up and create API key
   - Copy key to `.env`

2. Verify key format:
   ```bash
   echo $GROQ_API_KEY  # Should show long key
   ```

3. Test connection:
   ```bash
   curl -H "Authorization: Bearer YOUR_KEY" \
        "https://api.groq.com/openai/v1/models"
   ```

### Problem: "OpenAI API Error"

**Error:**
```
Error: Invalid OpenAI API key
```

**Solutions:**
1. Get OpenAI API key:
   - Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Create new API key
   - Copy to `.env`

2. Verify account has credits:
   - Check [platform.openai.com/account/billing](https://platform.openai.com/account/billing)
   - Add payment method if needed

3. Check API limits:
   - Some accounts have free trial only (expired)
   - New accounts need credit card

### Problem: "Rate limit exceeded"

**Error:**
```
Error 429: Too many requests
```

**Solutions:**
1. Switch to Groq (free, higher limits):
   ```bash
   LLM_PROVIDER=groq
   ```

2. Add delays between requests:
   ```python
   import time
   time.sleep(1)  # Wait 1 second between requests
   ```

3. Upgrade OpenAI plan:
   - Add payment method
   - Request higher rate limits

---

## Embedding Issues

### Problem: "Embedding API error"

**Error:**
```
Error: Invalid OpenAI API key
```

**Solutions:**
1. Embeddings use OpenAI API (not Groq)
2. Need valid OpenAI API key
3. Only embeddings require OpenAI; LLM can use Groq

### Problem: "Too many embedding requests"

**Solutions:**
1. Use smaller chunk size:
   ```python
   CHUNK_SIZE = 300  # Reduce from 500
   ```

2. Reduce batch size:
   ```python
   # In ingestion.py, reduce batch_size
   batch_size = 50  # From 100
   ```

3. Wait between uploads:
   ```bash
   # Upload one document, wait 30s, upload next
   ```

---

## Document Upload Issues

### Problem: "PDF upload fails"

**Error:**
```
Error: Could not extract text from PDF
```

**Solutions:**
1. Verify PDF is valid:
   - Try opening in Adobe Reader
   - Check file isn't corrupted

2. Try different PDF:
   - Might be encrypted/protected
   - Try simpler PDF file

3. Check file size:
   - If > 50MB, might timeout
   - Split large PDFs

4. Enable debug logging:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

### Problem: "No results returned"

**Error:**
```
No chunks found
```

**Solutions:**
1. Verify document was uploaded:
   - Check Supabase database
   - Run: `SELECT COUNT(*) FROM documents`

2. Check chunk content:
   ```
   SELECT content FROM documents LIMIT 5
   ```

3. Verify embeddings were created:
   ```
   SELECT embedding FROM documents LIMIT 5
   ```

---

## Query & RAG Issues

### Problem: "Wrong answer from query"

**Error:**
```
Answer doesn't match document content
```

**Solutions:**
1. Verify document is in database:
   ```bash
   # Use Streamlit UI → Documents tab
   # Or test_api.py
   ```

2. Check if top-k chunks are relevant:
   - Increase TOP_K_CHUNKS in config.py
   - Try: `TOP_K_CHUNKS = 5` instead of 4

3. Check embeddings quality:
   - Might need to re-embed documents
   - Delete document and re-upload

4. Adjust chunk size:
   - Larger chunks: `CHUNK_SIZE = 1000`
   - Smaller chunks: `CHUNK_SIZE = 250`

### Problem: "I don't have that information"

**This is correct behavior if:**
- Information isn't in document
- System is working as designed (RAG constraint)
- No chunking covers this question

**Not a bug unless:**
- Information IS in document
- Other questions work fine for same document

### Problem: "LLM generates hallucinated answers"

**Solutions:**
1. Improve retrieval:
   - Better chunk strategy
   - Increase TOP_K_CHUNKS
   - Use hybrid search (keyword + semantic)

2. Improve prompt:
   - Edit RAG_PROMPT in rag_pipeline.py
   - Make constraints clearer

3. Use different LLM:
   - GPT-4 (more accurate)
   - Better parameterization

---

## Performance Issues

### Problem: "Query is very slow"

**Error:**
```
Taking > 30 seconds to answer
```

**Solutions:**
1. Check vector search performance:
   ```sql
   -- In Supabase SQL
   EXPLAIN ANALYZE
   SELECT * FROM documents
   ORDER BY embedding <=> query_embedding
   LIMIT 5;
   ```

2. Optimize indexes:
   ```sql
   -- Recreate index
   DROP INDEX documents_embedding_idx;
   CREATE INDEX documents_embedding_idx ON documents 
   USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
   ```

3. Reduce retrieval scope:
   ```python
   TOP_K_CHUNKS = 3  # From 4
   ```

4. Cache embeddings:
   - Add Redis caching layer
   - Cache popular queries

### Problem: "High memory usage"

**Error:**
```
Application uses lots of RAM
```

**Solutions:**
1. Reduce batch processing:
   ```python
   batch_size = 50  # From 100
   ```

2. Reduce model size:
   - Use smaller embedding model
   - Use distilled LLM

3. Enable pagination:
   - Process documents in smaller chunks
   - Clear cache regularly

---

## Streamlit UI Issues

### Problem: "Streamlit won't start"

**Error:**
```
Error: Could not find Streamlit command
```

**Solutions:**
```bash
# Install Streamlit
pip install streamlit

# Or reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Problem: "UI doesn't connect to API"

**Error:**
```
Cannot connect to API at http://localhost:8000
```

**Solutions:**
1. Verify API is running:
   ```bash
   # Terminal 1
   python main.py
   ```

2. Update API URL in .env:
   ```bash
   API_BASE_URL=http://localhost:8000
   ```

3. Clear Streamlit cache:
   ```bash
   streamlit cache clear
   ```

---

## Docker Issues

### Problem: "Docker image build fails"

**Solutions:**
```bash
# Clean up Docker
docker system prune

# Try again
docker-compose build --no-cache

# Check logs
docker-compose build --verbose
```

### Problem: "Container exits immediately"

**Solutions:**
```bash
# Check logs
docker logs hospital-rag-api

# Run interactively
docker run -it hospital-rag-api /bin/bash

# Check environment
docker exec hospital-rag-api env
```

---

## Getting Help

### Debug Information to Gather

Before seeking help, collect:
1. **Python version**: `python --version`
2. **OS**: Windows/Mac/Linux
3. **Error message**: Full stack trace
4. **Logs**:
   ```bash
   # From main.py terminal
   tail -100 app.log
   ```
5. **Environment**: `.env` file (without secrets)
6. **Configuration**: `config.py` settings

### Debug Checklist

```bash
# Run comprehensive test
python test_api.py path/to/test.pdf

# Check dependencies
pip list

# Test components individually
python -c "from supabase_db import get_supabase_manager; print('✓ Supabase')"
python -c "from ingestion import get_embeddings_client; print('✓ Embeddings')"
python -c "from rag_pipeline import get_llm_client; print('✓ LLM')"
```

### Useful Commands for Debugging

```bash
# Check if port is in use
netstat -tuln | grep 8000

# Monitor API
curl -v http://localhost:8000/

# Check database
psql -h your-db.supabase.co -U postgres -d postgres

# View logs
docker logs hospital-rag-api

# Real-time logs
docker-compose logs -f api
```

---

## Common Misconfigurations

| Issue | Check |
|-------|-------|
| Embeddings fail | OPENAI_API_KEY set? Has credits? |
| Queries slow | SUPABASE_URL correct? Index created? |
| No results | Document uploaded? Chunks created? |
| Wrong answers | TOP_K_CHUNKS correct? Chunk size good? |
| API won't start | Port 8000 free? Dependencies installed? |

---

## Support Resources

- **Documentation**: `README.md`
- **Architecture**: `ARCHITECTURE.md`
- **Deployment**: `DEPLOYMENT.md`
- **API Tests**: `test_api.py`
- **Supabase Docs**: https://supabase.com/docs
- **LangChain Docs**: https://python.langchain.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com

---

**Last Updated**: 2024
**Version**: 1.0
