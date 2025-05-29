import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ConversationHandler,
    ContextTypes, filters
)

TOKEN = "тут_твій_токен"

# Стани
(
    FULL_NAME,
    EMAIL,
    PHONE,
    OS_CHOICE,
) = range(4)

# Налаштування логування
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    await update.message.reply_photo(photo=open("rozgolos_start.jpg", "rb"))
    await update.message.reply_text(
        await update.message.reply_text(
    f"""🇺🇦 Вас вітає офіційний бот застосунку *ROZGOLOS*.

Для запуску — заповніть коротку анкету нижче. Це займе менше хвилини.

🔽 Натисніть *Продовжити* щоб розпочати.""",
    reply_markup=ReplyKeyboardMarkup([['Продовжити']], resize_keyboard=True),
    parse_mode="Markdown"
)
    return FULL_NAME

async def get_full_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("📝 Введіть, будь ласка, *ПІБ:*", parse_mode="Markdown")
    return EMAIL

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["full_name"] = update.message.text
    await update.message.reply_text("📧 Введіть *email*:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["email"] = update.message.text
    await update.message.reply_text("📱 Введіть *номер телефону:*")
    return OS_CHOICE

async def get_os(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["phone"] = update.message.text

    keyboard = [["iOS", "Android"]]
    await update.message.reply_text(
        "🤖 Оберіть *операційну систему:*",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True),
        parse_mode="Markdown"
    )
    return ConversationHandler.END

async def os_redirect(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    os_choice = update.message.text.lower()
    if "ios" in os_choice:
        await update.message.reply_text(
            "🔗 Відкриваю App Store...",
        )
        await update.message.reply_text(
            "https://apps.apple.com/app/id6739999117"
        )
    elif "android" in os_choice:
        await update.message.reply_text(
            "🔗 Відкриваю Google Play...",
        )
        await update.message.reply_text(
            "https://play.google.com/store/apps/details?id=com.rozgolos"
        )
    else:
        await update.message.reply_text("Невірна операційна система. Спробуйте ще раз.")

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_full_name)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            OS_CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_os)],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.Regex("^(iOS|Android)$"), os_redirect))

    application.run_polling()

if __name__ == "__main__":
    main()
