import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import nest_asyncio

# TOKEN (тільки для тесту, не зберігати тут у продакшн!)
TOKEN = "7859058780:AAHvBh7w7iNvc8KLE9Eq0RMfmjdwKYuAFOA"

# Увімкнути логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Вітання
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_url = "https://rozgolos.online/static/rozgolos-preview.jpg"  # URL твоєї картинки

    keyboard = [
        [KeyboardButton("🔗 Android")],
        [KeyboardButton("🍏 iOS")],
        [KeyboardButton("🌐 Офіційний сайт")],
        [KeyboardButton("✅ Продовжити")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_photo(
        photo=photo_url,
        caption="Введіть Прізвище та ім’я",
        reply_markup=reply_markup
    )

# Обробка тексту
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.effective_chat.id

    if user_text == "✅ Продовжити":
        await context.bot.send_message(chat_id=chat_id, text="✅ Дякуємо! Заявку прийнято. Очікуйте дзвінка.")
    elif user_text == "🔗 Android":
        await context.bot.send_message(chat_id=chat_id, text="Відкрийте додаток: https://play.google.com/store/apps/details?id=com.rozgolos")
    elif user_text == "🍏 iOS":
        await context.bot.send_message(chat_id=chat_id, text="Відкрийте додаток: https://apps.apple.com/app/id6739999117")
    elif user_text == "🌐 Офіційний сайт":
        await context.bot.send_message(chat_id=chat_id, text="Офіційний сайт: https://rozgolos.online/bronyuvannya?utm_source=fb&utm_medium=paid_social&utm_campaign=RozgolosTelegram&utm_content=RozgolosTelegram&utm_term=RozgolosTelegram&fbclid=fbclid")
    else:
        await context.bot.send_message(chat_id=chat_id, text=f"Дякую, {user_text}! Для продовження натисніть ✅ Продовжити")

# Головна функція
async def main():
    nest_asyncio.apply()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Очистити Webhook і запускати polling
    await app.bot.delete_webhook(drop_pending_updates=True)
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())


