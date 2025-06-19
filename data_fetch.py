import requests
import pandas as pd
from config import API_KEY, SYMBOL, INTERVAL

def fetch_data():
    url = f"https://api.twelvedata.com/time_series?symbol={SYMBOL}&interval={INTERVAL}&apikey={API_KEY}&outputsize=50"
    response = requests.get(url)
    data = response.json()
    if "values" not in data:
        raise Exception("Ошибка загрузки данных")
    df = pd.DataFrame(data["values"])
    df = df.iloc[::-1].reset_index(drop=True)
    df["close"] = df["close"].astype(float)
    return df