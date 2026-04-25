def avg(vals):
    vals = [v for v in vals if v is not None]
    return sum(vals) / len(vals) if vals else 0

def normalize_money(x):
    return min(100, (x or 0) / 1_000_000 * 100)

def normalize_iv(x):
    return max(0, min(100, 50 + (x or 0) * 16.67))

def avg_top_scores(rows, n=10):
    scores = sorted([(r.get("contract_score") or 0) for r in rows], reverse=True)[:n]
    return avg(scores)

def aggregate_ticker_score(features, underlying_trend_score=50):
    calls = [f for f in features if str(f.get("put_call")).upper() == "CALL"]
    puts = [f for f in features if str(f.get("put_call")).upper() == "PUT"]
    call_premium = sum(f.get("premium_estimate") or 0 for f in calls)
    put_premium = sum(f.get("premium_estimate") or 0 for f in puts)
    call_delta = sum(f.get("delta_notional") or 0 for f in calls)
    put_delta = sum(f.get("delta_notional") or 0 for f in puts)
    call_iv = avg([f.get("iv_change") for f in calls])
    put_iv = avg([f.get("iv_change") for f in puts])
    call_quality = avg_top_scores(calls)
    put_quality = avg_top_scores(puts)
    bullish = 0.30*normalize_money(call_premium) + 0.20*normalize_money(call_delta) + 0.20*call_quality + 0.15*normalize_iv(call_iv) + 0.15*underlying_trend_score
    bearish = 0.30*normalize_money(put_premium) + 0.20*normalize_money(put_delta) + 0.20*put_quality + 0.15*normalize_iv(put_iv) + 0.15*(100-underlying_trend_score)
    top_reason = f"Call prem ${call_premium:,.0f}, Put prem ${put_premium:,.0f}, top call quality {call_quality:.1f}, top put quality {put_quality:.1f}"
    return {
        "bullish_score": round(min(100, bullish), 2),
        "bearish_score": round(min(100, bearish), 2),
        "call_premium": round(call_premium, 2),
        "put_premium": round(put_premium, 2),
        "net_delta_notional": round(call_delta - put_delta, 2),
        "call_volume_new": sum(f.get("new_volume") or 0 for f in calls),
        "put_volume_new": sum(f.get("new_volume") or 0 for f in puts),
        "avg_iv_change": round(avg([call_iv, put_iv]), 4),
        "underlying_trend_score": underlying_trend_score,
        "top_reason": top_reason,
        "underlying_price": None,
    }
