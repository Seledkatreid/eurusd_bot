import requests
import pandas as pd
import os

def analyze_signal():
    API_KEY = os.getenv("API_KEY")
    url = f"https://api.twelvedata.com/time_series?symbol=EUR/USD&interval=1min&apikey={API_KEY}&outputsize=50"
    response = requests.get(url)
    if response.status_code != 200 or not response.text.strip():
        return "❌ Ошибка при получении данных от Twelve Data."
    data = response.json()
    if "values" not in data:
        return "❌ Нет данных в ответе API."

    df = pd.DataFrame(data["values"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.sort_values("datetime")
    df.set_index("datetime", inplace=True)
    df = df.astype(float)

    df["change"] = df["close"] - df["close"].shift(1)
    df["gain"] = df["change"].apply(lambda x: x if x > 0 else 0)
    df["loss"] = df["change"].apply(lambda x: -x if x < 0 else 0)
    avg_gain = df["gain"].rolling(window=14).mean()
    avg_loss = df["loss"].rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["rsi"] = 100 - (100 / (1 + rs))

    # Bollinger Bands
    df["ma20"] = df["close"].rolling(window=20).mean()
    df["std20"] = df["close"].rolling(window=20).std()
    df["upper_bb"] = df["ma20"] + 2 * df["std20"]
    df["lower_bb"] = df["ma20"] - 2 * df["std20"]

    last = df.iloc[-1]

    message = f"📉 RSI: {last['rsi']:.2f}\n📊 BB: Верхняя {last['upper_bb']:.5f}, Нижняя {last['lower_bb']:.5f}\n"

    signal = "❌ Сигналов нет"

    if last["rsi"] > 75 and last["close"] < last["upper_bb"]:
        signal = "🔴 Сигнал на ПРОДАЖУ"
    elif last["rsi"] < 25 and last["close"] > last["lower_bb"]:
        signal = "🟢 Сигнал на ПОКУПКУ"

    return f"{signal}\n{message}"