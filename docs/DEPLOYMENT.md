# 🚀 Deployment Guide

## Local Development

### Prerequisites

- Python 3.9+
- PostgreSQL atau SQLite (untuk local development)
- Telegram BotFather token
- Supabase project

### Setup

1. **Clone Repository**

```bash
git clone https://github.com/yourusername/aw-production-bot.git
cd aw-production-bot
```

2. **Create Virtual Environment**

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# atau
.venv\Scripts\activate  # Windows
```

3. **Install Dependencies**

```bash
pip install -e ".[dev]"
# atau menggunakan requirements.txt (legacy)
pip install -r requirements.txt
```

4. **Setup Environment**

```bash
cp .env.example .env
# Edit .env dengan credentials Anda
nano .env
```

5. **Run Bot Locally**

```bash
python app.py
```

Bot akan berjalan di `http://localhost:7860`

### Run Tests Locally

```bash
pytest tests/
pytest tests/ --cov=. --cov-report=html
open htmlcov/index.html
```

### Run Linting

```bash
black .
isort .
flake8 . --max-line-length=100
mypy .
```

---

## Docker Deployment

### Build Docker Image

```bash
docker build -t aw-production-bot:latest .
```

### Run with Docker

```bash
docker run -d \
  --name aw-bot \
  -p 7860:7860 \
  -e TELEGRAM_BOT_TOKEN="your_token" \
  -e SUPABASE_URL="your_url" \
  -e SUPABASE_KEY="your_key" \
  -e TELEGRAM_BOT_ADMIN_IDS="123456,789012" \
  -v logs:/app/logs \
  aw-production-bot:latest
```

### Docker Compose

Buat `docker-compose.yml`:

```yaml
version: "3.8"

services:
  bot:
    build: .
    ports:
      - "7860:7860"
    environment:
      TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN}
      SUPABASE_URL: ${SUPABASE_URL}
      SUPABASE_KEY: ${SUPABASE_KEY}
      TELEGRAM_BOT_ADMIN_IDS: ${TELEGRAM_BOT_ADMIN_IDS}
      ENVIRONMENT: production
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  # Optional: PostgreSQL local
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

Run:

```bash
docker-compose up -d
```

---

## Hugging Face Spaces Deployment

### Prerequisites

- Hugging Face account
- Telegram bot token

### Steps

1. **Create New Space**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose "Docker" as Space SDK
   - Set visibility to "Private" (recommended)

2. **Configure Files**

The `Dockerfile` is already configured for Hugging Face. It:

- Uses Python 3.9
- Installs all dependencies including PaddleOCR
- Exposes port 7860
- Runs Flask server on `0.0.0.0:7860`

3. **Add Secrets**

In Hugging Face Space Settings → Secrets:

```
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_BOT_ADMIN_IDS=123456,789012
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
```

4. **Deploy**

Push your code to Hugging Face:

```bash
git remote add hf https://huggingface.co/spaces/yourusername/aw-bot
git push hf main
```

Space will automatically rebuild and deploy.

5. **Setup Webhook (Optional)**

For polling instead of webhook (recommended for Spaces):

- Keep default polling in `bot/core.py`
- Bot will periodically check for new messages

For webhook:

```python
# In app.py
@app.route('/telegram/webhook/<path_secret>', methods=['POST'])
def telegram_webhook(path_secret):
    # Handle webhook
```

---

## Cloud Platform Deployments

### AWS Lambda + API Gateway

1. **Create Lambda Function**
   - Runtime: Python 3.9
   - Handler: `app.lambda_handler`

2. **Configure Webhook**
   - Create API Gateway endpoint
   - Set as Telegram webhook URL

3. **Environment Variables**
   - Set in Lambda configuration

### Google Cloud Run

1. **Build Image**

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/aw-bot
```

2. **Deploy**

```bash
gcloud run deploy aw-bot \
  --image gcr.io/PROJECT_ID/aw-bot \
  --platform managed \
  --region asia-southeast1 \
  --set-env-vars TELEGRAM_BOT_TOKEN=token
```

### Railway

1. **Connect Repository**
   - Go to railway.app
   - Connect GitHub repo

2. **Add Environment Variables**
   - TELEGRAM_BOT_TOKEN
   - SUPABASE_URL
   - etc.

3. **Deploy**
   - Railway automatically deploys on push

---

## Database Setup

### Supabase Setup

1. **Create Project**
   - Go to supabase.com
   - Create new project

2. **Create Tables**

Run SQL queries in Supabase:

```sql
-- Master Barang
CREATE TABLE master_barang (
  id BIGINT PRIMARY KEY DEFAULT 1,
  nama TEXT NOT NULL,
  harga_satuan INT NOT NULL,
  satuan TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Master Metode
CREATE TABLE master_metode (
  id BIGINT PRIMARY KEY DEFAULT 1,
  nama TEXT NOT NULL,
  keyword TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Transaksi
CREATE TABLE transaksi (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tanggal DATE,
  nama TEXT,
  barang TEXT,
  jumlah INT,
  harga INT,
  total INT,
  status TEXT,
  metode TEXT,
  tagihan INT DEFAULT 0,
  uang_masuk INT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Histori Pelunasan
CREATE TABLE histori_pelunasan (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tanggal_bayar DATE,
  nama_pelanggan TEXT,
  nominal_bayar INT,
  sisa_setelah INT,
  catatan TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

3. **Enable Row Level Security (Optional)**

For production, implement RLS policies.

### PostgreSQL Local Setup

```bash
# Start PostgreSQL (if using Docker)
docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:15

# Create database
psql -U postgres -c "CREATE DATABASE aw_production;"

# Connect and run migrations
psql -U postgres -d aw_production -f migrations/init.sql
```

---

## Monitoring

### Logs

View logs:

```bash
# Docker
docker logs -f aw-bot

# Local
tail -f logs/bot.log
```

### Health Check

```bash
curl http://localhost:7860/health
```

Response:

```json
{
  "status": "ok",
  "bot_connected": true,
  "db_connected": true
}
```

---

## Scaling

### Horizontal Scaling

For multiple bot instances:

1. Use external cache (Redis) instead of in-memory
2. Use shared database (Supabase)
3. Load balance with Nginx/HAProxy

### Performance Optimization

1. **Enable Caching**
   - Set `CACHE_TTL_SECONDS=3600`

2. **Database Optimization**
   - Add indexes on frequently queried columns
   - Use pagination

3. **OCR Optimization**
   - Cache OCR results
   - Consider async OCR processing

---

## Troubleshooting

### Bot not responding

Check:

1. Bot token is correct
2. Bot is running: `curl http://localhost:7860/health`
3. Telegram can reach webhook URL
4. Firewall allows port 7860

### Database connection fails

Check:

1. SUPABASE_URL and SUPABASE_KEY are correct
2. Internet connection
3. Database is up
4. View logs: `tail -f logs/bot.log`

### OCR takes too long

Solution:

1. Increase `OCR_CONFIDENCE_THRESHOLD` to skip low-quality images
2. Reduce `OCR_LANGUAGE` to specific languages needed
3. Use smaller image sizes
4. For `mistralocr`, tune `OCR_MISTRAL_MAX_DIM` and `OCR_MISTRAL_JPEG_QUALITY` to reduce upload latency
5. Enable repeated-image speedups with `OCR_RESULT_CACHE_TTL_SECONDS` and `OCR_RESULT_CACHE_MAX_ITEMS`
6. For local OCR, tune `OCR_RUNTIME_MAX_DIM`, `OCR_RUNTIME_JPEG_QUALITY`, and `OCR_RUNTIME_PNG_COMPRESSION`

Recommended starting values:

```env
OCR_ENGINE=mistralocr
OCR_MISTRAL_MAX_DIM=1800
OCR_MISTRAL_JPEG_QUALITY=82
OCR_MISTRAL_MAX_SOURCE_BYTES=1500000
OCR_RESULT_CACHE_TTL_SECONDS=3600
OCR_RESULT_CACHE_MAX_ITEMS=64
```

---

## Zero Downtime Deployment

Using Docker and process manager:

```bash
# 1. Build new image
docker build -t aw-bot:v2 .

# 2. Start new container on different port
docker run -d -p 7861:7860 aw-bot:v2

# 3. Health check new container
curl http://localhost:7861/health

# 4. Update load balancer to point to new port
# 5. Stop old container
docker stop aw-bot

# 6. Rename
docker rename aw-bot-v2 aw-bot
```

Or use orchestration (Kubernetes):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aw-bot
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: aw-bot
  template:
    metadata:
      labels:
        app: aw-bot
    spec:
      containers:
        - name: aw-bot
          image: aw-bot:latest
          ports:
            - containerPort: 7860
          env:
            - name: TELEGRAM_BOT_TOKEN
              valueFrom:
                secretKeyRef:
                  name: bot-secrets
                  key: token
          livenessProbe:
            httpGet:
              path: /health
              port: 7860
            initialDelaySeconds: 10
            periodSeconds: 30
```

---

## Backup & Recovery

### Database Backup

```bash
# Supabase: Use built-in backup feature in console

# PostgreSQL:
pg_dump -U postgres aw_production > backup.sql

# Restore:
psql -U postgres aw_production < backup.sql
```

### Code Backup

```bash
# Git is your backup
git push origin main
```

---

## Security Checklist

- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS for webhook URL
- [ ] Implement rate limiting
- [ ] Validate all user inputs
- [ ] Use strong database passwords
- [ ] Enable database backups
- [ ] Monitor logs for errors
- [ ] Update dependencies regularly
- [ ] Use private Docker registry
- [ ] Enable Telegram bot privacy mode
