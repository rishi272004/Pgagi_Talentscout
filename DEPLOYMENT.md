# Deployment & Cloud Guide

## 🚀 Deployment Options

### Option 1: Local Development (Recommended for Testing)

#### Requirements
- Python 3.8+
- Ollama or OpenAI API key
- Git

#### Steps
```bash
# 1. Clone/navigate to project
cd talentscout-hiring-assistant

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
# Create .env with LLM_PROVIDER and OLLAMA_MODEL or OPENAI_API_KEY

# 5. Start Ollama (if using Ollama)
ollama serve

# 6. In new terminal, run Streamlit
streamlit run app.py

# 7. Access at http://localhost:8501
```

---

### Option 2: Streamlit Cloud (Easiest & Recommended)

#### Prerequisites
- GitHub account
- Project pushed to public GitHub repository
- Streamlit Cloud account (free)

#### Deployment Steps

1. **Push to GitHub**
```bash
git remote add origin https://github.com/your-username/talentscout-hiring-assistant.git
git branch -M main
git push -u origin main
```

2. **Sign Up for Streamlit Cloud**
- Visit: https://streamlit.io/cloud
- Click "Sign up with GitHub"
- Authorize Streamlit

3. **Deploy Application**
- Click "New app"
- Select your repository
- Select branch: `main`
- Set file path: `app.py`
- Click "Deploy"

4. **Configure Secrets**
```bash
# On Streamlit Cloud dashboard
Settings → Secrets → Add
```

Add to secrets (`~/.streamlit/secrets.toml`):
```toml
OPENAI_API_KEY = "sk-your-key"
LLM_PROVIDER = "openai"  # or "ollama"
OLLAMA_MODEL = "mistral"
```

5. **Get Live URL**
- Your app is now live at: `https://your-username-talentscout.streamlit.app`

#### Streamlit Cloud Limitations
- Ollama may not work (no local server access)
- Use OpenAI API for best results
- Free tier has resource limits
- Sleeps after 1 hour of inactivity

---

### Option 3: AWS EC2 Deployment

#### Prerequisites
- AWS account (free tier eligible)
- EC2 instance (Ubuntu 20.04 or later)
- SSH access to instance

#### Setup Instructions

1. **Launch EC2 Instance**
```bash
# In AWS Console:
# - Select Ubuntu 20.04 LTS AMI
# - Instance type: t2.micro (free tier)
# - Configure security group:
#   - Allow SSH (22)
#   - Allow HTTP (80)
#   - Allow HTTPS (443)
#   - Allow Streamlit (8501)
```

2. **Connect to Instance**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Install Dependencies**
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install python3-pip python3-venv git -y

# Install Ollama (optional)
curl https://ollama.ai/install.sh | sh
```

4. **Clone Repository**
```bash
git clone https://github.com/your-username/talentscout-hiring-assistant.git
cd talentscout-hiring-assistant
```

5. **Setup Python Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. **Configure Environment**
```bash
nano .env
# Add your LLM_PROVIDER and API keys
```

7. **Run Ollama (if using)**
```bash
# In background
nohup ollama serve > ollama.log 2>&1 &
ollama pull mistral  # Pull model
```

8. **Run Streamlit**
```bash
# In background with nohup
nohup streamlit run app.py --server.port 8501 > streamlit.log 2>&1 &

# Or use systemd service (recommended)
```

9. **Create Systemd Service (For Auto-Restart)**
```bash
sudo nano /etc/systemd/system/talentscout.service
```

Add:
```ini
[Unit]
Description=TalentScout Hiring Assistant
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/talentscout-hiring-assistant
Environment="PATH=/home/ubuntu/talentscout-hiring-assistant/venv/bin"
ExecStart=/home/ubuntu/talentscout-hiring-assistant/venv/bin/streamlit run app.py --server.port 8501

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable talentscout
sudo systemctl start talentscout
sudo systemctl status talentscout
```

10. **Setup Reverse Proxy (Nginx)**
```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/default
```

Configure:
```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable:
```bash
sudo systemctl restart nginx
```

11. **Access Your Application**
- Visit: `http://your-ec2-ip:8501`
- Or: `http://your-domain.com` (if domain configured)

---

### Option 4: Docker Deployment

#### Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8501

# Set Streamlit config
RUN mkdir -p ~/.streamlit && \
    echo "[server]" > ~/.streamlit/config.toml && \
    echo "headless = true" >> ~/.streamlit/config.toml && \
    echo "port = 8501" >> ~/.streamlit/config.toml && \
    echo "enableCORS = false" >> ~/.streamlit/config.toml

# Run Streamlit
CMD ["streamlit", "run", "app.py"]
```

#### Build and Run
```bash
# Build image
docker build -t talentscout:latest .

# Run container
docker run -p 8501:8501 \
  -e LLM_PROVIDER=openai \
  -e OPENAI_API_KEY=your_key \
  talentscout:latest

# Or with volume mount for data persistence
docker run -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -e LLM_PROVIDER=openai \
  -e OPENAI_API_KEY=your_key \
  talentscout:latest
```

#### Docker Compose (Multiple Services)
```yaml
version: '3.8'

services:
  talentscout:
    build: .
    ports:
      - "8501:8501"
    environment:
      LLM_PROVIDER: openai
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data
    depends_on:
      - ollama

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama:/root/.ollama
    command: serve

volumes:
  ollama:
```

Run with:
```bash
docker-compose up
```

---

### Option 5: Google Cloud Platform (GCP)

#### Cloud Run Deployment

1. **Set Up GCP Project**
```bash
gcloud init
gcloud config set project your-project-id
```

2. **Create app.yaml**
```yaml
runtime: python39
entrypoint: streamlit run app.py --server.port=$PORT
```

3. **Deploy**
```bash
gcloud run deploy talentscout \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars LLM_PROVIDER=openai,OPENAI_API_KEY=your_key
```

---

## 🔧 Environment Variables

### For OpenAI
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
```

### For Ollama
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=mistral
OLLAMA_BASE_URL=http://localhost:11434
```

### For Streamlit Cloud Secrets
Go to App → Settings → Secrets and add:
```toml
OPENAI_API_KEY = "sk-xxxxx"
LLM_PROVIDER = "openai"
```

---

## 📊 Performance & Monitoring

### Monitor Logs
```bash
# Systemd service
sudo journalctl -u talentscout -f

# Docker container
docker logs -f container_id
```

### Check Resource Usage
```bash
# EC2 instance CPU/Memory
top
free -h
df -h
```

---

## 🔐 Security Checklist

- [ ] Enable HTTPS/SSL (Certbot)
- [ ] Set strong database passwords
- [ ] Configure firewall rules
- [ ] Enable AWS security groups
- [ ] Rotate API keys regularly
- [ ] Use environment variables for secrets
- [ ] Enable audit logging
- [ ] Regular security updates

---

## 📈 Scaling Considerations

### Horizontal Scaling
- Use load balancer (AWS ELB, Nginx)
- Multiple EC2 instances
- Docker Swarm or Kubernetes

### Vertical Scaling
- Increase instance size
- Add more RAM
- Upgrade to faster CPU

### Database Scaling
- Migrate from JSON to database
- Use connection pooling
- Implement caching (Redis)

---

## 💰 Cost Estimation

### AWS EC2 (t2.micro - Free Tier)
- **Free tier**: 750 hours/month for 12 months
- **After**: ~$0.01/hour = ~$7/month
- **Storage**: Free tier 30GB EBS

### OpenAI API
- **GPT-3.5**: ~$0.0015 per 1K tokens
- **Typical interview**: ~2000 tokens = ~$0.003 per interview
- **100 interviews**: ~$0.30

### Streamlit Cloud
- **Free tier**: Available
- **Pro**: $5-30/month

### GCP Cloud Run
- **Free tier**: 2 million requests/month
- **Typical interview**: 10-15 requests = Free for ~130k interviews

---

## 🚀 Demo URL Examples

After deployment, your application will be available at:

- **Local**: http://localhost:8501
- **Streamlit Cloud**: https://your-username-talentscout.streamlit.app
- **AWS EC2**: http://your-ec2-ip:8501
- **AWS with Domain**: https://talentscout.yourdomain.com
- **GCP Cloud Run**: https://talentscout-xxxxx.run.app

---

## 📝 Post-Deployment Checklist

- [ ] Test full interview flow
- [ ] Verify data storage
- [ ] Check sentiment analysis
- [ ] Test language detection
- [ ] Verify download functionality
- [ ] Monitor performance
- [ ] Check error handling
- [ ] Test on mobile
- [ ] Verify GDPR compliance
- [ ] Create backup strategy

---

**Version**: 1.0.0  
**Last Updated**: January 2026
