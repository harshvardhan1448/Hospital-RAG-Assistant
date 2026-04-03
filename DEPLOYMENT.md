# Hospital RAG Assistant - Deployment Guide

This guide covers deploying the Hospital RAG Assistant to production environments.

## Table of Contents
1. [Local Deployment (Development)](#local-deployment-development)
2. [Render Deployment (Recommended)](#render-deployment-recommended)
3. [Heroku Deployment](#heroku-deployment)
4. [AWS EC2 Deployment](#aws-ec2-deployment)
5. [Production Checklist](#production-checklist)

---

## Local Deployment (Development)

### Prerequisites
- Python 3.9+
- Supabase account (free tier)
- OpenAI API key
- Groq API key (optional but recommended)

### Setup Steps

```bash
# 1. Clone repository or navigate to project
cd NexovAi

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate.bat

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 5. Run Supabase setup SQL
# Copy content from supabase_setup.sql
# Paste into Supabase SQL Editor at https://supabase.com/dashboard

# 6. Start FastAPI backend
python main.py
# Runs on http://localhost:8000

# 7. In another terminal, start Streamlit UI
streamlit run app_ui.py
# Runs on http://localhost:8501
```

---

## Render Deployment (Recommended)

Render is ideal for hosting this application with minimal configuration.

### Step 1: Prepare Repository

```bash
# 1. Initialize git repository (if not already)
git init
git add .
git commit -m "Initial Hospital RAG Assistant commit"

# 2. Create GitHub repository
# Push to GitHub (Render uses GitHub for deployment)
git remote add origin https://github.com/your-username/hospital-rag.git
git push -u origin main
```

### Step 2: Create Render Service

1. Go to [render.com](https://render.com)
2. Sign up/login with GitHub
3. Click "New +" → "Web Service"
4. Select your GitHub repository
5. Configure as follows:

```
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
