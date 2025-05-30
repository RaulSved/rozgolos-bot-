import asyncio
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)

# States
AWAIT_NAME, FULL_NAME, EMAIL, PHONE, PLATFORM = range(5)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

ADMIN_CHAT_ID = 7666787687

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        await update.message.reply_photo(photo=open("rozgolos_start.jpg", "rb"))
    except FileNotFoundError:
        await update.message.reply_text("⚠️ Зображення не знайдено. Продовжимо без нього.")

    await update.message.reply_text(
        "\U0001F1FA\U0001F1E6 Вас вітає офіційний бот застосунку *ROZGOLOS*\.

"
        "Для запуску — заповніть коротку анкету нижче\. Це займе менше хвилини\.

"
        "\U0001F53D Натисніть *Продовжити*, щоб розпочати\.",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("\U0001F680 Продовжити")]], resize_keyboard=True
        ),
        parse_mode="MarkdownV2"
    )
    return AWAIT_NAME

async def await_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if "продовжити" not in update.message.text.lower():
        await update.message.reply_text("Натисніть кнопку *Продовжити*, щоб почати\.", parse_mode="MarkdownV2")
        return AWAIT_NAME

    await update.message.reply_text("\U0001F464 Введіть *Прізвище та ім’я*:", parse_mode="MarkdownV2")
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
    await update.message.reply_text(
        "\U0001F4F1 Яка операційна система на вашому телефоні?",
        reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton("Android")],
            [KeyboardButton("iOS")],
            [KeyboardButton("\U0001F310 Офіційний сайт")],
        ], resize_keyboard=True)
    )
    return PLATFORM

async def get_platform(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['platform'] = update.message.text

    await update.message.reply_text(
        f"\u2705 Дякуємо за надану інформацію!\n\n"
        f"\U0001F464 *ПІБ:* {context.user_data['full_name']}\n"
        f"\U0001F4E7 *Email:* {context.user_data['email']}\n"
        f"\U0001F4DE *Телефон:* {context.user_data['phone']}\n"
        f"\U0001F4F1 *ОС:* {context.user_data['platform']}",
        parse_mode="Markdown"
    )

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=(
            "\U0001F4E5 Нова заявка:\n\n"
            f"\U0001F464 ПІБ: {context.user_data['full_name']}\n"
            f"\U0001F4E7 Email: {context.user_data['email']}\n"
            f"\U0001F4DE Телефон: {context.user_data['phone']}\n"
            f"\U0001F4F1 ОС: {context.user_data['platform']}"
        )
    )

    await update.message.reply_text(
        "⬇️ Завантажити застосунок або відвідати сайт:",
        reply_markup=ReplyKeyboardMarkup([
            [
                KeyboardButton("📲 Android", url="https://play.google.com/store/apps/details?id=com.rozgolos"),
                KeyboardButton("📱 iOS", url="https://apps.apple.com/app/id6739999117")
            ],
            [
                KeyboardButton("🌐 Офіційний сайт", url="https://rozgolos.online/bronyuvannya?utm_source=fb&utm_medium=paid_social&utm_campaign=RozgolosTelegram&utm_content=RozgolosTelegram&utm_term=RozgolosTelegram&fbclid=fbclid")
            ]
        ], resize_keyboard=True)
    )

    await update.message.reply_text("\U0001F64F Дякуємо! З вами зв’яжеться наш консультант.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("\u274C Операцію скасовано.")
    return ConversationHandler.END

async def main():
    TOKEN = "7859058780:AAHvBh7w7iNvc8KLE9Eq0RMfmjdwKYuAFOA"
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
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())
