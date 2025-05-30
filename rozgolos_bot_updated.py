import asyncio
import logging
import nest_asyncio
from os import getenv
from telegram import (
    Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters,
    ConversationHandler, ContextTypes
)

# Стан анкети
FULL_NAME, EMAIL, PHONE, PLATFORM = range(4)

# Логи
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        await update.message.reply_photo(photo=open("rozgolos_start.jpg", "rb"))
    except FileNotFoundError:
        await update.message.reply_text("⚠️ Зображення не знайдено. Продовжимо без нього.")

    await update.message.reply_text(
        "🇺🇦 Вас вітає офіційний бот застосунку *ROZGOLOS*.\n\n"
        "Для запуску — заповніть коротку анкету нижче. Це займе менше хвилини.\n\n"
        "🔽 Натисніть *Продовжити*, щоб розпочати.",
        reply_markup=ReplyKeyboardMarkup([["Продовжити"]], resize_keyboard=True),
        parse_mode="Markdown"
    )
    return FULL_NAME

# Отримуємо ПІБ
async def get_full_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text.lower() == "продовжити":
        await update.message.reply_text("👤 Введіть *Прізвище та ім’я*:", parse_mode="Markdown")
        return FULL_NAME
    else:
        context.user_data['full_name'] = update.message.text
        await update.message.reply_text("📧 Введіть ваш Email:")
        return EMAIL

# Email
async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['email'] = update.message.text
    await update.message.reply_text("📞 Введіть ваш номер телефону:")
    return PHONE

# Телефон → Переходи на магазини
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['phone'] = update.message.text

    buttons = [
        [InlineKeyboardButton("📱 Android", url="https://play.google.com/store/apps/details?id=com.rozgolos")],
        [InlineKeyboardButton("🍏 iOS", url="https://apps.apple.com/app/id6739999117")],
    ]

    await update.message.reply_text(
        "⬇️ Оберіть вашу операційну систему:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    return PLATFORM

# ОС → завершення
async def get_platform(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['platform'] = update.message.text

    await update.message.reply_text(
        f"✅ Дякуємо за надану інформацію!\n\n"
        f"*ПІБ:* {context.user_data.get('full_name')}\n"
        f"*Email:* {context.user_data.get('email')}\n"
        f"*Телефон:* {context.user_data.get('phone')}\n"
        f"*ОС:* {context.user_data.get('platform')}",
        parse_mode="Markdown"
    )

    await update.message.reply_text("🙏 Дякуємо! З вами зв’яжеться наш консультант найближчим часом.")
    return ConversationHandler.END

# Скасування
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Операцію скасовано.")
    return ConversationHandler.END

# Головна функція
async def main():
    nest_asyncio.apply()
    TOKEN = getenv("BOT_TOKEN") or "встав_свій_тестовий_токен_сюди"
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_full_name)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            PLATFORM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_platform)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    await app.run_polling()

# Запуск
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
