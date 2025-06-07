import requests

def get_price_binance(symbol: str):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data['price'])
    except Exception as e:
        print(f"Ошибка получения цены с Binance для {symbol}: {e}")
        return None
