import os
import math
import logging
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
from icrawler.builtin import GoogleImageCrawler
from icrawler import ImageDownloader

# تنظیمات ربات
BOT_TOKEN = "7714713597:AAELFzgtECBWRK7TDljAOXub-pF6FO3oBCw"
ASK_QUERY, ASK_COUNT = range(2)

# لاگ‌گیری
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# دانلودر سفارشی برای گرفتن URLها
class URLCollector(ImageDownloader):
    def download(self, task, default_ext, timeout=5, **kwargs):
        return task['file_url']

# گرفتن لیست آدرس عکس‌ها
def get_image_urls(query, count):
    crawler = GoogleImageCrawler(downloader_cls=URLCollector)
    crawler.crawl(
        keyword=query,
        max_num=count,
        file_idx_offset=0,
        feeder_threads=1,
        parser_threads=1,
        downloader_threads=1
    )
    return crawler.downloader.rets

# شروع مکالمه
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("سلام! موضوعی که می‌خوای عکس‌هاش رو بفرستم بنویس:")
    return ASK_QUERY

# دریافت موضوع
async def ask_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['query'] = update.message.text.strip()
    await update.message.reply_text("چند تا عکس می‌خوای؟ فقط عدد بنویس:")
    return ASK_COUNT

# دریافت تعداد و ارسال عکس‌ها
async def ask_count(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        count = int(update.message.text.strip())
        if count <= 0:
            raise ValueError
    except ValueError:
        await update.message.reply_text("لطفاً فقط یک عدد معتبر بنویس.")
        return ASK_COUNT

    query = context.user_data.get('query')
    await update.message.reply_text(f"در حال جستجو برای: {query} ({count} عکس)...")

    urls = get_image_urls(query, count)
    media = []
    for i, url in enumerate(urls):
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                img_file = BytesIO(resp.content)
                img_file.name = f"image_{i}.jpg"
                caption = f"تصویر {i+1} برای '{query}'" if i == 0 else None
                media.append(InputMediaPhoto(media=img_file, caption=caption))
        except Exception as e:
            logger.warning(f"مشکل در دانلود عکس: {e}")
            continue

    if not media:
        await update.message.reply_text("هیچ عکسی پیدا نشد. موضوع دیگه‌ای امتحان کن.")
        return ConversationHandler.END

    for i in range(0, len(media), 10):
        await update.message.reply_media_group(media[i:i+10])

    await update.message.reply_text("✅ ارسال انجام شد! برای شروع دوباره /start رو بزن.")
    return ConversationHandler.END

# لغو مکالمه
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("⛔ عملیات لغو شد. برای شروع دوباره /start رو بزن.")
    return ConversationHandler.END

# اجرای اصلی ربات
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_QUERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_query)],
            ASK_COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_count)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    print("ربات فعال شد. در تلگرام /start رو بزن.")
    app.run_polling()

if __name__ == '__main__':
    main()
