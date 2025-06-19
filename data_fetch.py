
import requests
from config import API_KEY, SYMBOL, INTERVAL, BASE_URL

def get_price_data():
    params = {
        'symbol': SYMBOL,
        'interval': INTERVAL,
        'apikey': API_KEY,
        'outputsize': 100
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    if 'values' in data:
        return data['values']
    else:
        return []
