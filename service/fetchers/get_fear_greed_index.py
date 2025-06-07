import requests


def get_fear_greed_index():
    url = "https://api.alternative.me/fng/"
    try:
        response = requests.get(url)
        data = response.json()
        value = data['data'][0]['value']
        classification = data['data'][0]['value_classification']
        return f"😨 *Fear & Greed Index:* {value} ({classification})"
    except Exception as e:
        print("Ошибка получения Fear & Greed Index:", e)
        return "⚠️ Fear & Greed Index недоступен"