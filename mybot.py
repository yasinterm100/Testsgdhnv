import telebot
from telebot import types

TOKEN = '7942772127:AAGjnzjnsHqAQAo6HtS2pdPEawQYbSPMJ1o'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # ایجاد دکمه‌های کیبورد
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_photo = types.KeyboardButton("عکس")
    button_end = types.KeyboardButton("تمام")
    markup.add(button_photo, button_end)
    
    bot.send_message(message.chat.id, "سلام! لطفاً یکی از دکمه‌ها را انتخاب کنید:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "عکس")
def send_photo_message(message):
    bot.send_message(message.chat.id, "شما دکمه 'عکس' را زدید!")

@bot.message_handler(func=lambda message: message.text == "تمام")
def end_message(message):
    bot.send_message(message.chat.id, "ربات تمام شد! خداحافظ!")

# شروع به کار ربات با تنظیمات polling
print("ربات۱ در حال اجراست...")
bot.polling(timeout=10, long_polling_timeout=5, retry_delay=3)
