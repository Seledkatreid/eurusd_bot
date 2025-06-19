import telebot
import pandas as pd
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import TOKEN
from data_fetch import fetch_data
from analysis import analyze

bot = telebot.TeleBot(TOKEN)

# Главное меню выбора таймфрейма
def build_timeframe_keyboard():
    markup = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text="1 мин", callback_data="tf_1"),
        InlineKeyboardButton(text="3 мин", callback_data="tf_3"),
        InlineKeyboardButton(text="5 мин", callback_data="tf_5"),
        InlineKeyboardButton(text="15 мин", callback_data="tf_15"),
    ]
    markup.row(*buttons[:2])
    markup.row(*buttons[2:])
    return markup

@bot.message_handler(commands=['start', 'signal'])
def send_menu(message):
    bot.send_message(message.chat.id, 
                     "Выберите таймфрейм для сигнала:", 
                     reply_markup=build_timeframe_keyboard())

@bot.callback_query_handler(func=lambda call: call.data.startswith("tf_"))
def callback_timeframe(call: CallbackQuery):
    try:
        tf = int(call.data.split("_")[1])
        # агрегация данных
        raw = fetch_data()
        df = pd.DataFrame(raw)
        df['datetime'] = pd.to_datetime(df['datetime'])
        df.set_index('datetime', inplace=True)
        df = df.resample(f'{tf}T').agg({'close': 'last'}).dropna().reset_index()

        signal, entry, tp, sl, eta = analyze(df)
        if signal:
            text = (
                f"📊 Сигнал: {signal}\n"
                f"💰 Вход: {entry}\n"
                f"🎯 TP: {tp} | 🛑 SL: {sl}\n"
                f"⏳ Прогноз до TP: ~{eta} мин\n"
                f"🕒 Таймфрейм: {tf} мин"
            )
        else:
            text = f"На таймфрейме {tf} мин сигналов нет."
        bot.send_message(call.message.chat.id, text)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Ошибка: {e}")

if __name__ == '__main__':
    bot.polling()