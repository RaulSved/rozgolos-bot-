import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)

# States
FULL_NAME, EMAIL, PHONE, PLATFORM = range(4)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_photo(photo=open("rozgolos_start.jpg", "rb"))
    await update.message.reply_text(
        "🇺🇦 Вас вітає офіційний бот застосунку *ROZGOLOS*.

"
        "Для запуску — заповніть коротку анкету нижче. Це займе менше хвилини.

"
        "🔽 Натисніть *Продовжити* щоб розпочати.",
        reply_markup=ReplyKeyboardMarkup([['Продовжити']], resize_keyboard=True),
        parse_mode="Markdown"
    )
    return FULL_NAME

async def get_full_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['full_name'] = update.message.text
    await update.message.reply_text("📧 Введіть ваш Email:")
    return EMAIL

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['email'] = update.message.text
    await update.message.reply_text("📞 Введіть ваш номер телефону:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("📱 Яка операційна система на вашому телефоні?
Наприклад: Android або iOS")
    return PLATFORM

async def get_platform(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['platform'] = update.message.text
    await update.message.reply_text(
        f"✅ Дякуємо за надану інформацію!

"
        f"*ПІБ:* {context.user_data['full_name']}
"
        f"*Email:* {context.user_data['email']}
"
        f"*Телефон:* {context.user_data['phone']}
"
        f"*ОС:* {context.user_data['platform']}",
        parse_mode="Markdown"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Операцію скасовано.")
    return ConversationHandler.END

if __name__ == '__main__':
    TOKEN = "6453650003:AAHn4X2fTPXUInD-6HdLkPUKU_WAOsW7ekc"
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_full_name)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            PLATFORM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_platform)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()