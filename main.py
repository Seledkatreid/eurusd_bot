from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from config import INTERVALS
from data_fetch import fetch_data
from analysis import generate_signal

keyboard = ReplyKeyboardMarkup(
    [[key for key in INTERVALS.keys()]], resize_keyboard=True, one_time_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Выберите таймфрейм для сигнала:", reply_markup=keyboard)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    interval = INTERVALS.get(user_input)
    if not interval:
        await update.message.reply_text("Пожалуйста, выбери таймфрейм с клавиатуры.")
        return
    
    data, error = fetch_data(interval)
    if error:
        await update.message.reply_text(error)
    else:
        signal = generate_signal(data)
        await update.message.reply_text(signal)

if __name__ == "__main__":
    from config import API_KEY
    import os
    from telegram.ext import Application

    token = os.getenv(8148012923:AAGMLwawfHBv_fqqMUsf08Odb5kKSiakIKo)

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()