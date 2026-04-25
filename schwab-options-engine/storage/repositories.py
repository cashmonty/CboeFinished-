from storage.db import get_conn

SNAP_COLS = [
    "ts","underlying","option_symbol","put_call","expiration","dte","strike","bid","ask","mark","last",
    "volume","open_interest","iv","delta","gamma","theta","vega","rho","underlying_price","spread_pct","moneyness"
]
FEAT_COLS = [
    "ts","underlying","option_symbol","put_call","expiration","dte","strike","new_volume","premium_estimate",
    "delta_notional","volume_oi","iv_change","mark_change","spread_pct","moneyness","liquidity_score","activity_score","contract_score"
]

def save_option_snapshots(rows):
    if not rows: return
    placeholders = ",".join([":"+c for c in SNAP_COLS])
    with get_conn() as conn:
        conn.executemany(f"INSERT INTO option_snapshots ({','.join(SNAP_COLS)}) VALUES ({placeholders})", rows)
        conn.commit()

def get_previous_snapshots(symbol):
    with get_conn() as conn:
        ts_row = conn.execute("SELECT MAX(ts) AS ts FROM option_snapshots WHERE underlying=?", (symbol.upper(),)).fetchone()
        if not ts_row or not ts_row["ts"]: return {}
        rows = conn.execute("SELECT * FROM option_snapshots WHERE underlying=? AND ts=?", (symbol.upper(), ts_row["ts"])).fetchall()
    return {r["option_symbol"]: dict(r) for r in rows}

def save_contract_features(rows):
    if not rows: return
    placeholders = ",".join([":"+c for c in FEAT_COLS])
    with get_conn() as conn:
        conn.executemany(f"INSERT INTO contract_features ({','.join(FEAT_COLS)}) VALUES ({placeholders})", rows)
        conn.commit()

def save_ticker_score(symbol, ts, score):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO ticker_scores
            (ts,symbol,bullish_score,bearish_score,call_premium,put_premium,net_delta_notional,call_volume_new,put_volume_new,avg_iv_change,underlying_trend_score,top_reason)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (ts, symbol.upper(), score.get("bullish_score"), score.get("bearish_score"), score.get("call_premium"), score.get("put_premium"),
             score.get("net_delta_notional"), score.get("call_volume_new"), score.get("put_volume_new"), score.get("avg_iv_change"),
             score.get("underlying_trend_score"), score.get("top_reason"))
        )
        conn.commit()

def save_alert(symbol, ts, direction, score, reason, sent=1):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO alerts (ts,symbol,direction,score,reason,price_at_alert,sent) VALUES (?,?,?,?,?,?,?)",
            (ts, symbol.upper(), direction, score.get("score"), reason, score.get("underlying_price"), sent)
        )
        conn.commit()
