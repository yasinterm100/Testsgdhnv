import telebot

TOKEN = '7942772127:AAGjnzjnsHqAQAo6HtS2pdPEawQYbSPMJ1o'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: message.text.lower() == "سلام")
def reply_to_salam(message):
    bot.reply_to(message, "خوبی")

while True:
    try:
        print("ربات در حال اجراست...")
        bot.polling(timeout=10, long_polling_timeout=5, retry_delay=3)
    except Exception as e:
        print(f"Error: {e}")
