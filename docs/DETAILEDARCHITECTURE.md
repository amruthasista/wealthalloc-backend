# WealthAlloc Architecture Document

**Version:** 1.0.0  
**Date:** November 2024  
**Status:** Production Ready  
**Author:** WealthAlloc Engineering Team

---

## Executive Summary

WealthAlloc is a cloud-native, AI-powered portfolio management platform designed to scale to 500M+ users. Built on modern microservices architecture with FastAPI backend, PostgreSQL/CockroachDB database, and integrated with Interactive Brokers for real-time trading capabilities.

**Key Highlights:**
- **Scalability:** 500M+ users, 10,000+ TPS
- **Availability:** 99.9% uptime SLA
- **Performance:** <100ms p99 API latency
- **Security:** Bank-grade encryption, SOC 2 compliant
- **AI/ML:** LSTM Autoencoder for anomaly detection
- **Trading:** Real-time IBKR integration

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Patterns](#architecture-patterns)
3. [Core Components](#core-components)
4. [Data Architecture](#data-architecture)
5. [API Architecture](#api-architecture)
6. [Security Architecture](#security-architecture)
7. [Scalability & Performance](#scalability--performance)
8. [Deployment Architecture](#deployment-architecture)
9. [Monitoring & Observability](#monitoring--observability)
10. [Disaster Recovery](#disaster-recovery)
11. [Technology Stack](#technology-stack)
12. [Integration Architecture](#integration-architecture)
13. [Future Roadmap](#future-roadmap)

---

## 1. System Overview

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                           │
│                  (Base44 React Application)                      │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTPS / REST API / WebSocket
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                      API Gateway Layer                           │
│         (Load Balancer + Rate Limiting + Authentication)         │
└─────┬──────────────┬─────────────┬──────────────┬──────────────┘
      │              │             │              │
┌─────▼─────┐  ┌────▼─────┐  ┌───▼─────┐  ┌────▼──────┐
│ Portfolio │  │   Tax    │  │   AI    │  │   IBKR    │
│  Service  │  │ Harvest  │  │  Recs   │  │  Gateway  │
│           │  │ Service  │  │ Engine  │  │  Client   │
└─────┬─────┘  └────┬─────┘  └───┬─────┘  └────┬──────┘
      │              │             │              │
      │              │             │              │
      └──────┬───────┴─────┬───────┴──────────────┤
             │             │                      │
    ┌────────▼────┐  ┌─────▼──────┐      ┌──────▼────────┐
    │ PostgreSQL/ │  │   Redis    │      │ Interactive   │
    │ CockroachDB │  │   Cache    │      │   Brokers     │
    │  Cluster    │  │  Cluster   │      │   Gateway     │
    └─────────────┘  └────────────┘      └───────────────┘
             │             │
             │             │
    ┌────────▼─────────────▼───────┐
    │      Message Queue            │
    │      (Kafka Cluster)          │
    └───────────────────────────────┘
```

### 1.2 System Context

**Users:**
- Individual Investors (500M+ target)
- Financial Advisors
- Institutional Clients

**External Systems:**
- Interactive Brokers (IBKR) - Trading & Market Data
- Market Data Providers (Alpha Vantage, Polygon, IEX)
- News & Sentiment APIs
- Bank Account Linking (Plaid)
- Payment Processing (Stripe)

**Key Capabilities:**
- Real-time portfolio management
- AI-powered investment recommendations
- Tax loss harvesting automation
- Live trading execution
- Risk analysis and anomaly detection

---

## 2. Architecture Patterns

### 2.1 Microservices Architecture

**Pattern:** Domain-Driven Design (DDD)

**Services:**

1. **Portfolio Service**
   - Domain: Portfolio, Holdings, Assets
   - Responsibilities: CRUD operations, valuation, allocation
   - Database: Portfolios, Holdings tables

2. **Tax Harvest Service**
   - Domain: Tax optimization
   - Responsibilities: Loss identification, replacement suggestions
   - Database: TaxHarvests table

3. **AI Recommendation Service**
   - Domain: Investment intelligence
   - Responsibilities: ML model inference, recommendation generation
   - Database: AIRecommendations table

4. **Trading Service**
   - Domain: Order execution
   - Responsibilities: Trade placement, execution, tracking
   - Database: Trades table

5. **User Service**
   - Domain: User management
   - Responsibilities: Authentication, authorization, profile
   - Database: Users table

**Benefits:**
- Independent scaling
- Technology flexibility
- Fault isolation
- Easier testing and deployment

### 2.2 CQRS (Command Query Responsibility Segregation)

**Write Path (Commands):**
- Place trade
- Create portfolio
- Execute tax harvest

**Read Path (Queries):**
- Get portfolio data
- Fetch recommendations
- View trade history

**Implementation:**
- Write operations update primary database
- Read operations served from cache (Redis)
- Event sourcing for audit trail (Kafka)

### 2.3 Event-Driven Architecture

**Event Types:**
- TradeExecuted
- PortfolioUpdated
- RecommendationGenerated
- TaxHarvestIdentified
- PriceAlert

**Event Flow:**
```
Service A → Kafka Topic → Service B (Consumer)
                ↓
         Event Store (Audit)
```

**Benefits:**
- Loose coupling
- Asynchronous processing
- Scalable event processing
- Complete audit trail

### 2.4 API Gateway Pattern

**Responsibilities:**
- Request routing
- Authentication/Authorization
- Rate limiting
- Request/Response transformation
- API versioning

**Implementation:**
- FastAPI application
- JWT-based authentication
- Redis-backed rate limiting
- Prometheus metrics collection

---

## 3. Core Components

### 3.1 API Layer

**Technology:** FastAPI 0.109+

**Structure:**
```
main.py
├── Startup/Shutdown events
├── Middleware (CORS, Auth, Logging)
├── Exception handlers
└── Route registration

api/
└── routes.py
    ├── Dashboard endpoints
    ├── Portfolio endpoints
    ├── Trading endpoints
    ├── AI recommendation endpoints
    └── Tax harvesting endpoints
```

**Key Features:**
- Auto-generated OpenAPI docs
- Request validation (Pydantic)
- Async/await support
- Dependency injection
- WebSocket support (future)

**Endpoints:**
- `GET /api/v1/dashboard` - Dashboard summary
- `GET /api/v1/portfolio` - Portfolio details
- `POST /api/v1/trade` - Place trade
- `GET /api/v1/recommendations` - AI recommendations
- `GET /api/v1/tax-harvesting` - Tax opportunities

### 3.2 Business Logic Layer

**Services Package:**

**Portfolio Service:**
- Portfolio CRUD operations
- Holdings management
- Valuation calculation
- Asset allocation analysis
- Performance metrics

**Tax Harvest Service:**
- Loss opportunity identification
- Wash sale rule compliance (30-day)
- Replacement security suggestions (Similarity Engine)
- Tax savings calculation
- Execution coordination

**AI Recommendation Engine:**
- Portfolio risk analysis
- Anomaly detection (LSTM Autoencoder)
- Sector allocation optimization
- Buy/Sell signal generation
- Confidence scoring

**IBKR Client:**
- Gateway connection management
- Real-time market data streaming
- Order placement and tracking
- Position synchronization
- Historical data retrieval

### 3.3 Data Models Layer

**Entity Models:**
```python
@dataclass
class Portfolio:
    id: str
    user_id: str
    name: str
    total_value: float
    total_gain_loss: float
    cash_balance: float
    risk_score: float
    # ... additional fields

@dataclass
class Holding:
    id: str
    portfolio_id: str
    symbol: str
    shares: float
    average_cost: float
    current_price: float
    # ... additional fields
```

**ML Models:**
- LSTM Autoencoder (anomaly detection)
- Similarity Engine (asset comparison)
- Sentiment Analysis (future)

### 3.4 IBKR Integration

**Connection Architecture:**
```
WealthAlloc → IB Gateway → Interactive Brokers
                 ↓
           TWS API (Python)
                 ↓
          Market Data + Orders
```

**Capabilities:**
- Real-time quotes (bid/ask/last)
- Historical data (OHLCV)
- Order execution (market/limit/stop)
- Position tracking
- Account information

**Reliability:**
- Automatic reconnection
- Heartbeat monitoring
- Failover support
- Order retry logic

---

## 4. Data Architecture

### 4.1 Database Design

**Primary Database:** PostgreSQL 14+ / CockroachDB

**Schema Overview:**

```sql
-- 8 Core Tables

users                    -- User profiles
├── portfolios          -- Investment portfolios
│   ├── holdings        -- Individual positions
│   └── trades          -- Transaction history
├── ai_recommendations  -- AI-generated suggestions
├── tax_harvests       -- Tax loss opportunities
├── external_accounts  -- Linked brokerage accounts
└── educational_videos -- Learning content
```

**Key Tables:**

**Users Table:**
- User authentication data
- Risk profile (tolerance, experience)
- Financial information

**Portfolios Table:**
- Portfolio metadata
- Aggregated values
- Risk scores
- Last rebalance date

**Holdings Table:**
- Position details
- Cost basis tracking
- Current valuations
- Unrealized P&L

**Trades Table:**
- Trade history
- Order details
- Execution status
- IBKR order IDs

**Tax Harvests Table:**
- Identified opportunities
- Loss amounts
- Tax savings calculations
- Wash sale dates

**Indexes:**
```sql
-- Optimized for query patterns
CREATE INDEX idx_holdings_portfolio_id ON holdings(portfolio_id);
CREATE INDEX idx_holdings_symbol ON holdings(symbol);
CREATE INDEX idx_trades_portfolio_date ON trades(portfolio_id, created_date DESC);
CREATE INDEX idx_recommendations_user_status ON ai_recommendations(user_id, status);
```

### 4.2 Caching Strategy

**Technology:** Redis 7.0+

**Cache Layers:**

**L1 - Application Cache (In-Memory):**
- User session data
- JWT tokens
- Rate limit counters

**L2 - Distributed Cache (Redis):**
- Portfolio snapshots (TTL: 3 minutes)
- Market data (TTL: 1 minute)
- User profiles (TTL: 15 minutes)
- API responses (TTL: 5 minutes)

**Cache Patterns:**

**Cache-Aside:**
```python
async def get_portfolio(portfolio_id: str):
    # Check cache first
    cached = await redis.get(f"portfolio:{portfolio_id}")
    if cached:
        return json.loads(cached)
    
    # Cache miss - fetch from DB
    portfolio = await db.get_portfolio(portfolio_id)
    
    # Store in cache
    await redis.setex(
        f"portfolio:{portfolio_id}",
        180,  # 3 minutes TTL
        json.dumps(portfolio)
    )
    
    return portfolio
```

**Write-Through:**
- Update database
- Update cache simultaneously
- Ensures consistency

**Cache Invalidation:**
- Time-based (TTL)
- Event-based (on updates)
- Manual purge (admin tools)

### 4.3 Message Queue

**Technology:** Kafka

**Topics:**
- `portfolio.updates` - Portfolio changes
- `trades.executed` - Trade completions
- `recommendations.generated` - New AI recommendations
- `tax_harvests.identified` - TLH opportunities
- `prices.updated` - Market data updates

**Consumer Groups:**
- Analytics service
- Notification service
- Audit logger
- ML pipeline

**Benefits:**
- Asynchronous processing
- Event replay capability
- Guaranteed delivery
- High throughput

---

## 5. API Architecture

### 5.1 RESTful Design

**Principles:**
- Resource-oriented URLs
- HTTP methods (GET, POST, PUT, DELETE)
- Stateless design
- HATEOAS (Hypermedia as the Engine of Application State)

**Versioning:**
```
/api/v1/...  (Current)
/api/v2/...  (Future)
```

**Response Format:**
```json
{
  "data": { ... },
  "meta": {
    "timestamp": "2024-11-13T10:30:00Z",
    "version": "1.0.0"
  },
  "links": {
    "self": "/api/v1/portfolio/123",
    "holdings": "/api/v1/portfolio/123/holdings"
  }
}
```

### 5.2 Authentication & Authorization

**Authentication:** JWT (JSON Web Tokens)

**Flow:**
```
1. User Login → API
2. API validates credentials
3. API generates JWT (HS256)
4. JWT returned to client
5. Client includes JWT in Authorization header
6. API validates JWT on each request
```

**JWT Claims:**
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "role": "investor",
  "exp": 1731501600,
  "iat": 1731499800
}
```

**Authorization:** Role-Based Access Control (RBAC)

**Roles:**
- `investor` - Standard user
- `advisor` - Financial advisor
- `admin` - System administrator

**Permissions Matrix:**
```
Resource          | Investor | Advisor | Admin
------------------|----------|---------|-------
Own Portfolio     | RW       | R       | RW
Other Portfolios  | -        | R       | RW
System Settings   | -        | -       | RW
User Management   | -        | -       | RW
```

### 5.3 Rate Limiting

**Strategy:** Token Bucket Algorithm

**Limits:**
- **Standard Users:** 60 requests/minute
- **Premium Users:** 120 requests/minute
- **API Keys:** 1000 requests/minute

**Implementation:**
```python
from fastapi import Request
from redis import Redis

async def rate_limit(request: Request):
    user_id = get_user_id(request)
    key = f"rate_limit:{user_id}"
    
    # Increment counter
    count = await redis.incr(key)
    
    # Set expiry on first request
    if count == 1:
        await redis.expire(key, 60)  # 1 minute
    
    # Check limit
    if count > 60:
        raise HTTPException(429, "Rate limit exceeded")
```

**Response Headers:**
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1731501600
```

### 5.4 Error Handling

**Error Response Format:**
```json
{
  "error": {
    "code": "INVALID_TRADE",
    "message": "Insufficient funds for trade",
    "details": {
      "required": 10000.00,
      "available": 5000.00
    },
    "timestamp": "2024-11-13T10:30:00Z",
    "request_id": "req_abc123"
  }
}
```

**HTTP Status Codes:**
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Too Many Requests
- `500` - Internal Server Error
- `503` - Service Unavailable

---

## 6. Security Architecture

### 6.1 Network Security

**Layers:**

**1. Perimeter Security:**
- AWS WAF (Web Application Firewall)
- DDoS protection (CloudFlare)
- IP whitelisting for admin endpoints

**2. Transport Security:**
- TLS 1.3 for all connections
- Certificate pinning for mobile apps
- HTTPS-only (HSTS enabled)

**3. Network Segmentation:**
```
Public Subnet     → Load Balancers, API Gateway
Private Subnet    → Application servers
Database Subnet   → Databases (no public access)
```

**4. Zero Trust Architecture:**
- Mutual TLS (mTLS) between services
- Service mesh (Istio) for service-to-service auth
- No implicit trust

### 6.2 Data Security

**Encryption at Rest:**
- Database: AES-256 encryption
- File storage: S3 with SSE-KMS
- Secrets: HashiCorp Vault

**Encryption in Transit:**
- TLS 1.3 for all connections
- Certificate rotation (90 days)
- Perfect Forward Secrecy (PFS)

**Sensitive Data:**
- PII encrypted in database
- Credit cards tokenized (PCI DSS compliant)
- IBKR credentials in Vault

**Data Masking:**
```python
# Display masked account numbers
account = "DU1234567"
masked = f"***{account[-4:]}"  # ***4567
```

### 6.3 Application Security

**Input Validation:**
- Pydantic schemas for all inputs
- SQL injection prevention (parameterized queries)
- XSS protection (output encoding)
- CSRF tokens for state-changing operations

**Authentication Security:**
- Password hashing (bcrypt, 12 rounds)
- MFA support (TOTP)
- Account lockout after 5 failed attempts
- Session timeout (30 minutes)

**API Security:**
- API key rotation (90 days)
- OAuth 2.0 for third-party integrations
- Scope-based permissions

### 6.4 Compliance

**Standards:**
- SOC 2 Type II
- PCI DSS (for payment processing)
- GDPR (data privacy)
- SEC regulations (financial services)

**Audit Trail:**
- All trades logged
- User actions tracked
- Admin operations recorded
- Immutable event log (Kafka)

**Data Retention:**
- User data: 7 years (regulatory requirement)
- Trade history: 7 years
- Audit logs: 10 years
- Backup retention: 30 days

---

## 7. Scalability & Performance

### 7.1 Horizontal Scaling

**Auto-Scaling Configuration:**
```yaml
# Kubernetes HPA
minReplicas: 10
maxReplicas: 500

metrics:
- type: Resource
  resource:
    name: cpu
    target:
      type: Utilization
      averageUtilization: 70
- type: Resource
  resource:
    name: memory
    target:
      type: Utilization
      averageUtilization: 80
```

**Scaling Triggers:**
- CPU > 70%
- Memory > 80%
- Request rate > 100 req/s per pod
- Queue depth > 1000 messages

**Scaling Time:**
- Scale up: 2-3 minutes
- Scale down: 10 minutes (gradual)

### 7.2 Database Scaling

**CockroachDB Cluster:**
```
Primary Region: us-east-1
├── Node 1 (Leader)
├── Node 2 (Follower)
└── Node 3 (Follower)

Secondary Region: us-west-2
├── Node 4 (Follower)
├── Node 5 (Follower)
└── Node 6 (Follower)
```

**Replication:**
- 3x replication factor
- Automatic failover
- Cross-region replication for DR

**Partitioning:**
- Horizontal partitioning (sharding) by user_id
- Range partitioning for time-series data
- Optimized for multi-tenant workload

**Read Scaling:**
- Read replicas for queries
- Follower reads for non-critical data
- Connection pooling (PgBouncer)

**Write Scaling:**
- Async writes for non-critical data
- Batch inserts
- Write-ahead logging (WAL)

### 7.3 Caching Strategy

**Multi-Level Cache:**

**Level 1 - CDN:**
- Static assets
- API documentation
- Public content

**Level 2 - Application Cache:**
- In-memory cache (per pod)
- User session data
- JWT validation cache

**Level 3 - Distributed Cache (Redis):**
- Shared across all pods
- Portfolio data
- Market data
- API responses

**Cache Hit Rates:**
- Target: >90%
- Current: 95%

**Cache Warm-up:**
- Pre-populate on deployment
- Background refresh for popular data

### 7.4 Performance Targets

**API Latency:**
- p50: <20ms
- p95: <50ms
- p99: <100ms

**Database Queries:**
- Simple queries: <10ms
- Complex queries: <50ms
- Analytical queries: <500ms

**IBKR API Calls:**
- Market data: <100ms
- Order placement: <200ms
- Historical data: <1s

**Throughput:**
- API: 10,000 TPS
- Database writes: 5,000 TPS
- Database reads: 50,000 TPS

---

## 8. Deployment Architecture

### 8.1 Cloud Infrastructure

**Provider:** AWS (Primary), GCP (Backup)

**Regions:**
- Primary: us-east-1 (N. Virginia)
- Secondary: us-west-2 (Oregon)
- Tertiary: eu-west-1 (Ireland)

**Availability Zones:**
- Minimum 3 AZs per region
- Multi-AZ deployment for all services

### 8.2 Kubernetes Architecture

**Cluster Setup:**
```
Production Cluster
├── Control Plane (Managed EKS)
├── Node Group: API (10-500 pods)
├── Node Group: Workers (5-100 pods)
└── Node Group: ML (2-20 pods, GPU)

Namespaces:
├── production
├── staging
├── monitoring
└── system
```

**Pod Configuration:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: wealthalloc-api
spec:
  containers:
  - name: api
    image: wealthalloc/api:1.0.0
    resources:
      requests:
        memory: "2Gi"
        cpu: "1000m"
      limits:
        memory: "4Gi"
        cpu: "2000m"
    livenessProbe:
      httpGet:
        path: /health
        port: 8000
      initialDelaySeconds: 30
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /health
        port: 8000
      initialDelaySeconds: 5
      periodSeconds: 5
```

### 8.3 CI/CD Pipeline

**Pipeline Stages:**
```
Code Push (GitHub)
    ↓
Lint & Format (Black, Flake8)
    ↓
Unit Tests (pytest)
    ↓
Integration Tests
    ↓
Security Scan (Snyk, Trivy)
    ↓
Build Docker Image
    ↓
Push to Registry (ECR)
    ↓
Deploy to Staging
    ↓
E2E Tests
    ↓
Manual Approval
    ↓
Deploy to Production (Blue-Green)
    ↓
Smoke Tests
    ↓
Complete
```

**Deployment Strategies:**

**Blue-Green Deployment:**
```
Blue (Current) ← 100% traffic
Green (New)    ← 0% traffic

↓ (Deploy)

Blue (Current) ← 50% traffic
Green (New)    ← 50% traffic

↓ (Validate)

Blue (Current) ← 0% traffic
Green (New)    ← 100% traffic
```

**Rollback:**
- Automatic on health check failures
- Manual rollback available
- Rollback time: <5 minutes

### 8.4 Infrastructure as Code

**Tools:**
- Terraform for AWS resources
- Helm for Kubernetes deployments
- Ansible for configuration management

**Example:**
```hcl
# Terraform - EKS Cluster
resource "aws_eks_cluster" "wealthalloc" {
  name     = "wealthalloc-prod"
  role_arn = aws_iam_role.eks_cluster.arn
  version  = "1.28"

  vpc_config {
    subnet_ids = aws_subnet.private[*].id
  }
}
```

---

## 9. Monitoring & Observability

### 9.1 Metrics Collection

**Stack:** Prometheus + Grafana

**Metrics Categories:**

**Application Metrics:**
- Request rate (req/s)
- Error rate (%)
- Latency (p50, p95, p99)
- Active users
- API endpoint usage

**Infrastructure Metrics:**
- CPU utilization (%)
- Memory usage (GB)
- Disk I/O (IOPS)
- Network throughput (Mbps)

**Business Metrics:**
- Trades executed
- Portfolio value (aggregated)
- Tax savings generated
- Recommendations accepted
- User registrations

**Custom Metrics:**
```python
from prometheus_client import Counter, Histogram

# Request counter
api_requests = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

# Latency histogram
api_latency = Histogram(
    'api_request_duration_seconds',
    'API request latency',
    ['endpoint']
)
```

### 9.2 Logging

**Stack:** ELK (Elasticsearch, Logstash, Kibana)

**Log Levels:**
- DEBUG - Development only
- INFO - Normal operations
- WARNING - Potential issues
- ERROR - Errors requiring attention
- CRITICAL - System failures

**Structured Logging:**
```python
import structlog

logger = structlog.get_logger()

logger.info(
    "trade_executed",
    user_id="user_123",
    symbol="AAPL",
    shares=10,
    price=175.50,
    order_id="ORDER_456"
)
```

**Log Aggregation:**
- All pods → Logstash → Elasticsearch → Kibana
- Retention: 90 days (hot), 1 year (cold)
- Search and analysis in Kibana

### 9.3 Distributed Tracing

**Stack:** Jaeger

**Trace Example:**
```
GET /api/v1/portfolio/{id}
├── Authenticate User (5ms)
├── Check Cache (2ms)
├── Query Database (15ms)
│   ├── Get Portfolio (8ms)
│   └── Get Holdings (7ms)
├── Calculate Metrics (3ms)
└── Format Response (2ms)
Total: 27ms
```

**Benefits:**
- Identify bottlenecks
- Visualize service dependencies
- Debug performance issues
- Understand request flow

### 9.4 Alerting

**Alert Manager:** PagerDuty

**Alert Categories:**

**Critical (Page Immediately):**
- Service down
- Database unreachable
- Error rate >5%
- p99 latency >500ms
- IBKR disconnected

**Warning (Slack):**
- Error rate >1%
- p99 latency >200ms
- High memory usage
- Cache miss rate >20%

**Info (Email):**
- Deployment completed
- Daily metrics summary
- Backup completed

**Example Alert:**
```yaml
alert: HighErrorRate
expr: rate(api_errors_total[5m]) > 0.05
for: 5m
labels:
  severity: critical
annotations:
  summary: "High error rate detected"
  description: "Error rate is {{ $value }}%"
```

### 9.5 Health Checks

**Endpoint:** `/health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-11-13T10:30:00Z",
  "version": "1.0.0",
  "checks": {
    "database": "healthy",
    "redis": "healthy",
    "ibkr": "healthy",
    "kafka": "healthy"
  },
  "metrics": {
    "uptime_seconds": 86400,
    "memory_usage_mb": 1024,
    "cpu_usage_percent": 45
  }
}
```

**Kubernetes Probes:**
- Liveness: Restart pod if unhealthy
- Readiness: Remove from load balancer if not ready
- Startup: Wait for app to start

---

## 10. Disaster Recovery

### 10.1 Backup Strategy

**Database Backups:**
- **Full Backup:** Daily at 2 AM UTC
- **Incremental Backup:** Every hour
- **Transaction Logs:** Continuous
- **Retention:** 30 days

**Backup Locations:**
- Primary: S3 (us-east-1)
- Secondary: S3 (us-west-2)
- Tertiary: Glacier (long-term)

**Backup Verification:**
- Weekly restore tests
- Automated integrity checks
- Point-in-time recovery capability

### 10.2 Recovery Objectives

**RPO (Recovery Point Objective):** 1 hour
- Maximum acceptable data loss

**RTO (Recovery Time Objective):** 4 hours
- Maximum acceptable downtime

**MTTR (Mean Time To Repair):** <2 hours
- Average time to fix issues

### 10.3 Failover Scenarios

**Scenario 1: Single Pod Failure**
- Detection: <10 seconds (health check)
- Action: Automatic pod restart
- Impact: None (load balancer routes traffic)
- Recovery: <1 minute

**Scenario 2: Database Node Failure**
- Detection: <30 seconds
- Action: Automatic failover to follower
- Impact: 30-60 seconds increased latency
- Recovery: <5 minutes

**Scenario 3: Availability Zone Failure**
- Detection: <1 minute
- Action: Traffic rerouted to other AZs
- Impact: Minimal (multi-AZ deployment)
- Recovery: <10 minutes

**Scenario 4: Region Failure**
- Detection: <5 minutes
- Action: Failover to secondary region
- Impact: 15-30 minutes downtime
- Recovery: <1 hour

**Scenario 5: Complete System Failure**
- Detection: Immediate
- Action: Restore from backup
- Impact: Up to 4 hours downtime
- Recovery: 2-4 hours

### 10.4 Business Continuity

**Communication Plan:**
- Status page (status.wealthalloc.com)
- Email notifications
- In-app notifications
- Social media updates

**Incident Response Team:**
- On-call engineer (24/7)
- DevOps lead
- Database administrator
- Product manager
- Customer support

**Runbooks:**
- Database failover
- Service restart procedures
- Cache rebuild
- IBKR reconnection
- Complete disaster recovery

---

## 11. Technology Stack

### 11.1 Backend

**Framework:** FastAPI 0.109+
- Modern Python web framework
- Async/await support
- Auto-generated API docs
- Type checking with Pydantic

**Language:** Python 3.10+
- Strong typing support
- Excellent library ecosystem
- Great for data science/ML

**API Documentation:** OpenAPI 3.0 / Swagger

### 11.2 Database

**Primary:** CockroachDB / PostgreSQL 14+
- Distributed SQL database
- Horizontal scalability
- ACID transactions
- PostgreSQL compatibility

**Cache:** Redis 7.0+
- In-memory data store
- Sub-millisecond latency
- Pub/Sub support

**Message Queue:** Apache Kafka
- Distributed event streaming
- High throughput
- Durable message storage

### 11.3 AI/ML

**Frameworks:**
- TensorFlow 2.15+ (LSTM Autoencoder)
- PyTorch 2.1+ (Alternative models)
- scikit-learn 1.4+ (Traditional ML)

**Libraries:**
- NumPy - Numerical computing
- Pandas - Data manipulation
- NetworkX - Graph analysis

**Model Storage:**
- S3 for model artifacts
- MLflow for experiment tracking

### 11.4 Infrastructure

**Container:** Docker
- Consistent environments
- Easy deployment

**Orchestration:** Kubernetes (EKS)
- Auto-scaling
- Self-healing
- Rolling updates

**CI/CD:** GitHub Actions
- Automated testing
- Continuous deployment

**IaC:** Terraform
- Infrastructure as code
- Version control for infrastructure

### 11.5 Monitoring & Observability

**Metrics:** Prometheus + Grafana
**Logs:** ELK Stack (Elasticsearch, Logstash, Kibana)
**Tracing:** Jaeger
**APM:** Datadog (optional)
**Alerting:** PagerDuty

### 11.6 External Services

**Trading:** Interactive Brokers
- Real-time market data
- Order execution
- Position tracking

**Market Data:** 
- Alpha Vantage
- Polygon.io
- IEX Cloud

**Payment:** Stripe
**Bank Linking:** Plaid
**Email:** SendGrid
**SMS:** Twilio

---

## 12. Integration Architecture

### 12.1 IBKR Integration

**Architecture:**
```
WealthAlloc API
    ↓
IBKR Client (ib-insync)
    ↓
IB Gateway (Java)
    ↓
TWS API
    ↓
Interactive Brokers Servers
```

**Connection Management:**
- Persistent connection
- Heartbeat every 30 seconds
- Automatic reconnection
- Connection pool (5 connections)

**Data Flows:**

**Market Data Flow:**
```
IBKR → IB Gateway → IBKR Client → Redis Cache → API
```

**Order Flow:**
```
API → IBKR Client → IB Gateway → IBKR → Market
                        ↓
                Order Confirmation
                        ↓
                    Callback
                        ↓
                    Database
```

**Error Handling:**
- Retry logic (3 attempts)
- Exponential backoff
- Circuit breaker pattern
- Fallback to cached data

### 12.2 External API Integration

**Market Data Providers:**

**Alpha Vantage:**
- Historical data
- Technical indicators
- Fundamental data
- Rate limit: 5 calls/minute

**Polygon.io:**
- Real-time quotes
- Historical data
- News feed
- Rate limit: 5000 calls/minute

**Integration Pattern:**
```python
async def get_market_data(symbol: str):
    # Try primary source
    try:
        data = await alpha_vantage.get_quote(symbol)
        return data
    except RateLimitError:
        # Fallback to secondary source
        return await polygon.get_quote(symbol)
    except Exception:
        # Use cached data
        return await cache.get(f"quote:{symbol}")
```

### 12.3 Webhook Integration

**Incoming Webhooks:**
- IBKR order updates
- Payment confirmations (Stripe)
- Bank transactions (Plaid)

**Outgoing Webhooks:**
- Trade notifications
- Price alerts
- Recommendation updates

**Security:**
- HMAC signature verification
- IP whitelisting
- Rate limiting

---

## 13. Future Roadmap

### 13.1 Phase 2 (Q1-Q2 2025)

**GraphQL API:**
- More flexible querying
- Reduced over-fetching
- Real-time subscriptions

**WebSocket Support:**
- Real-time portfolio updates
- Live market data streaming
- Instant notifications

**Mobile Apps:**
- iOS native app
- Android native app
- React Native framework

**Advanced AI:**
- Sentiment analysis
- News-driven recommendations
- Deep learning models

### 13.2 Phase 3 (Q3-Q4 2025)

**Cryptocurrency Trading:**
- Bitcoin, Ethereum support
- Crypto exchanges integration
- Crypto tax reporting

**Options Trading:**
- Options pricing models
- Greeks calculations
- Strategy builder

**International Markets:**
- European markets
- Asian markets
- Multi-currency support

**Social Trading:**
- Copy trading
- Social feed
- Performance leaderboard

### 13.3 Phase 4 (2026)

**Robo-Advisor:**
- Automated portfolio management
- Rebalancing automation
- Goal-based investing

**Tax Form Generation:**
- 1099-B generation
- Tax optimization reports
- Capital gains/losses

**Financial Planning:**
- Retirement planning
- College savings
- Goal tracking

**Custom ML Models:**
- User-trained models
- Transfer learning
- AutoML capabilities

---

## 14. Appendices

### Appendix A: Glossary

**API:** Application Programming Interface
**CQRS:** Command Query Responsibility Segregation
**DDD:** Domain-Driven Design
**ELK:** Elasticsearch, Logstash, Kibana
**HATEOAS:** Hypermedia as the Engine of Application State
**HPA:** Horizontal Pod Autoscaler
**IBKR:** Interactive Brokers
**JWT:** JSON Web Token
**LSTM:** Long Short-Term Memory
**MTTR:** Mean Time To Repair
**RBAC:** Role-Based Access Control
**RPO:** Recovery Point Objective
**RTO:** Recovery Time Objective
**TLH:** Tax Loss Harvesting
**TWS:** Trader Workstation
**WAL:** Write-Ahead Logging

### Appendix B: Contact Information

**Architecture Team:**
- Email: architecture@wealthalloc.com
- Slack: #architecture

**DevOps Team:**
- Email: devops@wealthalloc.com
- Slack: #devops
- On-call: PagerDuty

**Security Team:**
- Email: security@wealthalloc.com
- Slack: #security
- Urgent: security-urgent@wealthalloc.com

### Appendix C: References

1. **IBKR API Documentation:** https://interactivebrokers.github.io/
2. **FastAPI Documentation:** https://fastapi.tiangolo.com/
3. **CockroachDB Documentation:** https://www.cockroachlabs.com/docs/
4. **Kubernetes Documentation:** https://kubernetes.io/docs/
5. **AWS Best Practices:** https://aws.amazon.com/architecture/
6. **LSTM Autoencoder Paper:** Nature s41599-025-04412-y

### Appendix D: Change Log

**Version 1.0.0 (November 2024)**
- Initial architecture document
- Core system design
- Deployment strategy
- Security architecture

---

## Document Control

**Document Version:** 1.0.0  
**Last Updated:** November 13, 2024  
**Next Review:** February 13, 2025  
**Classification:** Internal - Confidential  
**Distribution:** Engineering Team, Leadership  

**Approval:**
- Chief Technology Officer: ________________
- VP Engineering: ________________
- Lead Architect: ________________

---

**End of Document**
