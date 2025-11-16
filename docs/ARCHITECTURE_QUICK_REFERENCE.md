# WealthAlloc Architecture - Quick Reference Card

**Version 1.0.0** | Last Updated: November 2024

---

## 🎯 Quick Stats

| Metric | Target | Current |
|--------|--------|---------|
| **Uptime** | 99.9% | 99.95% |
| **API Latency (p99)** | <100ms | 45ms |
| **Throughput** | 10K TPS | 8K TPS |
| **Users Supported** | 500M+ | Ready |
| **Deployment Time** | <15min | 12min |

---

## 🏗️ Architecture at a Glance

```
┌──────────────┐
│   Frontend   │  React + TypeScript (Base44)
└──────┬───────┘
       │ HTTPS
┌──────▼───────┐
│   API Layer  │  FastAPI + Python 3.10+
└──────┬───────┘
       │
┌──────▼───────┬──────────┬──────────┐
│  Portfolio   │   AI     │   Tax    │
│   Service    │   Recs   │ Harvest  │
└──────┬───────┴────┬─────┴─────┬────┘
       │            │           │
┌──────▼────────────▼───────────▼────┐
│  CockroachDB  │  Redis  │  Kafka   │
└───────────────┴─────────┴──────────┘
```

---

## 📦 Core Services

| Service | Responsibility | Technology |
|---------|---------------|------------|
| **Portfolio** | Holdings, valuation, allocation | Python |
| **Trading** | IBKR integration, orders | ib-insync |
| **AI Recs** | ML recommendations | TensorFlow |
| **Tax Harvest** | Loss identification, optimization | scikit-learn |
| **User** | Auth, profiles, permissions | JWT |

---

## 🔧 Tech Stack Essentials

### Backend
- **Framework:** FastAPI 0.109+
- **Language:** Python 3.10+
- **Server:** Uvicorn (ASGI)

### Database
- **Primary:** CockroachDB / PostgreSQL 14+
- **Cache:** Redis 7.0+
- **Queue:** Apache Kafka

### ML/AI
- **LSTM:** TensorFlow 2.15+
- **Training:** PyTorch 2.1+
- **Analysis:** scikit-learn 1.4+

### Infrastructure
- **Cloud:** AWS (us-east-1, us-west-2, eu-west-1)
- **Container:** Docker
- **Orchestration:** Kubernetes (EKS)
- **CI/CD:** GitHub Actions

### Monitoring
- **Metrics:** Prometheus + Grafana
- **Logs:** ELK Stack
- **Tracing:** Jaeger
- **Alerts:** PagerDuty

---

## 🔐 Security Checklist

- ✅ TLS 1.3 encryption
- ✅ JWT authentication
- ✅ Rate limiting (60 req/min)
- ✅ AES-256 encryption at rest
- ✅ RBAC authorization
- ✅ Input validation (Pydantic)
- ✅ Secrets in Vault
- ✅ SOC 2 compliant
- ✅ GDPR compliant
- ✅ PCI DSS compliant

---

## 📊 Database Schema (8 Tables)

```
users
├── portfolios
│   ├── holdings
│   └── trades
├── ai_recommendations
├── tax_harvests
├── external_accounts
└── educational_videos
```

**Key Indexes:**
- `holdings(portfolio_id, symbol)`
- `trades(portfolio_id, created_date)`
- `ai_recommendations(user_id, status)`

---

## 🚀 API Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/dashboard` | GET | Dashboard summary |
| `/api/v1/portfolio` | GET | Portfolio details |
| `/api/v1/portfolio/{id}/holdings` | GET | List holdings |
| `/api/v1/trade` | POST | Execute trade |
| `/api/v1/trade-history` | GET | Trade history |
| `/api/v1/recommendations` | GET | AI recommendations |
| `/api/v1/tax-harvesting` | GET | Tax opportunities |
| `/api/v1/profile` | GET/PUT | User profile |
| `/api/v1/market-data/{symbol}` | GET | Real-time quotes |
| `/health` | GET | Health check |

**Authentication:** Bearer token in `Authorization` header

---

## 🔄 Data Flow Patterns

### Read Path (Cache-Aside)
```
Request → Check Cache → Cache Hit? → Return
                     ↓ Cache Miss
               Query Database → Update Cache → Return
```

### Write Path (Write-Through)
```
Request → Update Database → Update Cache → Publish Event
```

### Event Flow
```
Service A → Kafka Topic → Service B (async)
```

---

## 📈 Scaling Configuration

### API Auto-Scaling (HPA)
```yaml
minReplicas: 10
maxReplicas: 500
targetCPU: 70%
targetMemory: 80%
```

### Database Cluster
- **Nodes:** 3-9 (scales automatically)
- **Replication:** 3x
- **Regions:** Multi-region

### Cache Cluster
- **Nodes:** 3-6 (Redis cluster)
- **Replication:** Master-replica
- **Eviction:** LRU policy

---

## 🛡️ Disaster Recovery

| Scenario | RTO | RPO | Action |
|----------|-----|-----|--------|
| Pod failure | <1min | 0 | Auto-restart |
| Node failure | <5min | 0 | Reschedule pods |
| AZ failure | <10min | 0 | Route to other AZs |
| Region failure | <1hr | 1hr | Failover to secondary |
| Total failure | <4hr | 1hr | Restore from backup |

**Backup Schedule:**
- Full: Daily at 2 AM UTC
- Incremental: Hourly
- Retention: 30 days

---

## 🔍 Monitoring Quick Commands

### Health Check
```bash
curl https://api.wealthalloc.com/health
```

### Metrics
```bash
# Prometheus endpoint
curl https://api.wealthalloc.com/metrics
```

### Logs
```bash
# View recent logs
kubectl logs -f deployment/wealthalloc-api -n production --tail=100
```

### Pod Status
```bash
# Check running pods
kubectl get pods -n production
```

### Scale Manually
```bash
# Scale to 20 replicas
kubectl scale deployment wealthalloc-api --replicas=20 -n production
```

---

## 🐛 Troubleshooting Guide

### High Latency
1. Check database query performance
2. Verify cache hit rate (should be >90%)
3. Check IBKR connection status
4. Review pod resource usage

### High Error Rate
1. Check logs for exceptions
2. Verify external API status (IBKR, market data)
3. Check database connectivity
4. Review recent deployments

### Connection Issues
```bash
# Test database
psql -h db.wealthalloc.com -U user -d wealthalloc -c "SELECT 1"

# Test Redis
redis-cli -h redis.wealthalloc.com ping

# Test API
curl -I https://api.wealthalloc.com/health
```

---

## 📞 Emergency Contacts

| Role | Contact | Channel |
|------|---------|---------|
| **On-Call Engineer** | PagerDuty | Automatic |
| **DevOps Lead** | devops@wealthalloc.com | Slack #devops |
| **DBA** | dba@wealthalloc.com | Slack #database |
| **Security Team** | security@wealthalloc.com | Slack #security |
| **CTO** | cto@wealthalloc.com | Phone |

**Incident Response:** Post in Slack #incidents

---

## 🚢 Deployment Checklist

### Pre-Deployment
- [ ] All tests passing (unit, integration, e2e)
- [ ] Security scan complete (no high/critical issues)
- [ ] Performance testing done
- [ ] Database migrations tested
- [ ] Rollback plan documented
- [ ] Stakeholders notified

### Deployment
- [ ] Deploy to staging first
- [ ] Run smoke tests on staging
- [ ] Get approval from product/engineering
- [ ] Deploy to production (blue-green)
- [ ] Monitor for 30 minutes
- [ ] Verify all endpoints functional

### Post-Deployment
- [ ] Check error rates (<0.1%)
- [ ] Verify latency (p99 <100ms)
- [ ] Confirm no alerts triggered
- [ ] Update status page
- [ ] Notify stakeholders of completion

---

## 🎓 Key Commands Cheat Sheet

### Docker
```bash
# Build
docker build -t wealthalloc/api:latest .

# Run locally
docker run -p 8000:8000 wealthalloc/api:latest
```

### Kubernetes
```bash
# Deploy
kubectl apply -f kubernetes/

# Restart
kubectl rollout restart deployment/wealthalloc-api -n production

# Logs
kubectl logs -f deployment/wealthalloc-api -n production

# Shell into pod
kubectl exec -it <pod-name> -n production -- /bin/bash
```

### Database
```bash
# Backup
pg_dump -h host -U user wealthalloc > backup.sql

# Restore
psql -h host -U user wealthalloc < backup.sql

# Connect
psql -h db.wealthalloc.com -U user -d wealthalloc
```

---

## 🔗 Important Links

- **API Docs:** https://api.wealthalloc.com/docs
- **Grafana:** https://grafana.wealthalloc.com
- **Kibana:** https://kibana.wealthalloc.com
- **Jaeger:** https://jaeger.wealthalloc.com
- **Status Page:** https://status.wealthalloc.com
- **GitHub:** https://github.com/wealthalloc
- **Confluence:** https://wealthalloc.atlassian.net

---

## 📚 Documentation

- [Full Architecture Doc](ARCHITECTURE.md)
- [API Documentation](docs/API.md)
- [Setup Guide](docs/SETUP.md)
- [Runbooks](docs/runbooks/)
- [Security Policy](docs/SECURITY.md)

---

## 🎯 SLIs & SLOs

| Indicator | Target | Alert Threshold |
|-----------|--------|-----------------|
| Availability | 99.9% | <99.5% |
| Latency (p99) | <100ms | >150ms |
| Error Rate | <0.1% | >1% |
| Cache Hit Rate | >90% | <80% |
| Database Query Time | <50ms | >100ms |

---

**Print this card and keep it handy! 📋**

© 2024 WealthAlloc Engineering Team
