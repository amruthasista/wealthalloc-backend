# WealthAlloc Backend - Setup Guide

This guide will help you set up the WealthAlloc backend for development or production deployment.

## Prerequisites

### Required Software
- Python 3.10 or higher
- PostgreSQL 14 or higher
- Redis 7.0 or higher
- Docker & Docker Compose (for containerized deployment)
- Kubernetes cluster (for production deployment)

### IBKR Requirements
- Interactive Brokers account
- IB Gateway or TWS installed and running
- API access enabled in your IBKR account settings

## Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/wealthalloc-backend.git
cd wealthalloc-backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

#### PostgreSQL

```bash
# Create database
createdb wealthalloc

# Run schema
psql -d wealthalloc -f database/schema.sql
```

#### Redis

```bash
# Start Redis (if not running)
redis-server
```

### 5. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env
```

Required environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `IBKR_HOST`: IBKR Gateway host (default: 127.0.0.1)
- `IBKR_PORT`: IBKR Gateway port (default: 7497 for paper, 7496 for live)
- `IBKR_CLIENT_ID`: Client ID for IBKR connection
- `SECRET_KEY`: JWT secret key (generate with `openssl rand -hex 32`)

### 6. IBKR Gateway Setup

#### Start IB Gateway

```bash
# Download and install IB Gateway from:
# https://www.interactivebrokers.com/en/trading/ibgateway-stable.php

# Configure Gateway:
# - Enable API connections
# - Set port to 7497 (paper trading) or 7496 (live)
# - Add localhost to trusted IPs
```

#### Test Connection

```bash
python -c "
from services.ibkr_client import IBKRClient
import asyncio

async def test():
    client = IBKRClient(host='127.0.0.1', port=7497, client_id=1)
    await client.connect()
    print('✓ Connected to IBKR Gateway')

asyncio.run(test())
"
```

### 7. Run Development Server

```bash
python main.py
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/api/docs
- Health: http://localhost:8000/health

### 8. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_api.py -v
```

## Docker Setup

### Build Image

```bash
docker build -t wealthalloc/api:latest .
```

### Run with Docker Compose

```bash
# Create docker-compose.yml (see example below)
docker-compose up -d
```

Example `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    image: wealthalloc/api:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/wealthalloc
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:14
    environment:
      POSTGRES_DB: wealthalloc
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## Production Deployment

### Kubernetes

1. **Configure Secrets**

```bash
# Create secrets
kubectl create secret generic wealthalloc-secrets \
  --from-literal=database-url=postgresql://... \
  --from-literal=secret-key=... \
  --from-literal=ibkr-username=... \
  --from-literal=ibkr-password=...
```

2. **Deploy**

```bash
./scripts/deploy.sh
```

3. **Verify**

```bash
kubectl get pods -n wealthalloc
kubectl logs -f deployment/wealthalloc-api -n wealthalloc
```

### Environment Variables (Production)

```bash
# Application
APP_NAME=Wealthalloc
ENVIRONMENT=production
DEBUG=False

# Security
SECRET_KEY=<generate-secure-key>
ALLOWED_ORIGINS=https://app.wealthalloc.com

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/wealthalloc
DB_POOL_SIZE=20

# IBKR (use live credentials)
IBKR_HOST=ibkr-gateway
IBKR_PORT=7496
IBKR_PAPER_TRADING=False

# Monitoring
LOG_LEVEL=INFO
ENABLE_METRICS=True
```

## Training ML Models

### LSTM Autoencoder

```bash
# Train model
python scripts/train_lstmae.py

# Model will be saved to models/lstm_autoencoder.pth
```

## Troubleshooting

### IBKR Connection Issues

**Problem**: Cannot connect to IBKR Gateway

**Solutions**:
1. Verify Gateway is running: `netstat -an | grep 7497`
2. Check API settings in Gateway configuration
3. Verify client ID is unique
4. Check firewall settings

### Database Connection Issues

**Problem**: Cannot connect to PostgreSQL

**Solutions**:
1. Verify PostgreSQL is running: `pg_isready`
2. Check DATABASE_URL format
3. Verify credentials
4. Check network connectivity

### Port Already in Use

**Problem**: Port 8000 is already in use

**Solutions**:
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
PORT=8001 python main.py
```

## Performance Tuning

### Database

```sql
-- Create indexes for better performance
CREATE INDEX CONCURRENTLY idx_holdings_portfolio_symbol 
ON holdings(portfolio_id, symbol);

CREATE INDEX CONCURRENTLY idx_trades_created_status 
ON trades(created_date DESC, status);
```

### API

- Adjust `WORKERS` environment variable based on CPU cores
- Enable Redis caching for frequently accessed data
- Use connection pooling for database

## Monitoring

### Health Checks

```bash
# API health
curl http://localhost:8000/health

# Database health
psql -d wealthalloc -c "SELECT 1"

# Redis health
redis-cli ping
```

### Logs

```bash
# View logs
tail -f logs/wealthalloc.log

# Kubernetes logs
kubectl logs -f deployment/wealthalloc-api -n wealthalloc
```

### Metrics

Access Prometheus metrics at:
```
http://localhost:8000/metrics
```

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use strong database passwords
- [ ] Enable HTTPS in production
- [ ] Configure CORS properly
- [ ] Enable rate limiting
- [ ] Rotate API keys regularly
- [ ] Use secrets management (e.g., HashiCorp Vault)
- [ ] Enable database encryption
- [ ] Set up API authentication
- [ ] Configure network policies

## Next Steps

1. Review [API Documentation](API.md)
2. Read [Architecture Overview](ARCHITECTURE.md)
3. Set up monitoring and alerting
4. Configure backup procedures
5. Plan disaster recovery

## Support

For issues or questions:
- GitHub Issues: https://github.com/yourusername/wealthalloc-backend/issues
- Email: support@wealthalloc.com
