from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    filters
)

from analysis_by_dialogflow import analyse_message


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        analyse_message(update.message.text, update.message.chat_id)
    )


def bot_start(telegram_main_bot_token):
    application = Application.builder().token(
        telegram_main_bot_token
    ).build()
    application.add_handler(
        MessageHandler(filters.TEXT, echo)
    )
    application.run_polling(allowed_updates=Update.ALL_TYPES)
