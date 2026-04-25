from datetime import date, timedelta
from config import USE_MOCK_DATA, STRIKE_COUNT, DTE_MAX
from collectors.mock_data import mock_chain

def fetch_option_chain(client, symbol: str) -> dict:
    """Fetch an option chain from Schwab or mock data.

    This wrapper intentionally isolates Schwab API variation. If your client method
    signature differs, update only this file.
    """
    if USE_MOCK_DATA:
        return mock_chain(symbol)

    today = date.today()
    to_date = today + timedelta(days=DTE_MAX)

    try:
        resp = client.get_option_chain(
            symbol=symbol,
            contract_type="ALL",
            strike_count=STRIKE_COUNT,
            include_underlying_quote=True,
            from_date=today,
            to_date=to_date,
            strategy="SINGLE",
        )
    except TypeError:
        resp = client.get_option_chain(symbol=symbol)

    if hasattr(resp, "json"):
        return resp.json()
    return resp
