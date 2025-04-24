import os
import shutil
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ConversationHandler, ContextTypes, filters
from icrawler.builtin import GoogleImageCrawler

# توکن ربات
TOKEN = "7714713597:AAELFzgtECBWRK7TDljAOXub-pF6FO3oBCw"

# مراحل مکالمه
ASK_QUERY, ASK_COUNT = range(2)
TEMP_DIR = "downloaded_images"

# استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔍 جست‌وجوی عکس", callback_data="search_image")]
    ]
    await update.message.reply_text(
        "سلام! یکی از گزینه‌ها رو انتخاب کن:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# هندلر دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "search_image":
        await query.edit_message_text("لطفاً موضوع مورد نظر برای عکس رو بنویس:")
        return ASK_QUERY

# گرفتن موضوع
async def ask_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["query"] = update.message.text
    await update.message.reply_text("چند تا عکس می‌خوای؟ (حداکثر ۲۰)")
    return ASK_COUNT

# گرفتن تعداد و ارسال عکس‌ها
async def send_images(update: Update, context: ContextTypes.DEFAULT_TYPE):
    count_text = update.message.text
    if not count_text.isdigit():
        await update.message.reply_text("لطفاً یک عدد بین 1 تا 20 وارد کن.")
        return ASK_COUNT

    count = int(count_text)
    if count < 1 or count > 20:
        await update.message.reply_text("حداکثر ۲۰ تا عکس مجازه.")
        return ASK_COUNT

    query = context.user_data["query"]
    await update.message.reply_text(f"در حال جست‌وجوی {count} عکس درباره: {query}")

    os.makedirs(TEMP_DIR, exist_ok=True)
    google_crawler = GoogleImageCrawler(storage={"root_dir": TEMP_DIR})
    google_crawler.crawl(keyword=query, max_num=count)

    for filename in os.listdir(TEMP_DIR):
        path = os.path.join(TEMP_DIR, filename)
        with open(path, "rb") as f:
            await update.message.reply_photo(photo=f)
        await asyncio.sleep(0.2)

    shutil.rmtree(TEMP_DIR)
    return ConversationHandler.END

# اجرای اصلی
def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler)],
        states={
            ASK_QUERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_count)],
            ASK_COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, send_images)],
        },
        fallbacks=[]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    app.run_polling()

if __name__ == "__main__":
    main()