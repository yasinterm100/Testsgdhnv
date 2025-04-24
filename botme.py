import os
import requests
from io import BytesIO
from telegram import Update, InputMediaPhoto
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
from duckduckgo_search import DuckDuckGoImages

# توکن ربات تلگرام
BOT_TOKEN = "7714713597:AAELFzgtECBWRK7TDljAOXub-pF6FO3oBCw"
ASK_QUERY, ASK_COUNT = range(2)

# شروع مکالمه
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("سلام! موضوع عکس‌هایی که می‌خوای رو بنویس:")
    return ASK_QUERY

# دریافت موضوع جستجو
async def get_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['query'] = update.message.text.strip()
    await update.message.reply_text("چند تا عکس می‌خوای؟ فقط عدد بنویس:")
    return ASK_COUNT

# دریافت تعداد و ارسال تصاویر
async def get_count(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        count = int(update.message.text.strip())
        if count <= 0:
            raise ValueError
    except:
        await update.message.reply_text("عدد معتبر وارد کن.")
        return ASK_COUNT

    query = context.user_data.get("query")
    await update.message.reply_text(f"در حال جستجو برای: «{query}» ({count} عکس) ...")

    results = DuckDuckGoImages().search(query, max_results=count)
    media = []

    for i, result in enumerate(results):
        url = result.image
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                img = BytesIO(res.content)
                img.name = f"image_{i}.jpg"
                caption = f"تصویر {i+1} از {count}" if i == 0 else None
                media.append(InputMediaPhoto(media=img, caption=caption))
        except:
            continue
        if len(media) >= count:
            break

    if not media:
        await update.message.reply_text("هیچ عکسی پیدا نشد. لطفاً موضوع دیگه‌ای امتحان کن.")
        return ConversationHandler.END

    for i in range(0, len(media), 10):
        await update.message.reply_media_group(media[i:i+10])

    await update.message.reply_text("✅ عکس‌ها ارسال شدن! برای جستجوی جدید /start رو بزن.")
    return ConversationHandler.END

# لغو عملیات
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("⛔ عملیات لغو شد.")
    return ConversationHandler.END

# اجرای اصلی ربات
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_QUERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_query)],
            ASK_COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_count)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv)
    print("ربات اجرا شد. در تلگرام /start رو بزن.")
    app.run_polling()

if __name__ == "__main__":
    main()
