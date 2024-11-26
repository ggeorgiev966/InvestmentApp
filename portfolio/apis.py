import requests
from portfolio.models import LastAvailablePrice
from decimal import Decimal
import os


def get_last_available_price(symbol):
    last_price = LastAvailablePrice.objects.filter(symbol=symbol).first()
    return float(last_price.price) if last_price else 0.0


def get_silver_price():
    api_key = os.getenv("GOLDAPI_KEY")
    symbol = "XAG"
    curr = "USD"
    date = ""

    url = f"https://www.goldapi.io/api/{symbol}/{curr}{date}"

    headers = {
        "x-access-token": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        price = data.get('price')
        if price is None:
            raise ValueError("Price not found in response")

        last_price, created = LastAvailablePrice.objects.update_or_create(
            symbol="silver",
            defaults={"price": Decimal(price)}
        )
        return price, None
    except Exception as e:
        print(f"Error fetching silver price: {e}")
        last_price = get_last_available_price("silver")
        return last_price, "Error fetching silver price. API request limit exceeded. Displaying last available price."


def get_bitcoin_price():
    try:
        url = 'https://api.coindesk.com/v1/bpi/currentprice/USD.json'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if response.status_code == 429:
            last_price = get_last_available_price("bitcoin")
            return last_price, "API request limit exceeded. Displaying last available price."

        price = data['bpi']['USD']['rate'].replace(',', '')
        last_price, created = LastAvailablePrice.objects.update_or_create(
            symbol="bitcoin",
            defaults={"price": Decimal(price)}
        )
        return float(price), None
    except Exception as e:
        print(f"Error fetching Bitcoin price: {e}")
        last_price = get_last_available_price("bitcoin")
        return last_price, "Error fetching Bitcoin price. Displaying last available price."


ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')


def get_stock_price(symbol):
    try:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}&outputsize=compact'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "Note" in data and "Thank you for using Alpha Vantage!" in data["Note"]:
            last_price = get_last_available_price(symbol)
            return {"current_stock_price": last_price, "error": "API limit reached. Displaying last available price."}

        if "Error Message" in data:
            return {"current_stock_price": 0.0, "error": "Unrecognized ticker."}

        last_refreshed = max(data['Time Series (Daily)'].keys())
        current_price = float(data['Time Series (Daily)'][last_refreshed]['4. close'])

        last_price, created = LastAvailablePrice.objects.update_or_create(
            symbol=symbol,
            defaults={"price": Decimal(current_price)}
        )
        return {"current_stock_price": current_price, "error": None}
    except Exception as e:
        print(f"Error fetching stock price for {symbol}: {e}")
        last_price = get_last_available_price(symbol)
        return {"current_stock_price": last_price,
                "error": "Error fetching stock price. API request limit exceeded. Displaying last available price."}
