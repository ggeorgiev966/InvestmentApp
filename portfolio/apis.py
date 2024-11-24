import requests
from django.http import JsonResponse

LAST_SILVER_PRICE = None
LAST_BITCOIN_PRICE = None
LAST_STOCK_PRICES = {}

def get_silver_price():
    global LAST_SILVER_PRICE
    api_key = "goldapi-btin6sm3artlym-io"
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

        if response.status_code == [429, 403]:
            return LAST_SILVER_PRICE, "API request limit exceeded. API limit reached."
        LAST_SILVER_PRICE = data['price']
        return LAST_SILVER_PRICE, None
    except Exception as e:
        print(f"Error fetching silver price: {e}")
        return LAST_SILVER_PRICE, "Error fetching silver price. API limit reached."


def get_bitcoin_price():
    global LAST_BITCOIN_PRICE
    try:
        url = 'https://api.coindesk.com/v1/bpi/currentprice/USD.json'
        response = requests.get(url)
        if response.status_code == 429:
            return LAST_BITCOIN_PRICE, "API request limit exceeded. Displaying last available price"
        data = response.json()
        LAST_BITCOIN_PRICE = data['bpi']['USD']['rate']
        return LAST_BITCOIN_PRICE, None
    except Exception as e:
        print(f"Error fetching Bitcoin price: {e}")
        return LAST_BITCOIN_PRICE, "Error fetching Bitcoin price. Displaying last available price"


ALPHA_VANTAGE_API_KEY = '84G9TTF1ZLAGSH0B'

def get_stock_price(symbol):
    global LAST_STOCK_PRICES
    try:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}&outputsize=compact'
        response = requests.get(url)
        data = response.json()


        if "Note" in data and "Thank you for using Alpha Vantage!" in data["Note"]:
            last_price = LAST_STOCK_PRICES.get(symbol)
            if last_price:
                return {"current_stock_price": float(last_price), "error": "API limit reached. Displaying last available price."}
            else:
                return {"current_stock_price": 0.0, "error": "API limit reached. No last available price."}


        if "Error Message" in data:
            return {"current_stock_price": 0.0, "error": "Unrecognized ticker."}


        last_refreshed = max(data['Time Series (Daily)'].keys())
        current_price = float(data['Time Series (Daily)'][last_refreshed]['4. close'])


        LAST_STOCK_PRICES[symbol] = current_price

        return {"current_stock_price": current_price, "error": None}
    except Exception as e:
        print(f"Error fetching stock price for {symbol}: {e}")


        last_price = LAST_STOCK_PRICES.get(symbol)
        if last_price:
            return {"current_stock_price": float(last_price), "error": "Error fetching stock price. Displaying last available price."}
        else:
            return {"current_stock_price": 0.0, "error": "Error fetching stock price. API limit reached."}


def last_stock_prices_view(request):
    return JsonResponse(LAST_STOCK_PRICES)
