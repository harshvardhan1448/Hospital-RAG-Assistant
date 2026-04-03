# Hospital RAG Assistant - Troubleshooting Guide

## Quick Issue Lookup

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named` | Install missing packages: `pip install -r requirements.txt` |
| `Cannot connect to API at http://localhost:8000` | Start FastAPI backend: `python main.py` |
| `SUPABASE_URL or SUPABASE_KEY not set` | Copy `.env.example` to `.env` and fill in values |
| `OpenAI API Error: Invalid API Key` | Verify OPENAI_API_KEY in .env is correct |
| `No documents found in database` | Upload a PDF first using the UI or test_api.py |

---

## Installation & Setup Issues

### Problem: Python not found

**Error:**
```
'python' is not recognized as an internal or external command
```

**Solutions:**
1. Install Python from [python.org](https://python.org)
2. Make sure to check "Add Python to PATH" during installation
3. Restart terminal after installation
4. Try `python3` instead of `python`

### Problem: Virtual environment not activating

**Error:**
```
The term 'venv\Scripts\activate.bat' is not recognized
```

**Solutions:**
```bash
# Windows - try PowerShell as Administrator
venv\Scripts\Activate.ps1

# If that doesn't work, try Command Prompt
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

### Problem: pip install fails

**Error:**
```
ERROR: Could not find a version that satisfies the requirement
```

**Solutions:**
```bash
# Upgrade pip
pip install --upgrade pip

# Clear pip cache
pip cache purge

# Try installing with specific version
pip install --no-cache-dir -r requirements.txt

# For Windows, try:
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## API Connection Issues

### Problem: "Cannot connect to API"

**Error:**
```
Error: Cannot connect to API at http://localhost:8000
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
