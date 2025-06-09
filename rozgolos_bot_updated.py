m pathlib import Path

code = """
import asyncio
import logging
from telegram import (
    Update, KeyboardButton, ReplyKeyboardMarkup,
    InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# Стан анкети
AWAIT_NAME, FULL_NAME, EMAIL, PHONE = range(4)

# ID чату для повідомлень адміну
ADMIN_CHAT_ID = 7666787687

# Токен тестового бота
TOKEN = "7859058780:AAHvBh7w7iNvc8KLE9Eq0RMfmjdwKYuAFOA"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("✅ start() triggered")
    try:
        await update.message.reply_photo(photo=open("rozgolos_start.jpg", "rb"))
    except FileNotFoundError:
        await update.message.reply_text("⚠️ Зображення не знайдено.")

    await update.message.reply_text(
        "🎯 *Тільки через бота* — повний доступ до ROZGOLOS *на 3 дні безкоштовно!*\\n\\n"
        "🇺🇦 Вас вітає офіційний бот застосунку *ROZGOLOS*\\.\\n\\n"
        "Для запуску — заповніть коротку анкету нижче\\.\\n\\n"
        "🔽 Натисніть *Продовжити*, щоб розпочати\\.",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("🚀 Продовжити")]], resize_keyboard=True
        ),
        parse_mode="MarkdownV2"
    )
    return AWAIT_NAME


async def await_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("✅ await_name() triggered")
    if "продовжити" not in update.message.text.lower():
        await update.message.reply_text(
            "Натисніть кнопку *Продовжити*, щоб почати.", parse_mode="MarkdownV2"
        )
        return AWAIT_NAME

    await update.message.reply_text(
        "👤 Введіть *Прізвище та ім’я*:",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="MarkdownV2"
    )
    return FULL_NAME


async def get_full_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("✅ get_full_name() triggered")
    context.user_data["full_name"] = update.message.text
    await update.message.reply_text("📧 Введіть ваш Email:")
    return EMAIL


async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("✅ get_email() triggered")
    context.user_data["email"] = update.message.text
    await update.message.reply_text("📞 Введіть ваш номер телефону:")
    return PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("✅ get_phone() triggered")
    context.user_data["phone"] = update.message.text

    await update.message.reply_text(
        f"✅ Дякуємо за надану інформацію!\\n\\n"
        f"👤 *ПІБ:* {context.user_data['full_name']}\\n"
        f"📧 *Email:* {context.user_data['email']}\\n"
        f"📞 *Телефон:* {context.user_data['phone']}",
        parse_mode="Markdown"
    )

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=(
            "📥 Нова заявка:\\n\\n"
            f"👤 ПІБ: {context.user_data['full_name']}\\n"
            f"📧 Email: {context.user_data['email']}\\n"
            f"📞 Телефон: {context.user_data['phone']}"
        )
    )

    await update.message.reply_text(
        "🎁 Ви активували акцію — *3 дні повного доступу до ROZGOLOS безкоштовно!*\\n\\n"
        "⚠️ Пропозиція дійсна лише при переході через цього Telegram-бота.",
        parse_mode="Markdown"
    )

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Android", url="https://play.google.com/store/apps/details?id=com.rozgolos&referrer=utm_source%3Dfb%2526utm_medium%3Dpaid_social%2526utm_campaign%3DRozgolos04.05.25TGbotGoPl%2526utm_content%3DRozgolos04.05.25TGbotGoPl%2526utm_term%3DRozgolos04.05.25TGbotGoPl")],
        [InlineKeyboardButton("🔗 iOS", url="https://rozgolos.online/apple/store?utm_source=fb&utm_medium=paid_social&utm_campaign=Rozgolos04.05.25TGbotAppSt&utm_content=Rozgolos04.05.25TGbotAppSt&utm_term=Rozgolos04.05.25TGbotAppSt")],
        [InlineKeyboardButton("🌐 Офіційний сайт", url="https://rozgolos.online/bronyuvannya?utm_source=fb&utm_medium=paid_social&utm_campaign=RozgolosTelegram&utm_content=RozgolosTelegram&utm_term=RozgolosTelegram")]
    ])

    await update.message.reply_text(
        "⬇️ Завантажити застосунок або відвідати сайт:",
        reply_markup=buttons
    )

    await update.message.reply_text("🙏 Дякуємо! З вами зв’яжеться наш консультант.")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("❌ cancel() triggered")
    await update.message.reply_text("❌ Операцію скасовано.")
    return ConversationHandler.END


async def main():
    print("🚀 Bot is starting...")
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            AWAIT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, await_name)],
            FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_full_name)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    await app.run_polling()


if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())
"""

# Збережемо файл
output_path = Path("/mnt/data/rozgolos_bot_fixed.py")
output_path.write_text(code, encoding="utf-8")

output_path.name
