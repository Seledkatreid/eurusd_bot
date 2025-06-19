import requests
from config import API_KEY, SYMBOL

def fetch_data(interval):
    url = f"https://api.twelvedata.com/time_series?symbol={SYMBOL}&interval={interval}&apikey={API_KEY}&outputsize=30"
    response = requests.get(url)
    data = response.json()
    if "values" in data:
        return data["values"]
    else:
        raise Exception(f"Ошибка получения данных: {data}")