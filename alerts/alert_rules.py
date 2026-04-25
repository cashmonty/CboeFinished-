from config import MIN_ALERT_SCORE, MIN_ALERT_PREMIUM

def decide_alert(score: dict):
    bull = score.get("bullish_score") or 0
    bear = score.get("bearish_score") or 0
    call_premium = score.get("call_premium") or 0
    put_premium = score.get("put_premium") or 0
    if bull >= MIN_ALERT_SCORE and call_premium >= MIN_ALERT_PREMIUM and bull - bear >= 10:
        return True, "BULLISH", bull, "Bullish options positioning score crossed threshold"
    if bear >= MIN_ALERT_SCORE and put_premium >= MIN_ALERT_PREMIUM and bear - bull >= 10:
        return True, "BEARISH", bear, "Bearish options positioning score crossed threshold"
    return False, "", 0, ""

def format_alert(symbol: str, direction: str, score_value: float, reason: str, score: dict, features: list[dict]) -> str:
    top = sorted(features, key=lambda f: f.get("contract_score") or 0, reverse=True)[:5]
    lines = [
        f"{symbol} {direction} Options Alert — Score {score_value:.1f}",
        "",
        f"Reason: {reason}",
        f"Call premium estimate: ${score.get('call_premium', 0):,.0f}",
        f"Put premium estimate: ${score.get('put_premium', 0):,.0f}",
        f"Net delta notional: ${score.get('net_delta_notional', 0):,.0f}",
        f"New call volume: {score.get('call_volume_new', 0):,}",
        f"New put volume: {score.get('put_volume_new', 0):,}",
        "",
        "Top contracts:",
    ]
    for f in top:
        lines.append(f"- {f['option_symbol']} | score {f['contract_score']} | new vol {f['new_volume']} | prem ${f['premium_estimate']:,.0f}")
    return "\n".join(lines)
