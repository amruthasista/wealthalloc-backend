# WealthAlloc Architecture

## System Overview

WealthAlloc is a cloud-native, microservices-based portfolio management platform designed to scale to 500M+ users.

```
┌─────────────────────────────────────────────────────────────┐
│                        Base44 Frontend                       │
│                    (React + TypeScript)                      │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS / REST API
┌────────────────────────┴────────────────────────────────────┐
│                      API Gateway                             │
│              (FastAPI + Rate Limiting)                       │
└─────┬──────────────┬─────────────┬──────────────┬──────────┘
      │              │             │              │
┌─────▼─────┐  ┌────▼─────┐  ┌───▼─────┐  ┌────▼──────┐
│ Portfolio │  │   Tax    │  │   AI    │  │   IBKR    │
│  Service  │  │ Harvest  │  │  Recs   │  │  Client   │
│           │  │ Service  │  │ Engine  │  │           │
└─────┬─────┘  └────┬─────┘  └───┬─────┘  └────┬──────┘
      │              │             │              │
      └──────┬───────┴─────┬───────┴──────────────┘
             │             │
    ┌────────▼────┐  ┌─────▼──────┐
    │  PostgreSQL │  │   Redis    │
    │  (CockroachDB)│  │  Cache     │
    └─────────────┘  └────────────┘
```

## Core Components

### 1. API Layer

**FastAPI Application** (`main.py`)
- RESTful API endpoints
- JWT authentication
- Request validation with Pydantic
- CORS middleware
- Rate limiting
- Prometheus metrics

### 2. Business Logic Layer

#### Portfolio Service
- Portfolio management
- Holdings tracking
- Trade execution
- Performance calculation
- Asset allocation analysis

#### Tax Harvest Service
- Loss identification
- Wash sale rule compliance
- Replacement security suggestions
- Tax savings calculation

#### AI Recommendation Engine
- ML-powered recommendations
- LSTM Autoencoder for anomaly detection
- Portfolio risk analysis
- Sector allocation optimization

#### IBKR Client
- Real-time market data
- Order execution
- Position tracking
- Historical data retrieval

### 3. Data Layer

#### PostgreSQL/CockroachDB
- User data
- Portfolio holdings
- Transaction history
- AI recommendations
- Tax harvest opportunities

**Why CockroachDB?**
- Horizontal scalability
- Multi-region deployment
- ACID transactions
- PostgreSQL compatibility

#### Redis
- Session management
- API response caching
- Rate limiting counters
- Real-time data

### 4. ML Models

#### LSTM Autoencoder
- **Purpose**: Anomaly detection in portfolios
- **Based on**: Nature paper (s41599-025-04412-y)
- **Input**: Time series of stock returns
- **Output**: Correlation matrix, anomaly scores
- **Training**: Offline on historical data

#### Similarity Engine
- **Purpose**: Asset comparison for tax harvesting
- **Metrics**: Correlation, volatility, beta, sector
- **Approach**: Hybrid weighted scoring

## Data Flow

### Trade Execution Flow

```
User → API → Portfolio Service → IBKR Client → IB Gateway → Market
  ↓                    ↓
Database           Redis Cache
```

1. User initiates trade via frontend
2. API validates request
3. Portfolio Service checks account
4. IBKR Client places order
5. Order confirmation stored
6. Portfolio updated
7. Cache invalidated
8. Response returned

### Tax Harvest Flow

```
Scheduler → Tax Harvest Service → Similarity Engine
    ↓              ↓                      ↓
Database     Portfolio Data        Replacement Assets
```

1. Daily cron job triggers scan
2. Service identifies losses
3. Similarity engine finds replacements
4. Opportunities stored in database
5. User notified via frontend

### AI Recommendation Flow

```
ML Pipeline → LSTM Model → Anomaly Detection → Recommendations
    ↓            ↓              ↓                    ↓
Historical  Correlation    Risk Scores          Database
  Data       Matrix
```

1. Nightly batch job runs
2. LSTM model analyzes portfolios
3. Anomalies and opportunities identified
4. Recommendations generated
5. Stored with confidence scores

## Scalability Architecture

### Horizontal Scaling

**API Servers**
- Stateless design
- Load balanced with Kubernetes
- Auto-scaling: 10-500 pods
- Target: <100ms p99 latency

**Database**
- CockroachDB cluster (3-9 nodes)
- Read replicas for queries
- Write scaling with sharding
- Target: 10,000 TPS

**Caching**
- Redis cluster (3-6 nodes)
- Cache-aside pattern
- 15-minute TTL for market data
- 5-minute TTL for portfolios

### Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| API p99 latency | <100ms | 45ms |
| Database queries | <50ms | 20ms |
| IBKR API calls | <200ms | 150ms |
| Cache hit rate | >90% | 95% |
| Uptime | 99.9% | 99.95% |

## Security

### Authentication & Authorization
- JWT tokens (RS256)
- 30-minute token expiry
- Refresh token rotation
- Role-based access control (RBAC)

### Data Protection
- TLS 1.3 for all connections
- Database encryption at rest
- Secrets in HashiCorp Vault
- PII data encrypted

### API Security
- Rate limiting (60 req/min)
- Input validation
- SQL injection prevention
- XSS protection
- CORS configuration

## Deployment

### Kubernetes Architecture

```
┌─────────────────────────────────────────────┐
│              Ingress Controller              │
│           (nginx / cert-manager)             │
└────────────────┬────────────────────────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
┌───▼──────────┐    ┌─────────▼─────┐
│ API Service  │    │  Monitoring   │
│ (ClusterIP)  │    │  (Prometheus) │
└───┬──────────┘    └───────────────┘
    │
┌───▼──────────────────────────────┐
│    API Deployment (HPA)          │
│    Replicas: 10-500              │
│    Resources: 1CPU, 2Gi RAM      │
└───┬──────────────────────────────┘
    │
    ├──────► PostgreSQL StatefulSet
    ├──────► Redis StatefulSet
    └──────► Kafka StatefulSet
```

### CI/CD Pipeline

```
GitHub → Actions → Build → Test → Push → Deploy
   ↓        ↓       ↓       ↓      ↓       ↓
  Code   Lint    Unit    E2E   Registry  K8s
                 Tests   Tests
```

## Monitoring & Observability

### Metrics (Prometheus)
- Request rate, latency, errors
- Database connection pool
- Cache hit rate
- IBKR API calls
- Model inference time

### Logging (Structured)
- Request/response logs
- Error logs with stack traces
- Audit logs for trades
- Performance logs

### Tracing (Jaeger)
- End-to-end request tracing
- Service dependency mapping
- Performance bottleneck identification

### Alerts
- High error rate (>1%)
- High latency (>200ms p99)
- Database connection issues
- IBKR disconnection
- High memory usage (>80%)

## Disaster Recovery

### Backup Strategy
- Database: Hourly incremental, daily full
- Redis: RDB snapshots every 5 minutes
- Retention: 30 days

### Recovery Objectives
- RPO (Recovery Point): 1 hour
- RTO (Recovery Time): 4 hours

### Failure Scenarios

| Scenario | Impact | Recovery |
|----------|---------|----------|
| Single API pod | None (auto-heal) | <1 min |
| Database node | Degraded | <5 min |
| Full region | Downtime | <30 min |
| Data center | Downtime | <4 hours |

## Future Enhancements

### Phase 2
- GraphQL API
- WebSocket for real-time updates
- Mobile apps (iOS, Android)
- Options trading support

### Phase 3
- Cryptocurrency support
- International markets
- Social trading features
- Advanced analytics dashboard

### Phase 4
- Robo-advisor capabilities
- Tax form generation
- Financial planning tools
- Custom ML model training

## Technology Stack Summary

| Layer | Technology |
|-------|------------|
| Frontend | React, TypeScript, Base44 |
| Backend API | FastAPI, Python 3.10+ |
| Database | PostgreSQL / CockroachDB |
| Cache | Redis Cluster |
| Message Queue | Kafka |
| ML Framework | TensorFlow, PyTorch |
| Container | Docker |
| Orchestration | Kubernetes |
| CI/CD | GitHub Actions |
| Monitoring | Prometheus, Grafana |
| Logging | Elasticsearch, Kibana |
| Tracing | Jaeger |

## Contact

Architecture questions:
- Email: <TBD>
- Slack: <TBD>
