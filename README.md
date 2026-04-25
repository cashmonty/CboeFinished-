# Schwab Options Positioning + Volatility Imbalance Engine

A Python MVP that uses Schwab option-chain market data snapshots to estimate fresh options activity, score bullish/bearish positioning, send optional Telegram alerts, and log everything to SQLite for research/backtesting.

This is a snapshot-based engine designed around option chains, volume deltas, IV changes, Greeks, liquidity filters, and underlying confirmation.

## Features

- Schwab option-chain collector via `schwab-py`
- Mock data mode so you can test before Schwab auth is working
- SQLite database with option snapshots, features, ticker scores, and alerts
- Fresh volume from snapshot diffs
- Premium estimate and delta-notional estimate
- Liquidity, DTE, delta, and activity scoring
- Bullish/bearish ticker aggregation
- Optional Telegram alerts
- Streamlit dashboard

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

If `WATCHLIST` is left blank, the app uses a built-in 200-name liquid universe
covering major U.S. ETFs and large-cap option names.

## Run with mock data first

```powershell
$env:USE_MOCK_DATA="true"
$env:POLL_SECONDS="0"
python app.py
```

## Run live with Schwab

Edit `.env`:

```env
SCHWAB_APP_KEY=your_key
SCHWAB_APP_SECRET=your_secret
SCHWAB_CALLBACK_URL=https://127.0.0.1
SCHWAB_TOKEN_PATH=./tokens/schwab_token.json
USE_MOCK_DATA=false
POLL_SECONDS=60
```

Then:

```powershell
python app.py
```

## Dashboard

```powershell
streamlit run dashboard/streamlit_app.py
```

## Push to your GitHub repo

```powershell
git remote add origin https://github.com/cashmonty/CboeFinished-.git
git branch -M main
git push -u origin main
```

If remote already exists:

```powershell
git remote set-url origin https://github.com/cashmonty/CboeFinished-.git
git branch -M main
git push -u origin main
```

## Notes

Schwab wrapper signatures can vary by `schwab-py` version and your approved developer product. If the Schwab call fails, edit only:

```text
collectors/schwab_chains.py
```
