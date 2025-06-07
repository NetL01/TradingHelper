import requests

def get_price_coingecko(coin_id: str):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data[coin_id]['usd']
    except Exception as e:
        print(f"Ошибка получения цены с CoinGecko для {coin_id}: {e}")
        return None
