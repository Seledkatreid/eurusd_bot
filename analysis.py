import requests
import pandas as pd
from datetime import datetime, timedelta
import os

API_KEY = os.getenv("API_KEY") or '8715cc7afe1745758b4668cd5cffe3d0'
PAIR = 'EUR/USD'
INTERVAL = '1min'

def calculate_expiry(minutes):
    expiry_time = datetime.now() + timedelta(minutes=minutes)
    return expiry_time.strftime("%H:%M")

def analyze_signal():
    rsi_url = f"https://api.twelvedata.com/rsi?symbol=EURUSD&interval={INTERVAL}&apikey={API_KEY}&time_period=14"
    bb_url = f"https://api.twelvedata.com/bbands?symbol=EURUSD&interval={INTERVAL}&apikey={API_KEY}&time_period=20&stddev=2"

    rsi_response = requests.get(rsi_url)
    bb_response = requests.get(bb_url)

    if rsi_response.status_code != 200 or bb_response.status_code != 200:
        return "❌ Ошибка получения данных от API."

    try:
        rsi = float(rsi_response.json()['values'][0]['rsi'])
        bb = bb_response.json()['values'][0]
        upper = float(bb['upper_band'])
        lower = float(bb['lower_band'])
        close = float(bb['close'])
    except Exception as e:
        return f"❌ Ошибка обработки данных: {e}"

    signal_time = datetime.now().strftime("%H:%M")
    direction = None
    level = "⚠️ СРЕДНИЙ"

    expiry_minutes = 3

    if rsi < 25 and close <= lower:
        direction = "🟢 Сигнал на ПОКУПКУ"

        if rsi < 20:
            level = "🟢 СИЛЬНЫЙ"

            expiry_minutes = 5
        elif rsi < 23:
            level = "🟢 УВЕРЕННЫЙ"

            expiry_minutes = 4

    elif rsi > 75 and close >= upper:
        direction = "🔴 Сигнал на ПРОДАЖУ"

        if rsi > 80:
            level = "🔴 СИЛЬНЫЙ"

            expiry_minutes = 5
        elif rsi > 77:
            level = "🔴 УВЕРЕННЫЙ"

            expiry_minutes = 4

    if direction:
        expiry_time = calculate_expiry(expiry_minutes)
        return f"{direction}" \

               f"\nRSI: {rsi:.2f}" \

               f"\nЦена закрытия: {close:.5f}" \

               f"\nВерхняя BB: {upper:.5f}" \

               f"\nНижняя BB: {lower:.5f}" \

               f"\nЭкспирация до: {expiry_time}" \

               f"\nСила сигнала: {level}" \

               f"\nВремя сигнала: {signal_time}"

    else:

        return "Нет сигнала: условия RSI и BB не совпадают."