def calculate_rsi(prices, period):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def generate_signal(df, period, oversold, overbought):
    rsi = calculate_rsi(df["close"], period)
    latest_rsi = rsi.iloc[-1]

    if latest_rsi < 25:
        level = "💥 ОЧЕНЬ СИЛЬНЫЙ"
        expiration = "5 минут"
        signal = "🟢 Сигнал на ПОКУПКУ"
    elif latest_rsi < oversold:
        level = "⚠️ СРЕДНИЙ"
        expiration = "3 минуты"
        signal = "🟢 Сигнал на ПОКУПКУ"
    elif latest_rsi < 40:
        level = "⚠️ СЛАБЫЙ"
        expiration = "1 минута"
        signal = "🟢 Сигнал на ПОКУПКУ"
    elif latest_rsi > 75:
        level = "💥 ОЧЕНЬ СИЛЬНЫЙ"
        expiration = "5 минут"
        signal = "🔴 Сигнал на ПРОДАЖУ"
    elif latest_rsi > overbought:
        level = "⚠️ СРЕДНИЙ"
        expiration = "3 минуты"
        signal = "🔴 Сигнал на ПРОДАЖУ"
    elif latest_rsi > 60:
        level = "⚠️ СЛАБЫЙ"
        expiration = "1 минута"
        signal = "🔴 Сигнал на ПРОДАЖУ"
    else:
        return f"🟡 Нет чёткого сигнала\nRSI: {latest_rsi:.2f}"

    return f"{signal}\nRSI: {latest_rsi:.2f}\nЭкспирация: {expiration}\nУровень сигнала: {level}"