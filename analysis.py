def generate_signal(data):
    try:
        close_prices = [float(item["close"]) for item in data[:10]]
        avg_price = sum(close_prices) / len(close_prices)
        last_price = float(data[0]["close"])

        if last_price > avg_price:
            return "🟢 Сигнал на ПОКУПКУ"
        elif last_price < avg_price:
            return "🔴 Сигнал на ПРОДАЖУ"
        else:
            return "🟡 Нет сигнала"

    except Exception as e:
        return f"Ошибка анализа данных: {e}"