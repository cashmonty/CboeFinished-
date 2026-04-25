import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "true").lower() in {"1", "true", "yes"}
WATCHLIST = [s.strip().upper() for s in os.getenv("WATCHLIST", "SPY,QQQ,NVDA,TSLA").split(",") if s.strip()]
POLL_SECONDS = int(os.getenv("POLL_SECONDS", "60"))
DB_PATH = os.getenv("DB_PATH", str(DATA_DIR / "options_engine.sqlite"))
STRIKE_COUNT = int(os.getenv("STRIKE_COUNT", "40"))
DTE_MAX = int(os.getenv("DTE_MAX", "60"))

SCHWAB_APP_KEY = os.getenv("SCHWAB_APP_KEY", "")
SCHWAB_APP_SECRET = os.getenv("SCHWAB_APP_SECRET", "")
SCHWAB_CALLBACK_URL = os.getenv("SCHWAB_CALLBACK_URL", "https://127.0.0.1")
SCHWAB_TOKEN_PATH = os.getenv("SCHWAB_TOKEN_PATH", "./tokens/schwab_token.json")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
MIN_ALERT_SCORE = float(os.getenv("MIN_ALERT_SCORE", "80"))
MIN_ALERT_PREMIUM = float(os.getenv("MIN_ALERT_PREMIUM", "250000"))
ALERT_COOLDOWN_MINUTES = int(os.getenv("ALERT_COOLDOWN_MINUTES", "30"))
