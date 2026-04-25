import time
from datetime import datetime, timezone

from auth.schwab_auth import create_schwab_client
from collectors.schwab_chains import fetch_option_chain
from normalizers.option_chain_normalizer import flatten_option_chain
from storage.db import init_db
from storage.repositories import (
    save_option_snapshots,
    get_previous_snapshots,
    save_contract_features,
    save_ticker_score,
    save_alert,
)
from features.builder import build_features
from scoring.ticker_score import aggregate_ticker_score
from alerts.alert_rules import decide_alert, format_alert
from alerts.telegram import send_telegram_alert
from config import WATCHLIST, POLL_SECONDS

def run_once(client):
    ts = datetime.now(timezone.utc).isoformat()
    all_scores = []
    for symbol in WATCHLIST:
        try:
            previous = get_previous_snapshots(symbol)
            raw = fetch_option_chain(client, symbol)
            rows = flatten_option_chain(raw, symbol, ts)
            if not rows:
                print(f"[{symbol}] No chain rows returned")
                continue
            save_option_snapshots(rows)
            features = build_features(rows, previous)
            save_contract_features(features)
            ticker_score = aggregate_ticker_score(features, underlying_trend_score=50)
            save_ticker_score(symbol, ts, ticker_score)
            all_scores.append((symbol, ticker_score))
            should, direction, score_val, reason = decide_alert(ticker_score)
            if should:
                msg = format_alert(symbol, direction, score_val, reason, ticker_score, features)
                sent = send_telegram_alert(msg)
                save_alert(symbol, ts, direction, {"score": score_val, **ticker_score}, reason, sent=int(sent))
            print(f"[{symbol}] bull={ticker_score['bullish_score']:.1f} bear={ticker_score['bearish_score']:.1f} callPrem=${ticker_score['call_premium']:,.0f} putPrem=${ticker_score['put_premium']:,.0f}")
        except Exception as exc:
            print(f"[ERROR] {symbol}: {exc}")
    return all_scores

def main():
    init_db()
    client = create_schwab_client()
    print(f"Starting engine. Watchlist={WATCHLIST}. POLL_SECONDS={POLL_SECONDS}")
    while True:
        run_once(client)
        if POLL_SECONDS <= 0:
            break
        time.sleep(POLL_SECONDS)

if __name__ == "__main__":
    main()
