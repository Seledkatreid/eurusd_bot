import requests
import pandas as pd
from config import API_KEY, SYMBOL, INTERVAL, BASE_URL

def fetch_data():
    params = {
        "function": "FX_INTRADAY",
        "from_symbol": SYMBOL.split('/')[0],
        "to_symbol": SYMBOL.split('/')[1],
        "interval": INTERVAL,
        "apikey": API_KEY,
        "outputsize": "compact"
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "Time Series FX (" + INTERVAL + ")" not in data:
        raise Exception("Ошибка получения данных: " + str(data))

    ts_data = data["Time Series FX (" + INTERVAL + ")"]
    records = []
    for time, values in ts_data.items():
        records.append({
            "datetime": time,
            "close": float(values["4. close"])
        })
    records.sort(key=lambda x: x["datetime"])
    return records