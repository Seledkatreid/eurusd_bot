def analyze_data(data):
    if not data or len(data) < 2:
        return "Недостаточно данных для анализа."
    close_prices = [float(item["close"]) for item in data[:5]]
    avg = sum(close_prices) / len(close_prices)
    last_price = float(data[0]["close"])
    if last_price > avg:
        return "Сигнал на ПОКУПКУ 🚀"
    elif last_price < avg:
        return "Сигнал на ПРОДАЖУ 📉"
    else:
        return "Сигналов нет."