# 🚀 Deployment Guide

Ready to share your RAG assistant with others? This guide shows how.

---

## 📊 Deployment Options

| Option | Cost | Ease | Best For |
|--------|------|------|----------|
| **Local Machine** | $0 | ⭐⭐ (Easyest) | Development, testing |
| **Render** | ~$7/mo | ⭐⭐⭐ (Easy) | Small teams |
| **Railway** | ~$5/mo | ⭐⭐⭐ (Easy) | Hobby projects |
| **AWS EC2** | $5-20/mo | ⭐⭐⭐⭐ (Harder) | Scale |
| **Docker** | Varies | ⭐⭐⭐⭐ (Hard) | Professional |

---

## 🏠 Option 1: Local Machine (Best for Learning)

Already done! You're running it locally.

To keep it running:
- Don't close the terminals
- Keep your computer on
- Use ngrok to share (see below)

**To share with others:**

1. Get your public IP:
   - Go to https://whatismyipaddress.com
   - Copy the IPv4 address

2. Share link: `http://[YOUR_IP]:8501`
   - Ensure port 8501 is open
   - Others on your network can access it

---

## ☁️ Option 2: Render.com (Easiest Cloud)

Render is hands-down the easiest way to deploy.

### Step 1: Push to GitHub

First, upload your code to GitHub:

```bash
# Initialize git
git init
git add .
git commit -m "Hospital RAG Assistant"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/Hospital-RAG-Assistant.git
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to **[render.com](https://render.com)**
2. Sign up (use GitHub for easy 1-click signup)
3. Click **"New"** → **"Web Service"**
4. **Connect your GitHub repo**
5. Choose your Hospital-RAG-Assistant repo
6. **Configure:**
   - Name: `hospital-rag-assistant`
   - Environment: `Python 3.11`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
   - Region: `Ohio` or closest to you
   - Plan: `Free` (if available) or `Starter` ($7/month)

7. **Add Environment Variables:**
   - Click **"Advanced"**
   - Add these:
     ```
     SUPABASE_URL=your_supabase_url
     SUPABASE_KEY=your_supabase_key
     GROQ_API_KEY=your_groq_key
     API_BASE_URL=https://hospital-rag-xxx.onrender.com
     ```

8. **Deploy!** (Wait 5-10 minutes)

Your app will be at: `https://hospital-rag-xxx.onrender.com`

---

### For Streamlit UI on Render:

Create a second service:

1. **New** → **Web Service**
2. Same repo, but:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app_ui.py --server.port 8501`
   - Add same environment variables

---

## 🚂 Option 3: Railway.app (Even Easier)

Railway is super beginner-friendly:

1. Go to **[railway.app](https://railway.app)**
2. Click **"Start a New Project"**
3. **"Deploy from GitHub"**
4. **Authorize GitHub**
5. Select your Hospital-RAG-Assistant repo
6. **Add variables:**
   - Right panel → "Add Variables"
   - Add all your `.env` variables
7. **Deploy!**

Done! Railway handles everything.

Cost: ~$5/month for hobby projects

---

## 🐳 Option 4: Docker (Advanced)

For professional deployments:

```dockerfile
# Dockerfile (already in project)
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

Deploy with:
```bash
# Build
docker build -t hospital-rag .

# Run locally
docker run -p 8000:8000 --env-file .env hospital-rag

# Push to Docker Hub
docker push your_username/hospital-rag
```

Then deploy to AWS ECS, Google Cloud Run, etc.

---

## 🔒 Production Checklist

Before going live, verify:

- [ ] `.env` file is on server (not in git)
- [ ] API keys are secret/protected
- [ ] Database has backups enabled
- [ ] HTTPS is enabled (SSL certificate)
- [ ] Rate limiting is configured
- [ ] Error logging is working
- [ ] Monitoring is set up
- [ ] You have a way to restart if it crashes
- [ ] Supabase free tier limits are OK for your usage
- [ ] API keys are not exposed in logs

---

## 📈 Monitoring Your Deployment

### Check if it's running:

```bash
# For Render/Railway
# Check their dashboard

# For local:
curl http://localhost:8000/

# Should return:
# {"status":"healthy","message":"..."}
```

### View logs:

- **Render**: In dashboard, click "Logs"
- **Railway**: In dashboard, click "Deployment"
- **Local**: Check terminal output

### Common issues:

| Issue | Fix |
|-------|-----|
| Service not starting | Check logs for errors |
| Slow response | Upgrade to paid plan or optimize code |
| API key errors | Verify .env variables in dashboard |
| Database connection down | Check Supabase status |

---

## 💾 Securing Your Deployment

**Protect your API:**

```python
# Add in main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["yourdomain.com"],  # Block others
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Add authentication (optional):**

```python
from fastapi import HTTPException, Depends

def verify_key(api_key: str = Header(...)):
    if api_key != os.getenv("API_SECRET"):
        raise HTTPException(status_code=401, detail="Invalid key")
    return api_key
```

---

## 🎯 Sharing with Colleagues

Once deployed, share:

```
Here's our Hospital RAG Assistant:
https://hospital-rag-assistant.onrender.com

Upload a hospital PDF and ask questions!

(If deployed locally)
Share via your IP: http://192.168.1.100:8501
Or use ngrok: https://hospital-rag-xyz.ngrok.io
```

---

## 📊 Scaling Tips

As you grow:

1. **Enable Supabase backups** (free tier limited)
2. **Add database indexing** for faster queries
3. **Cache embeddings** to reduce computation
4. **Use CDN** for static files
5. **Load balance** multiple instances
6. **Monitor API usage** to stay in free tier

---

## 🚨 Disaster Recovery

If something breaks:

1. **Stop the service** (stop receiving traffic)
2. **Check logs** for error message
3. **Test locally** to reproduce
4. **Fix and redeploy**
5. **Monitor for stability**

If database is corrupted:
- Restore from backup
- Re-upload documents
- Start fresh

---

## 📞 Getting Help

- **Render Issues**: [render.com/support](https://render.com/support)
- **Railway Issues**: [railway.app/support](https://railway.app/support)
- **Supabase Issues**: [supabase.com/support](https://supabase.com/support)
- **Groq Issues**: Check console.groq.com

---

## ✅ Summary

| Method | Time | Cost | Best For |
|--------|------|------|----------|
| Local | Done ✅ | $0 | Learning |
| Railway | 10 min | $5/mo | Small projects |
| Render | 10 min | $7/mo | Teams |
| Docker | 30 min | Varies | Production |

**Recommendation:** Start with Railway or Render (easiest!)
Name: hospital-rag-assistant
Environment: Python 3.11
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port 8000
```

### Step 3: Add Environment Variables

In Render dashboard:
1. Go to your service → "Environment" tab
2. Add the following variables:

```
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-anon-key
OPENAI_API_KEY=your-openai-key
GROQ_API_KEY=your-groq-key
LLM_PROVIDER=groq
```

### Step 4: Deploy Streamlit Frontend (Optional)

For Streamlit UI, create a separate web service:

1. New Web Service (same repository)
2. Configure:

```
Name: hospital-rag-ui
Environment: Python 3.11
Build Command: pip install -r requirements.txt
Start Command: streamlit run app_ui.py --server.port=8501
```

3. Add Environment Variables:
```
API_BASE_URL=https://your-api-service.onrender.com
```

### Render Deployment Tips
- Free tier available (limited resources)
- SSL/HTTPS included automatically
- Auto-deploys on git push
- Suitable for small to medium scale

---

## Heroku Deployment

### Prerequisites
- Heroku account (credit card required, free tier paused)
- Heroku CLI installed

### Step 1: Create Procfile

Create `Procfile` in project root:

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Step 2: Create runtime.txt

Create `runtime.txt`:

```
python-3.11.7
```

### Step 3: Deploy

```bash
# 1. Login to Heroku
heroku login

# 2. Create Heroku app
heroku create hospital-rag-assistant

# 3. Set environment variables
heroku config:set SUPABASE_URL=your-supabase-url
heroku config:set SUPABASE_KEY=your-supabase-key
heroku config:set OPENAI_API_KEY=your-openai-key
heroku config:set GROQ_API_KEY=your-groq-key
heroku config:set LLM_PROVIDER=groq

# 4. Deploy
git push heroku main

# 5. Check logs
heroku logs --tail
```

---

## AWS EC2 Deployment

### Step 1: Launch EC2 Instance

1. Go to AWS EC2 Console
2. Launch instance (Ubuntu 22.04 LTS recommended)
3. Configure:
   - Instance type: t3.micro (free tier eligible)
   - Security Group: Allow HTTP (80), HTTPS (443), SSH (22)

### Step 2: Connect and Setup

```bash
# SSH into instance
ssh -i "your-key.pem" ubuntu@your-ec2-public-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3-pip python3-venv git

# Clone repository
git clone https://github.com/your-username/hospital-rag.git
cd hospital-rag

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
# Create .env file
nano .env

# Add your configuration:
# SUPABASE_URL=...
# SUPABASE_KEY=...
# OPENAI_API_KEY=...
# etc.

# Press Ctrl+O, Enter, Ctrl+X to save
```

### Step 4: Setup Gunicorn (Production WSGI Server)

```bash
# Add gunicorn to requirements.txt or install separately
pip install gunicorn

# Test run
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

### Step 5: Setup Systemd Service

```bash
# Create service file
sudo nano /etc/systemd/system/hospital-rag.service

# Add:
[Unit]
Description=Hospital RAG Assistant
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/hospital-rag
ExecStart=/home/ubuntu/hospital-rag/venv/bin/gunicorn -w 4 -b 0.0.0.0:8000 main:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable hospital-rag
sudo systemctl start hospital-rag
sudo systemctl status hospital-rag
```

### Step 6: Setup Nginx Reverse Proxy

```bash
# Install nginx
sudo apt install -y nginx

# Create config
sudo nano /etc/nginx/sites-available/hospital-rag

# Add:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/hospital-rag /etc/nginx/sites-enabled/

# Test and restart
sudo nginx -t
sudo systemctl restart nginx
```

### Step 7: Setup SSL (HTTPS)

```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renew
sudo systemctl enable certbot.timer
```

---

## Production Checklist

### Security
- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure CORS properly (not allow *)
- [ ] Set database RLS policies
- [ ] Use strong API keys
- [ ] Enable authentication for API endpoints
- [ ] Hide error stack traces from users
- [ ] Implement rate limiting

### Performance
- [ ] Setup caching (Redis)
- [ ] Use connection pooling for database
- [ ] Optimize embeddings batch size
- [ ] Monitor API response times
- [ ] Setup CDN for static files
- [ ] Enable database query optimization

### Monitoring & Logging
- [ ] Setup error tracking (Sentry)
- [ ] Configure logging to file/cloud
- [ ] Monitor API usage and costs
- [ ] Setup alerts for failures
- [ ] Track database performance
- [ ] Monitor LLM API usage

### Maintenance
- [ ] Regular database backups
- [ ] Monitor Supabase storage
- [ ] Track API key usage
- [ ] Update dependencies regularly
- [ ] Monitor server resources
- [ ] Plan for scaling

### Testing
- [ ] Run test_api.py in production
- [ ] Test with multiple concurrent users
- [ ] Test with large PDF documents
- [ ] Verify error handling
- [ ] Test rate limiting

---

## Environment-Specific Configuration

### Development (.env)
```
DEBUG=true
LLM_PROVIDER=groq
TOP_K_CHUNKS=4
CHUNK_SIZE=500
```

### Staging (.env.staging)
```
DEBUG=false
LLM_PROVIDER=groq
TOP_K_CHUNKS=4
CHUNK_SIZE=500
```

### Production (.env.production)
```
DEBUG=false
LLM_PROVIDER=openai
TOP_K_CHUNKS=5
CHUNK_SIZE=600
```

---

## Cost Estimation

### Monthly Costs (Approximate)

**Render Free Tier:**
- API Backend: Free (limited)
- Supabase: Free tier (500 MB storage)
- OpenAI Embeddings: ~$1-5 per 1M tokens

**Render Paid:**
- $7/month per service
- Supabase Pro: $25/month
- OpenAI: $0.02 per 1k tokens (embeddings)

**AWS EC2:**
- t3.micro: Free (first year)
- RDS/Database: $15-50/month
- Data transfer: ~$0.12/GB
- OpenAI: Pay per usage

**Groq (Recommended for Cost):**
- Free up to limits
- Much cheaper than OpenAI

---

## Troubleshooting

### API Connection Issues
```bash
# Test API from server
curl http://localhost:8000/

# Check service status
sudo systemctl status hospital-rag

# View logs
sudo journalctl -u hospital-rag -f
```

### Database Connection Issues
```bash
# Test Supabase connection
python -c "import config; from supabase_db import get_supabase_manager; print(get_supabase_manager())"
```

### High Memory Usage
```bash
# Reduce Gunicorn workers
gunicorn -w 2 -b 0.0.0.0:8000 main:app

# Monitor memory
free -h
```

---

## Recommended Architecture for Production

```
┌─────────────────────────────────────────┐
│        CloudFlare / Nginx Reverse       │
│             Proxy + Cache               │
└────────────┬────────────────────────────┘
             │
    ┌────────┴────────┐
    ▼                 ▼
┌─────────────┐  ┌─────────────┐
│  API Server │  │ API Server  │ (Load balanced)
│  (Gunicorn) │  │ (Gunicorn)  │
└────────┬────┘  └────────┬────┘
         │                │
         └────────┬───────┘
                  ▼
         ┌─────────────────┐
         │  Supabase       │ (PostgreSQL + pgvector)
         │  (Managed DB)   │
         └─────────────────┘
         
         ┌─────────────────┐
         │  Redis Cache    │ (Optional)
         │  (Session/Query)│
         └─────────────────┘

         ┌─────────────────┐
         │  OpenAI/Groq    │ (External APIs)
         │  (LLM + Embed)  │
         └─────────────────┘
```

---

**Last Updated**: 2024
**Version**: 1.0
