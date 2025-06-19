
import pandas as pd
import ta

def analyze(data):
    df = pd.DataFrame(data)
    df = df.rename(columns={'datetime': 'time', 'close': 'close'})
    df['close'] = df['close'].astype(float)
    df = df.sort_values('time')

    df['ema_fast'] = ta.trend.ema_indicator(df['close'], window=5, fillna=True)
    df['ema_slow'] = ta.trend.ema_indicator(df['close'], window=21, fillna=True)
    df['rsi'] = ta.momentum.rsi(df['close'], window=14, fillna=True)
    df['macd'] = ta.trend.macd(df['close'], window_slow=26, window_fast=12, fillna=True)
    df['macd_signal'] = ta.trend.macd_signal(df['close'], window_slow=26, window_fast=12, window_sign=9, fillna=True)

    df['diff'] = df['close'].diff().abs()
    avg_volatility = df['diff'].tail(10).mean()
    pip_size = 0.0001
    avg_pips_per_minute = avg_volatility / pip_size if avg_volatility else 1

    last = df.iloc[-1]

    signal = None
    if last['ema_fast'] > last['ema_slow'] and last['rsi'] < 70 and last['macd'] > last['macd_signal']:
        signal = 'BUY'
    elif last['ema_fast'] < last['ema_slow'] and last['rsi'] > 30 and last['macd'] < last['macd_signal']:
        signal = 'SELL'

    if signal:
        entry = last['close']
        tp = round(entry + 0.0010, 5) if signal == 'BUY' else round(entry - 0.0010, 5)
        sl = round(entry - 0.0050, 5) if signal == 'BUY' else round(entry + 0.0050, 5)
        time_estimate = round(10 / avg_pips_per_minute)
        return signal, entry, tp, sl, time_estimate
    else:
        return None, None, None, None, None
