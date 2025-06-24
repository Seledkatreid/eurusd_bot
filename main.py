import telebot
from analysis import analyze_signal
import os

BOT_TOKEN = os.getenv("BOT_TOKEN") or '8148012923:AAGMLwawfHBv_fqqMUsf08Odb5kKSiakIKo'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я анализирую EUR/USD по RSI и Bollinger Bands. Напиши /signal для сигнала.")

@bot.message_handler(commands=['signal'])
def send_signal(message):
    signal = analyze_signal()
    bot.send_message(message.chat.id, signal)

bot.polling()