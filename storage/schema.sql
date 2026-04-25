CREATE TABLE IF NOT EXISTS option_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    underlying TEXT NOT NULL,
    option_symbol TEXT NOT NULL,
    put_call TEXT NOT NULL,
    expiration TEXT,
    dte INTEGER,
    strike REAL,
    bid REAL,
    ask REAL,
    mark REAL,
    last REAL,
    volume INTEGER,
    open_interest INTEGER,
    iv REAL,
    delta REAL,
    gamma REAL,
    theta REAL,
    vega REAL,
    rho REAL,
    underlying_price REAL,
    spread_pct REAL,
    moneyness REAL
);

CREATE INDEX IF NOT EXISTS idx_option_snapshots_symbol_ts ON option_snapshots(underlying, option_symbol, ts);

CREATE TABLE IF NOT EXISTS contract_features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    underlying TEXT NOT NULL,
    option_symbol TEXT NOT NULL,
    put_call TEXT,
    expiration TEXT,
    dte INTEGER,
    strike REAL,
    new_volume INTEGER,
    premium_estimate REAL,
    delta_notional REAL,
    volume_oi REAL,
    iv_change REAL,
    mark_change REAL,
    spread_pct REAL,
    moneyness REAL,
    liquidity_score REAL,
    activity_score REAL,
    contract_score REAL
);

CREATE TABLE IF NOT EXISTS ticker_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    symbol TEXT NOT NULL,
    bullish_score REAL,
    bearish_score REAL,
    call_premium REAL,
    put_premium REAL,
    net_delta_notional REAL,
    call_volume_new INTEGER,
    put_volume_new INTEGER,
    avg_iv_change REAL,
    underlying_trend_score REAL,
    top_reason TEXT
);

CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    symbol TEXT NOT NULL,
    direction TEXT,
    score REAL,
    reason TEXT,
    price_at_alert REAL,
    sent INTEGER DEFAULT 0
);
