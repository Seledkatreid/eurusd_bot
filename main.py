
import telebot
from config import BOT_TOKEN, CHAT_ID
from data_fetch import get_price_data
from analysis import analyze

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот по EUR/USD. Напиши /signal для получения сигнала.")

@bot.message_handler(commands=['signal'])
def send_signal(message):
    data = get_price_data()
    if not data:
        bot.send_message(message.chat.id, "Ошибка при получении котировок.")
        return

    signal, entry, tp, sl, estimate = analyze(data)
    if signal:
        msg = (
            f"📊 Сигнал: {signal}\n"
            f"💰 Вход: {entry}\n"
            f"🎯 TP: {tp} | 🛑 SL: {sl}\n"
            f"⏳ Прогноз времени до TP: ~{estimate} мин"
        )
    else:
        msg = "Сигналов на данный момент нет."

    bot.send_message(message.chat.id, msg)

bot.polling()
