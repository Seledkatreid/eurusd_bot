import telebot
from config import TOKEN
from data_fetch import fetch_data
from analysis import analyze

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Напиши /signal 1 или /signal 5, чтобы получить сигнал по EUR/USD с анализом.")

@bot.message_handler(commands=['signal'])
def send_signal(message):
    try:
        parts = message.text.strip().split()
        timeframe = int(parts[1]) if len(parts) > 1 else 1
        if timeframe not in [1, 3, 5, 15]:
            bot.send_message(message.chat.id, "Выбери таймфрейм: 1, 3, 5 или 15 минут. Например: /signal 5")
            return

        raw_data = fetch_data()
        # Агрегируем данные по таймфрейму
        df = raw_data.copy()
        df['datetime'] = pd.to_datetime(df['datetime'])
        df.set_index('datetime', inplace=True)
        df = df.resample(f'{timeframe}T').agg({'close': 'last'}).dropna().reset_index()

        signal, entry, tp, sl, eta = analyze(df)
        if signal:
            bot.send_message(message.chat.id,
                f"📊 Сигнал: {signal}\n"
                f"💰 Вход: {entry}\n"
                f"🎯 TP: {tp} | 🛑 SL: {sl}\n"
                f"⏳ Прогноз времени до TP: ~{eta} мин"
            )
        else:
            bot.send_message(message.chat.id, "Сигналов нет по текущему анализу.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

bot.polling()