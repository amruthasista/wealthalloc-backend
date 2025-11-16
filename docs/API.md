# WealthAlloc API Documentation

Base URL: `https://api.wealthalloc.com/api/v1`

## Authentication

All endpoints require JWT authentication (except `/health`).

```
Authorization: Bearer <token>
```

## Endpoints

### Dashboard

#### GET /dashboard

Get dashboard summary data.

**Response:**
```json
{
  "portfolio": {
    "id": "uuid",
    "total_value": 100000.00,
    "total_gain_loss": 10000.00,
    "total_gain_loss_percent": 11.11,
    "cash_balance": 5000.00,
    "risk_score": 55.0
  },
  "holdings": [...],
  "allocation": {
    "Technology": 65000.00,
    "Financial": 20000.00
  },
  "total_tax_savings": 2500.00
}
```

### Portfolio

#### GET /portfolio

Get complete portfolio data including all holdings.

**Response:**
```json
{
  "portfolio": {...},
  "holdings": [
    {
      "id": "uuid",
      "symbol": "AAPL",
      "company_name": "Apple Inc.",
      "shares": 100.0,
      "average_cost": 150.00,
      "current_price": 175.00,
      "total_value": 17500.00,
      "total_gain_loss": 2500.00,
      "total_gain_loss_percent": 16.67,
      "sector": "Technology"
    }
  ]
}
```

### Trading

#### POST /trade

Create a new trade order.

**Request:**
```json
{
  "portfolio_id": "uuid",
  "symbol": "AAPL",
  "trade_type": "buy",
  "order_type": "market",
  "shares": 10.0,
  "limit_price": 175.00,  // optional
  "stop_price": 170.00    // optional
}
```

**Response:**
```json
{
  "trade": {
    "id": "uuid",
    "status": "executed",
    "price": 174.50,
    "total_amount": 1745.00,
    "executed_at": "2024-01-15T10:30:00Z"
  },
  "order_id": "IBKR_123456"
}
```

#### GET /trade-history

Get trade history.

**Query Parameters:**
- `limit`: Number of trades to return (max 500, default 100)

**Response:**
```json
{
  "trades": [...]
}
```

### AI Recommendations

#### GET /recommendations

Get AI-generated recommendations.

**Response:**
```json
{
  "recommendations": [
    {
      "id": "uuid",
      "title": "Strong Buy Signal on NVDA",
      "description": "AI analysis indicates...",
      "recommendation_type": "buy",
      "symbol": "NVDA",
      "confidence_score": 87.5,
      "potential_gain": 5000.00,
      "risk_level": "medium",
      "priority": "high",
      "status": "active",
      "expires_at": "2024-01-22T00:00:00Z"
    }
  ],
  "total_count": 4,
  "active_count": 3
}
```

#### PUT /recommendations/{rec_id}

Update recommendation status.

**Request:**
```json
{
  "status": "acted_upon"  // or "dismissed", "expired"
}
```

### Tax Loss Harvesting

#### GET /tax-harvesting

Get tax loss harvesting opportunities.

**Response:**
```json
{
  "tax_harvests": [
    {
      "id": "uuid",
      "symbol": "TSLA",
      "shares": 30.0,
      "purchase_price": 250.00,
      "current_price": 245.00,
      "loss_amount": 150.00,
      "tax_savings": 37.50,
      "purchase_date": "2024-01-15",
      "status": "identified",
      "wash_sale_date": "2024-02-14"
    }
  ],
  "total_potential_savings": 2500.00,
  "current_year_harvested": 0.00
}
```

#### POST /tax-harvesting/execute

Execute a tax harvest.

**Request:**
```json
{
  "harvest_id": "uuid"
}
```

**Response:**
```json
{
  "success": true,
  "harvest": {...},
  "replacement_suggestions": [
    {
      "symbol": "TSLA_ALT1",
      "similarity_score": 0.92,
      "reason": "High correlation, same sector"
    }
  ]
}
```

### External Accounts

#### GET /external-accounts

Get linked external accounts.

**Response:**
```json
{
  "accounts": [
    {
      "id": "uuid",
      "account_name": "Fidelity 401k",
      "broker_name": "Fidelity",
      "account_type": "401k",
      "total_value": 250000.00,
      "connection_status": "connected",
      "last_synced": "2024-01-15T10:00:00Z"
    }
  ]
}
```

### Educational Videos

#### GET /educational-videos

Get educational video library.

**Query Parameters:**
- `category`: Filter by category (optional)

**Response:**
```json
{
  "videos": [
    {
      "id": "uuid",
      "title": "Getting Started with Investing",
      "description": "Learn the basics...",
      "video_url": "https://...",
      "thumbnail_url": "https://...",
      "duration": 600,
      "category": "beginner",
      "difficulty_level": "beginner",
      "views": 1000,
      "is_interactive": false
    }
  ]
}
```

### User Profile

#### GET /profile

Get user profile.

**Response:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "phone": "+1-555-0123",
  "risk_tolerance": "moderate",
  "investment_experience": "intermediate",
  "annual_income": 150000.00
}
```

#### PUT /profile

Update user profile.

**Request:**
```json
{
  "phone": "+1-555-0123",
  "risk_tolerance": "aggressive",
  "investment_experience": "advanced",
  "annual_income": 200000.00
}
```

### Market Data

#### GET /market-data/{symbol}

Get real-time market data for a symbol.

**Response:**
```json
{
  "symbol": "AAPL",
  "bid": 174.95,
  "ask": 175.00,
  "last": 174.98,
  "volume": 1000000,
  "timestamp": "2024-01-15T14:30:00Z"
}
```

### Health Check

#### GET /health

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T14:30:00Z",
  "ibkr_connected": true
}
```

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message",
  "error": "Additional error context"
}
```

### Status Codes

- `200`: Success
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `500`: Internal Server Error

## Rate Limiting

- Rate limit: 60 requests per minute per user
- Burst limit: 10 requests

Headers:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1705329600
```

## Webhooks

Coming soon: Real-time notifications for trades, recommendations, and price alerts.

## SDK Examples

### Python

```python
import httpx

async def get_dashboard():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.wealthalloc.com/api/v1/dashboard",
            headers={"Authorization": f"Bearer {token}"}
        )
        return response.json()
```

### JavaScript

```javascript
async function getDashboard() {
  const response = await fetch(
    'https://api.wealthalloc.com/api/v1/dashboard',
    {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  );
  return await response.json();
}
```

## Support

For API questions:
- Email: api-support@wealthalloc.com
- Slack: #api-support
