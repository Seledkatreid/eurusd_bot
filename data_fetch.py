import requests
from config import API_KEY, SYMBOL, BASE_URL

def fetch_data(interval):
    params = {
        "symbol": SYMBOL,
        "interval": interval,
        "apikey": API_KEY,
        "outputsize": 30
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "values" not in data:
        return None, f"Ошибка получения данных: {data.get('message', data)}"
    
    return data["values"], None