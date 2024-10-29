import os
import logging

from environs import Env
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

from analysis_by_dialogflow import analyse_message
from bot_logging import setup_logger, exception_out


def echo(update: Update, context: CallbackContext, project_id) -> None:
    analyse_response = analyse_message(
        update.message.text, update.message.chat_id, project_id
    )
    update.message.reply_text(
        analyse_response.query_result.fulfillment_text
    )


if __name__ == "__main__":
    env = Env()
    env.read_env()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = env.str(
        'GOOGLE_APPLICATION_CREDENTIALS'
    )
    project_id = env.str('DIALOGFLOW_PROJECT_ID')
    main_bot_token = env.str('TELEGRAM_MAIN_BOT_TOKEN')
    setup_logger(
        env.str('TELEGRAM_LOGGER_BOT_TOKEN_TG'),
        env.str('TELEGRAM_CHAT_ID'))
    while (True):
        try:
            updater = Updater(main_bot_token)
            dispatcher = updater.dispatcher
            dispatcher.add_handler(
                MessageHandler(
                    Filters.text & ~Filters.command,
                    echo(project_id=project_id)
                )
            )
            logging.info('Бот Telegram успешно запущен!')
            updater.start_polling()
            updater.idle()
        except Exception as e:
            exception_out(
                'Шеф, у нас неожиданная ошибка: ', e
            )
