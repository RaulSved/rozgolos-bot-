import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import os

TOKEN = "7666787687:AAHbD..."  # встав сюди свій робочий токен

# Увімкнення логів
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Кнопки меню
keyboard_main = [
    [InlineKeyboardButton("📱 Android", url="https://play.google.com/store/apps/details?id=com.rozgolos")],
    [InlineKeyboardButton("🥏 iOS", url="https://apps.apple.com/app/id6739999117")],
    [InlineKeyboardButton("🌐 Офіційний сайт", url="https://rozgolos.online/bronyuvannya?utm_source=fb&utm_medium=paid_social&utm_campaign=RozgolosTelegram&utm_content=RozgolosTelegram&utm_term=RozgolosTelegram")],
    [InlineKeyboardButton("➡️ Продовжити", callback_data="continue")]
]

# Обробник /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    photo_path = os.path.join(os.path.dirname(__file__), "start.jpg")

    if os.path.exists(photo_path):
        with open(photo_path, "rb") as photo:
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Введіть Прізвище та ім'я",
        reply_markup=InlineKeyboardMarkup(keyboard_main)
    )

# Обробник кнопок
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "continue":
        await query.edit_message_text(text="🙏 Дякуємо! Заявку отримано. Чекайте звідомлення від нашого консультанта!")

# Обробка тексту (ПІБ, email, телефон...)
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    user_id = update.effective_chat.id

    logger.info(f"Заявка від {user_id}: {text}")
    await update.message.reply_text("🙏 Дякуємо за ваші дані! Натисніть \"Продовжити\" або виберіть платформу.")

# Основна функція
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Бот запущено...")
    app.run_polling()

if __name__ == "__main__":
    main()
