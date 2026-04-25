def clamp(x, lo=0, hi=100):
    return max(lo, min(hi, x))

def liquidity_score(row: dict) -> float:
    bid = row.get("bid") or 0
    ask = row.get("ask") or 0
    mark = row.get("mark") or 0
    oi = row.get("open_interest") or 0
    vol = row.get("volume") or 0
    spread_pct = row.get("spread_pct") if row.get("spread_pct") is not None else 9
    score = 100
    if bid <= 0 or ask <= 0: score -= 40
    if spread_pct > 0.30: score -= 35
    elif spread_pct > 0.15: score -= 20
    elif spread_pct > 0.08: score -= 10
    if oi < 50: score -= 25
    elif oi < 200: score -= 10
    if vol < 10: score -= 10
    if mark < 0.05: score -= 20
    return clamp(score)
