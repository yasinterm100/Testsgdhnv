import telebot

# توکن ربات تلگرام خود را اینجا وارد کنید
TOKEN = 'توکن_ربات_اینجا'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: message.text.lower() == "سلام")
def reply_to_salam(message):
    bot.reply_to(message, "خوبی")

# شروع به کار ربات
print("ربات در حال اجراست...")
bot.polling()
