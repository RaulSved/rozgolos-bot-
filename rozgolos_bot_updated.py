import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext, ContextTypes, filters

TOKEN = "7859058780:AAHvBh7w7iNvc8KLE9Eq0RMfmjdwKYuAFOA"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

WELCOME_TEXT = "👋 Введіть Прізвище та ім’я"
IMAGE_URL = "https://rozgolos.online/static/telegram-start.jpg"

keyboard = [
    [
        InlineKeyboardButton("📲 Android", url="https://play.google.com/store/apps/details?id=com.rozgolos"),
        InlineKeyboardButton("🍏 iOS", url="https://apps.apple.com/app/id6739999117")
    ],
    [
        InlineKeyboardButton("🌐 Офіційний сайт", url="https://rozgolos.online/bronyuvannya?utm_source=fb&utm_medium=paid_social&utm_campaign=RozgolosTelegram&utm_content=RozgolosTelegram&utm_term=RozgolosTelegram&fbclid=fbclid")
    ],
    [
        InlineKeyboardButton("✅ Продовжити", callback_data="continue")
    ]
]

reply_markup = InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    await context.bot.send_photo(
        chat_id=chat_id,
        photo=IMAGE_URL,
        caption=WELCOME_TEXT,
        reply_markup=reply_markup
    )

async def handle_continue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("Дякуємо, заявка прийнята! Очікуйте дзвінка від нашого менеджера.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Тут можна зберігати дані або відправляти адміну
    await update.message.reply_text("✅ Дані прийнято. Натисніть 'Продовжити' для завершення.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_text))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_text))
    app.add_handler(MessageHandler(filters.VIDEO, handle_text))
    app.add_handler(MessageHandler(filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_TITLE, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_PHOTO, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.DELETE_CHAT_PHOTO, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.GROUP_CHAT_CREATED, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.SUPERGROUP_CHAT_CREATED, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.CHANNEL_CHAT_CREATED, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.MIGRATE_TO_CHAT_ID, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.MIGRATE_FROM_CHAT_ID, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.PINNED_MESSAGE, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.MESSAGE_AUTO_DELETE_TIMER_CHANGED, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.FORUM_TOPIC_CREATED, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.FORUM_TOPIC_CLOSED, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.FORUM_TOPIC_REOPENED, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.GENERAL_FORUM_TOPIC_HIDDEN, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.GENERAL_FORUM_TOPIC_UNHIDDEN, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.WRITE_ACCESS_ALLOWED, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.USER_SHARED, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.CHAT_SHARED, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.STORY, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.BOOST_ADDED, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.BOOST_REMOVED, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.GIVEAWAY_CREATED, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.GIVEAWAY_COMPLETED, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.GIVEAWAY_WON, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    
    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    
    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    
    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    
    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    
    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    
    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    
    app.add_handler(MessageHandler(filters.ALL, handle_text))
    
    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.add_handler(MessageHandler(filters.ALL, handle_text))
    
    app.add_handler(MessageHandler(filters.ALL, handle_text))

    app.run_polling()

if __name__ == '__main__':
    main()
