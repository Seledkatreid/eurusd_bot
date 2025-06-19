from telegram.ext import ApplicationBuilder, CommandHandler
from config import RSI_PERIOD, RSI_OVERSOLD, RSI_OVERBOUGHT
from data_fetch import fetch_data
from rsi_signal import generate_signal

BOT_TOKEN = "8148012923:AAGMLwawfHBv_fqqMUsf08Odb5kKSiakIKo"

async def start(update, context):
    await update.message.reply_text("Привет! Я бот для бинарных сигналов по EUR/USD.\nНапиши /signal чтобы получить сигнал.")

async def signal(update, context):
    try:
        df = fetch_data()
        signal_text = generate_signal(df, RSI_PERIOD, RSI_OVERSOLD, RSI_OVERBOUGHT)
        await update.message.reply_text(signal_text)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.run_polling()

if __name__ == "__main__":
    main()