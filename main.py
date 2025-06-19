from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from config import INTERVALS
from data_fetch import fetch_data
from signal_logic import analyze_data

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton(text=label, callback_data=label)
        for label in ["1 мин", "3 мин"]
    ], [
        InlineKeyboardButton(text=label, callback_data=label)
        for label in ["5 мин", "15 мин"]
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите таймфрейм для сигнала:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    tf_label = query.data
    interval = INTERVALS[tf_label]
    try:
        data = fetch_data(interval)
        signal = analyze_data(data)
    except Exception as e:
        signal = f"Ошибка: {e}"
    await query.edit_message_text(text=f"Таймфрейм: {tf_label}
{signal}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

if __name__ == "__main__":
    app.run_polling()