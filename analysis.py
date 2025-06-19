import pandas as pd
import ta

def analyze(data):
    df = pd.DataFrame(data)
    df = df.rename(columns={'datetime': 'time', 'close': 'close'})
    df['close'] = df['close'].astype(float)
    df = df.sort_values('time')

    # Индикаторы
    df['ema_fast'] = ta.trend.ema_indicator(df['close'], window=5, fillna=True)
    df['ema_slow'] = ta.trend.ema_indicator(df['close'], window=21, fillna=True)
    df['rsi'] = ta.momentum.rsi(df['close'], window=14, fillna=True)
    df['macd'] = ta.trend.macd(df['close'], window_slow=26, window_fast=12, fillna=True)
    df['macd_signal'] = ta.trend.macd_signal(df['close'], window_slow=26, window_fast=12, window_sign=9, fillna=True)

    # Временная замена high/low на close (нет OHLC)
    df['cci'] = ta.trend.cci(high=df['close'], low=df['close'], close=df['close'], window=14, fillna=True)
    bb = ta.volatility.BollingerBands(df['close'], window=20, fillna=True)
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()
    df['stoch_rsi'] = ta.momentum.stochrsi(df['close'], window=14, fillna=True)

    # Волатильность
    df['diff'] = df['close'].diff().abs()
    avg_volatility = df['diff'].tail(10).mean()
    pip_size = 0.0001
    avg_pips_per_minute = avg_volatility / pip_size if avg_volatility else 1

    last = df.iloc[-1]

    signal = None

    if (
        last['ema_fast'] > last['ema_slow'] and
        last['rsi'] < 70 and
        last['macd'] > last['macd_signal'] and
        -100 < last['cci'] < 100 and
        last['close'] > last['bb_lower'] and
        last['stoch_rsi'] < 0.8
    ):
        signal = 'BUY'
    elif (
        last['ema_fast'] < last['ema_slow'] and
        last['rsi'] > 30 and
        last['macd'] < last['macd_signal'] and
        -100 < last['cci'] < 100 and
        last['close'] < last['bb_upper'] and
        last['stoch_rsi'] > 0.2
    ):
        signal = 'SELL'

    if signal:
        entry = last['close']
        recent_high = df['close'].rolling(10).max().iloc[-1]
        recent_low = df['close'].rolling(10).min().iloc[-1]

        if signal == 'BUY':
            tp = round(recent_high, 5)
            sl = round(recent_low, 5)
        else:
            tp = round(recent_low, 5)
            sl = round(recent_high, 5)

        time_estimate = round(abs(tp - entry) / avg_volatility) if avg_volatility else 5
        return signal, entry, tp, sl, time_estimate
    else:
        return None, None, None, None, None