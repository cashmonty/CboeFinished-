from datetime import datetime, timezone

def safe_float(x, default=None):
    try:
        if x is None or x == "":
            return default
        return float(x)
    except Exception:
        return default

def safe_int(x, default=0):
    try:
        if x is None or x == "":
            return default
        return int(float(x))
    except Exception:
        return default

def midpoint(bid, ask):
    if bid is not None and ask is not None and bid > 0 and ask > 0:
        return (bid + ask) / 2
    return None

def calc_spread_pct(bid, ask, mid):
    if bid is None or ask is None or not mid or mid <= 0:
        return None
    return max(0, (ask - bid) / mid)

def calc_moneyness(underlying_price, strike):
    if not underlying_price or not strike:
        return None
    return strike / underlying_price

def parse_exp_key(exp_key: str):
    parts = str(exp_key).split(":")
    expiration = parts[0]
    dte = safe_int(parts[1], None) if len(parts) > 1 else None
    if dte is None:
        try:
            dte = (datetime.fromisoformat(expiration).date() - datetime.now(timezone.utc).date()).days
        except Exception:
            dte = None
    return expiration, dte

def extract_underlying_price(raw_chain: dict):
    for path in [
        ("underlyingPrice",),
        ("underlying", "last"),
        ("underlying", "mark"),
    ]:
        cur = raw_chain
        try:
            for p in path:
                cur = cur[p]
            val = safe_float(cur)
            if val:
                return val
        except Exception:
            pass
    return None

def flatten_option_chain(raw_chain: dict, underlying: str, ts: str):
    rows = []
    underlying_price = extract_underlying_price(raw_chain)

    for side_key in ["callExpDateMap", "putExpDateMap"]:
        put_call = "CALL" if side_key == "callExpDateMap" else "PUT"
        exp_map = raw_chain.get(side_key, {}) or {}
        for exp_key, strikes in exp_map.items():
            expiration, dte = parse_exp_key(exp_key)
            for strike_str, contracts in (strikes or {}).items():
                for c in contracts or []:
                    bid = safe_float(c.get("bid"))
                    ask = safe_float(c.get("ask"))
                    mark = safe_float(c.get("mark")) or safe_float(c.get("last")) or midpoint(bid, ask)
                    last = safe_float(c.get("last"))
                    strike = safe_float(c.get("strikePrice"), safe_float(strike_str))
                    spread_pct = calc_spread_pct(bid, ask, mark)
                    rows.append({
                        "ts": ts,
                        "underlying": underlying.upper(),
                        "option_symbol": c.get("symbol"),
                        "put_call": c.get("putCall", put_call),
                        "expiration": expiration,
                        "dte": dte,
                        "strike": strike,
                        "bid": bid,
                        "ask": ask,
                        "mark": mark,
                        "last": last,
                        "volume": safe_int(c.get("totalVolume", c.get("volume"))),
                        "open_interest": safe_int(c.get("openInterest")),
                        "iv": safe_float(c.get("volatility", c.get("iv"))),
                        "delta": safe_float(c.get("delta")),
                        "gamma": safe_float(c.get("gamma")),
                        "theta": safe_float(c.get("theta")),
                        "vega": safe_float(c.get("vega")),
                        "rho": safe_float(c.get("rho")),
                        "underlying_price": underlying_price,
                        "spread_pct": spread_pct,
                        "moneyness": calc_moneyness(underlying_price, strike),
                    })
    return rows
