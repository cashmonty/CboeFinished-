import random
from datetime import datetime, timedelta, timezone

BASE_PRICES = {
    "SPY": 520, "QQQ": 440, "NVDA": 900, "TSLA": 180, "AMD": 165,
    "AAPL": 185, "MSFT": 420, "META": 500, "AMZN": 185, "GOOGL": 160,
}
_counter = 0

def mock_chain(symbol: str) -> dict:
    global _counter
    _counter += 1
    spot = BASE_PRICES.get(symbol.upper(), 100) * (1 + random.uniform(-0.006, 0.006))
    today = datetime.now(timezone.utc).date()
    call_map, put_map = {}, {}

    for dte in [3, 7, 14, 21, 35, 49]:
        exp = today + timedelta(days=dte)
        exp_key = f"{exp.isoformat()}:{dte}"
        call_map[exp_key] = {}
        put_map[exp_key] = {}
        for i in range(-10, 11):
            strike = round((spot * (1 + i * 0.015)) / 5) * 5
            for side, target in [("CALL", call_map), ("PUT", put_map)]:
                intrinsic = max(0, spot - strike) if side == "CALL" else max(0, strike - spot)
                extrinsic = max(0.15, abs(i) * 0.10 + (60 - dte) * 0.03 + random.random())
                mark = round(intrinsic + extrinsic, 2)
                bid = max(0.01, round(mark * 0.96, 2))
                ask = round(mark * 1.04 + 0.02, 2)
                base_vol = max(0, int(1000 / (abs(i) + 2) + random.randint(0, 50)))
                volume = base_vol + _counter * random.randint(0, 10)
                oi = max(10, int(2000 / (abs(i) + 1) + random.randint(0, 500)))
                delta = (0.5 - i * 0.035) if side == "CALL" else -(0.5 + i * 0.035)
                delta = max(-0.95, min(0.95, delta))
                contract = {
                    "symbol": f"{symbol}_{exp.isoformat()}_{side[0]}_{strike}",
                    "putCall": side,
                    "strikePrice": strike,
                    "bid": bid,
                    "ask": ask,
                    "mark": mark,
                    "last": mark,
                    "totalVolume": volume,
                    "openInterest": oi,
                    "volatility": round(35 + random.uniform(-5, 5), 2),
                    "delta": round(delta, 3),
                    "gamma": round(random.uniform(0.002, 0.04), 4),
                    "theta": round(random.uniform(-0.25, -0.01), 4),
                    "vega": round(random.uniform(0.01, 0.25), 4),
                    "rho": round(random.uniform(-0.05, 0.05), 4),
                }
                target[exp_key].setdefault(str(strike), []).append(contract)

    return {
        "symbol": symbol,
        "underlyingPrice": spot,
        "underlying": {"symbol": symbol, "last": spot, "mark": spot},
        "callExpDateMap": call_map,
        "putExpDateMap": put_map,
    }
