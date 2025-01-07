import telebot

bot = telebot.TeleBot('7638563599:AAHiWrHxxfgAjSmIU8Tgb6BzLwIRPUs8z9s')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()