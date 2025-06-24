import telebot
from analysis import analyze_signal
import os

BOT_TOKEN = os.getenv("BOT_TOKEN") or '8148012923:AAGMLwawfHBv_fqqMUsf08Odb5kKSiakIKo'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Напиши /signal, чтобы получить торговый сигнал по EUR/USD.")

@bot.message_handler(commands=['signal'])
def send_signal(message):
    signal = analyze_signal()
    bot.reply_to(message, signal)

bot.polling()