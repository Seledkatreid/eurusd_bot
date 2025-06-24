import telebot
from analysis import analyze_signal
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который анализирует EUR/USD по RSI и Bollinger Bands. Напиши /signal чтобы получить торговый сигнал.")

@bot.message_handler(commands=['signal'])
def send_signal(message):
    signal = analyze_signal()
    bot.reply_to(message, signal)

bot.polling()