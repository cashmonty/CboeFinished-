from pathlib import Path
from config import SCHWAB_APP_KEY, SCHWAB_APP_SECRET, SCHWAB_CALLBACK_URL, SCHWAB_TOKEN_PATH, USE_MOCK_DATA

class MockSchwabClient:
    pass

def create_schwab_client():
    """Create a Schwab client using schwab-py."""
    if USE_MOCK_DATA:
        return MockSchwabClient()

    if not SCHWAB_APP_KEY or not SCHWAB_APP_SECRET:
        raise RuntimeError("Missing SCHWAB_APP_KEY or SCHWAB_APP_SECRET in .env")

    try:
        from schwab.auth import easy_client
    except Exception as exc:
        raise RuntimeError("Could not import schwab-py. Run: pip install schwab-py") from exc

    token_path = Path(SCHWAB_TOKEN_PATH)
    token_path.parent.mkdir(parents=True, exist_ok=True)

    return easy_client(
        api_key=SCHWAB_APP_KEY,
        app_secret=SCHWAB_APP_SECRET,
        callback_url=SCHWAB_CALLBACK_URL,
        token_path=str(token_path),
    )
