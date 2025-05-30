import asyncio
import logging
from os import getenv
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)
import nest_asyncio

# СТАНИ анкети
AWAIT_NAME, FULL_NAME, EMAIL, PHONE, PLATFORM = range(5)

# Логування
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        await update.message.reply_photo(photo=open("rozgolos_start.jpg", "rb"))
    except FileNotFoundError:
        await update.message.reply_text("⚠️ Зображення не знайдено. Продовжимо без нього.")

    await update.message.reply_text(
        "\U0001F1FA\U0001F1E6 Вас вітає офіційний бот застосунку *ROZGOLOS*\n\n"
        "Для запуску — заповніть коротку анкету нижче. Це займе менше хвилини.\n\n"
        "\u2B07\ufe0f Натисніть *Продовжити*, щоб розпочати.",
        reply_markup=ReplyKeyboardMarkup([["Продовжити"]], resize_keyboard=True),
        parse_mode="Markdown"
    )
    return AWAIT_NAME

# Очікуємо натискання "Продовжити"
async def await_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text.lower() != "продовжити":
        await update.message.reply_text("Натисніть кнопку *Продовжити*, щоб почати.", parse_mode="Markdown")
        return AWAIT_NAME

    await update.message.reply_text("\U0001F464 Введіть *Прізвище та ім’я*:", parse_mode="Markdown")
    return FULL_NAME

async def get_full_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['full_name'] = update.message.text
    await update.message.reply_text("\U0001F4E7 Введіть ваш Email:")
    return EMAIL

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['email'] = update.message.text
    await update.message.reply_text("\U0001F4DE Введіть ваш номер телефону:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['phone'] = update.message.text
    buttons = [
        [InlineKeyboardButton("\U0001F4F1 Android", url="https://play.google.com/store/apps/details?id=com.rozgolos")],
        [InlineKeyboardButton("\U0001F34F iOS", url="https://apps.apple.com/app/id6739999117")],
    ]
    await update.message.reply_text(
        "\U0001F4F1 Яка операційна система на вашому телефоні?",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    return PLATFORM

async def get_platform(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['platform'] = update.message.text
    await update.message.reply_text(
        f"\u2705 Дякуємо за надану інформацію!\n\n"
        f"*ПІБ:* {context.user_data['full_name']}\n"
        f"*Email:* {context.user_data['email']}\n"
        f"*Телефон:* {context.user_data['phone']}\n"
        f"*ОС:* {context.user_data['platform']}",
        parse_mode="Markdown"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("\u274C Операцію скасовано.")
    return ConversationHandler.END

async def main():
    nest_asyncio.apply()
    TOKEN = getenv("BOT_TOKEN") or "7859058780:AAHvBh7w7iNvc8KLE9Eq0RMfmjdwKYuAFOA"
    app = ApplicationBuilder().token(TOKEN).build()

    await app.bot.delete_webhook(drop_pending_updates=True)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            AWAIT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, await_name)],
            FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_full_name)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            PLATFORM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_platform)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    await app.run_polling()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
