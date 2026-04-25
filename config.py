import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DEFAULT_WATCHLIST = [
    "SPY", "QQQ", "IWM", "DIA", "XLF", "XLE", "XLK", "XLV", "XLI", "XLP",
    "XLY", "XLU", "XLB", "XLC", "SMH", "SOXX", "TQQQ", "SQQQ", "GLD", "SLV",
    "TLT", "HYG", "LQD", "USO", "EEM", "FXI", "KRE", "ARKK", "VXX", "UVXY",
    "AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "GOOG", "TSLA", "AMD", "AVGO",
    "NFLX", "ORCL", "CRM", "ADBE", "INTC", "CSCO", "QCOM", "AMAT", "MU", "PANW",
    "PLTR", "UBER", "SHOP", "ARM", "ASML", "TXN", "ADI", "LRCX", "KLAC", "MSTR",
    "PYPL", "INTU", "NOW", "SNOW", "CRWD", "DDOG", "MDB", "ZS", "TEAM", "NET",
    "ANET", "APP", "ABNB", "BKNG", "MELI", "PDD", "JD", "BABA", "TMUS", "CMCSA",
    "DIS", "WMT", "COST", "HD", "LOW", "TGT", "SBUX", "MCD", "NKE", "ROST",
    "TJX", "MAR", "CMG", "YUM", "KO", "PEP", "PM", "MO", "PG", "CL",
    "KMB", "GIS", "MDLZ", "KHC", "EL", "JNJ", "ABBV", "MRK", "PFE", "LLY",
    "AMGN", "UNH", "CI", "CVS", "HUM", "ISRG", "TMO", "DHR", "ABT", "MDT",
    "SYK", "BMY", "GILD", "REGN", "VRTX", "BSX", "GE", "CAT", "DE", "HON",
    "UPS", "FDX", "BA", "LMT", "RTX", "NOC", "GD", "ETN", "EMR", "MMM",
    "JPM", "BAC", "WFC", "C", "GS", "MS", "BLK", "SCHW", "CB", "CME",
    "ICE", "SPGI", "MCO", "AXP", "V", "MA", "COF", "TRV", "PGR", "ALL",
    "AIG", "XOM", "CVX", "COP", "OXY", "SLB", "EOG", "MPC", "PSX", "VLO",
    "KMI", "HAL", "FANG", "DVN", "SO", "DUK", "NEE", "AEP", "VZ", "T",
    "AMT", "PLD", "EQIX", "O", "FCX", "NEM", "LIN", "SHW", "APD", "GM",
    "F", "DAL", "UAL", "MRVL", "MCHP", "NXPI", "ON", "MPWR", "MRNA", "BIIB",
]


def parse_watchlist(raw_watchlist: str | None) -> list[str]:
    if not raw_watchlist or not raw_watchlist.strip():
        return DEFAULT_WATCHLIST.copy()
    return [symbol.strip().upper() for symbol in raw_watchlist.split(",") if symbol.strip()]


USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "true").lower() in {"1", "true", "yes"}
WATCHLIST = parse_watchlist(os.getenv("WATCHLIST"))
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
