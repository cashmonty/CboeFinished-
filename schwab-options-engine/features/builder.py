from features.liquidity import liquidity_score, clamp

def dte_quality(dte):
    if dte is None: return 0
    if 14 <= dte <= 45: return 100
    if 7 <= dte < 14 or 46 <= dte <= 75: return 75
    if 1 <= dte < 7: return 45
    return 20

def delta_quality(delta):
    d = abs(delta or 0)
    if 0.35 <= d <= 0.60: return 100
    if 0.25 <= d < 0.35 or 0.60 < d <= 0.75: return 75
    if 0.15 <= d < 0.25: return 45
    return 20

def activity_score(new_volume, premium, delta_notional, volume_oi, iv_change):
    score = 0
    if new_volume >= 1000: score += 25
    elif new_volume >= 500: score += 20
    elif new_volume >= 100: score += 12
    elif new_volume >= 25: score += 6
    if premium >= 1_000_000: score += 25
    elif premium >= 500_000: score += 20
    elif premium >= 100_000: score += 12
    elif premium >= 25_000: score += 6
    if delta_notional >= 500_000: score += 15
    elif delta_notional >= 100_000: score += 10
    elif delta_notional >= 25_000: score += 5
    if volume_oi >= 2: score += 15
    elif volume_oi >= 1: score += 10
    elif volume_oi >= 0.5: score += 5
    if iv_change is not None:
        if iv_change >= 3: score += 15
        elif iv_change >= 1: score += 8
        elif iv_change < -2: score -= 10
    return clamp(score)

def build_features(current_rows, previous_by_symbol):
    features = []
    for row in current_rows:
        prev = previous_by_symbol.get(row["option_symbol"])
        prev_vol = prev.get("volume", 0) if prev else 0
        prev_iv = prev.get("iv") if prev else None
        prev_mark = prev.get("mark") if prev else None
        new_volume = max((row.get("volume") or 0) - (prev_vol or 0), 0)
        mark = row.get("mark") or 0
        delta = row.get("delta") or 0
        oi = row.get("open_interest") or 0
        premium = new_volume * mark * 100
        delta_notional = premium * abs(delta)
        volume_oi = (row.get("volume") or 0) / max(oi, 1)
        iv_change = (row.get("iv") - prev_iv) if prev_iv is not None and row.get("iv") is not None else None
        mark_change = (mark - prev_mark) if prev_mark is not None else None
        liq = liquidity_score(row)
        act = activity_score(new_volume, premium, delta_notional, volume_oi, iv_change)
        contract_score = 0.35 * act + 0.25 * liq + 0.20 * dte_quality(row.get("dte")) + 0.20 * delta_quality(delta)
        features.append({
            "ts": row["ts"], "underlying": row["underlying"], "option_symbol": row["option_symbol"],
            "put_call": row["put_call"], "expiration": row["expiration"], "dte": row["dte"], "strike": row["strike"],
            "new_volume": new_volume, "premium_estimate": premium, "delta_notional": delta_notional,
            "volume_oi": volume_oi, "iv_change": iv_change, "mark_change": mark_change,
            "spread_pct": row.get("spread_pct"), "moneyness": row.get("moneyness"),
            "liquidity_score": liq, "activity_score": act, "contract_score": round(contract_score, 2)
        })
    return features
