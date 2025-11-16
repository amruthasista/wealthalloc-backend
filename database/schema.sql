-- WealthAlloc Database Schema
-- Perfectly matches Base44 entities

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    risk_tolerance VARCHAR(20) CHECK (risk_tolerance IN ('conservative', 'moderate', 'aggressive')),
    investment_experience VARCHAR(20) CHECK (investment_experience IN ('beginner', 'intermediate', 'advanced')),
    annual_income DECIMAL(15, 2) DEFAULT 0,
    created_date TIMESTAMP DEFAULT NOW(),
    updated_date TIMESTAMP DEFAULT NOW()
);

-- Portfolios table
CREATE TABLE portfolios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    total_value DECIMAL(15, 2) DEFAULT 0,
    total_gain_loss DECIMAL(15, 2) DEFAULT 0,
    total_gain_loss_percent DECIMAL(10, 4) DEFAULT 0,
    cash_balance DECIMAL(15, 2) DEFAULT 0,
    risk_score DECIMAL(5, 2) DEFAULT 50,
    risk_tolerance VARCHAR(20) CHECK (risk_tolerance IN ('conservative', 'moderate', 'aggressive')),
    last_rebalanced DATE,
    created_date TIMESTAMP DEFAULT NOW(),
    updated_date TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_portfolios_user_id ON portfolios(user_id);

-- Holdings table
CREATE TABLE holdings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id) ON DELETE CASCADE,
    symbol VARCHAR(20) NOT NULL,
    company_name VARCHAR(255),
    shares DECIMAL(15, 4) NOT NULL,
    average_cost DECIMAL(15, 4) NOT NULL,
    current_price DECIMAL(15, 4) DEFAULT 0,
    total_value DECIMAL(15, 2) DEFAULT 0,
    total_gain_loss DECIMAL(15, 2) DEFAULT 0,
    total_gain_loss_percent DECIMAL(10, 4) DEFAULT 0,
    sector VARCHAR(100),
    asset_class VARCHAR(50) CHECK (asset_class IN ('stocks', 'etf', 'bonds', 'cash', 'alternatives')),
    created_date TIMESTAMP DEFAULT NOW(),
    updated_date TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_holdings_portfolio_id ON holdings(portfolio_id);
CREATE INDEX idx_holdings_symbol ON holdings(symbol);

-- Trades table
CREATE TABLE trades (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id) ON DELETE CASCADE,
    symbol VARCHAR(20) NOT NULL,
    trade_type VARCHAR(10) CHECK (trade_type IN ('buy', 'sell')),
    order_type VARCHAR(10) CHECK (order_type IN ('market', 'limit', 'stop')),
    shares DECIMAL(15, 4) NOT NULL,
    price DECIMAL(15, 4),
    limit_price DECIMAL(15, 4),
    stop_price DECIMAL(15, 4),
    total_amount DECIMAL(15, 2),
    status VARCHAR(20) CHECK (status IN ('pending', 'executed', 'cancelled', 'failed')),
    executed_at TIMESTAMP,
    notes TEXT,
    created_date TIMESTAMP DEFAULT NOW(),
    updated_date TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_trades_portfolio_id ON trades(portfolio_id);
CREATE INDEX idx_trades_created_date ON trades(created_date DESC);
CREATE INDEX idx_trades_status ON trades(status);

-- AI Recommendations table
CREATE TABLE ai_recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    recommendation_type VARCHAR(50) CHECK (recommendation_type IN ('buy', 'sell', 'rebalance', 'alert', 'opportunity')),
    symbol VARCHAR(20),
    confidence_score DECIMAL(5, 2),
    potential_gain DECIMAL(10, 4),
    risk_level VARCHAR(20) CHECK (risk_level IN ('low', 'medium', 'high')),
    priority VARCHAR(20) CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    status VARCHAR(20) CHECK (status IN ('active', 'acted_upon', 'dismissed', 'expired')),
    expires_at TIMESTAMP,
    created_date TIMESTAMP DEFAULT NOW(),
    updated_date TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_recommendations_user_id ON ai_recommendations(user_id);
CREATE INDEX idx_recommendations_status ON ai_recommendations(status);
CREATE INDEX idx_recommendations_created_date ON ai_recommendations(created_date DESC);

-- Tax Harvests table
CREATE TABLE tax_harvests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id) ON DELETE CASCADE,
    symbol VARCHAR(20) NOT NULL,
    shares DECIMAL(15, 4) NOT NULL,
    purchase_price DECIMAL(15, 4) NOT NULL,
    current_price DECIMAL(15, 4) NOT NULL,
    loss_amount DECIMAL(15, 2) NOT NULL,
    tax_savings DECIMAL(15, 2) NOT NULL,
    purchase_date DATE,
    status VARCHAR(20) CHECK (status IN ('identified', 'pending', 'executed', 'expired')),
    identified_date DATE,
    wash_sale_date DATE,
    created_date TIMESTAMP DEFAULT NOW(),
    updated_date TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tax_harvests_portfolio_id ON tax_harvests(portfolio_id);
CREATE INDEX idx_tax_harvests_status ON tax_harvests(status);
CREATE INDEX idx_tax_harvests_identified_date ON tax_harvests(identified_date DESC);

-- External Accounts table
CREATE TABLE external_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    account_name VARCHAR(255) NOT NULL,
    broker_name VARCHAR(255) NOT NULL,
    account_number VARCHAR(100),
    account_type VARCHAR(50) CHECK (account_type IN ('brokerage', 'retirement', 'ira', '401k')),
    total_value DECIMAL(15, 2) DEFAULT 0,
    cash_balance DECIMAL(15, 2) DEFAULT 0,
    connection_status VARCHAR(20) CHECK (connection_status IN ('connected', 'disconnected', 'error')),
    last_synced TIMESTAMP,
    api_key TEXT,
    created_date TIMESTAMP DEFAULT NOW(),
    updated_date TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_external_accounts_user_id ON external_accounts(user_id);

-- Educational Videos table
CREATE TABLE educational_videos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    video_url TEXT,
    thumbnail_url TEXT,
    duration INTEGER DEFAULT 0,
    category VARCHAR(100) CHECK (category IN ('beginner', 'intermediate', 'advanced', 'tax_strategy', 'portfolio_management', 'trading_basics', 'market_analysis')),
    difficulty_level VARCHAR(50) CHECK (difficulty_level IN ('beginner', 'intermediate', 'advanced')),
    tags TEXT[],
    views INTEGER DEFAULT 0,
    is_interactive BOOLEAN DEFAULT FALSE,
    created_date TIMESTAMP DEFAULT NOW(),
    updated_date TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_videos_category ON educational_videos(category);
CREATE INDEX idx_videos_difficulty ON educational_videos(difficulty_level);
CREATE INDEX idx_videos_views ON educational_videos(views DESC);

-- Triggers for updated_date
CREATE OR REPLACE FUNCTION update_updated_date_column()
RETURNS TRIGGER AS $
BEGIN
    NEW.updated_date = NOW();
    RETURN NEW;
END;
$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_date BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_date_column();

CREATE TRIGGER update_portfolios_updated_date BEFORE UPDATE ON portfolios
    FOR EACH ROW EXECUTE FUNCTION update_updated_date_column();

CREATE TRIGGER update_holdings_updated_date BEFORE UPDATE ON holdings
    FOR EACH ROW EXECUTE FUNCTION update_updated_date_column();

CREATE TRIGGER update_trades_updated_date BEFORE UPDATE ON trades
    FOR EACH ROW EXECUTE FUNCTION update_updated_date_column();

CREATE TRIGGER update_recommendations_updated_date BEFORE UPDATE ON ai_recommendations
    FOR EACH ROW EXECUTE FUNCTION update_updated_date_column();

CREATE TRIGGER update_tax_harvests_updated_date BEFORE UPDATE ON tax_harvests
    FOR EACH ROW EXECUTE FUNCTION update_updated_date_column();

CREATE TRIGGER update_external_accounts_updated_date BEFORE UPDATE ON external_accounts
    FOR EACH ROW EXECUTE FUNCTION update_updated_date_column();

CREATE TRIGGER update_videos_updated_date BEFORE UPDATE ON educational_videos
    FOR EACH ROW EXECUTE FUNCTION update_updated_date_column();

