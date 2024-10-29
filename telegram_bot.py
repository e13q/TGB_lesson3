import logging
from functools import partial

from environs import Env
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from google.oauth2 import service_account

from working_with_dialogflow import request_to_dialogflow
from bot_logging import setup_logger, exception_out


def echo(update: Update, context: CallbackContext, credentials, project_id):
    analyse_response = request_to_dialogflow(
        update.message.text,
        f'tg-{update.message.chat_id}',
        credentials,
        project_id
    )
    update.message.reply_text(
        analyse_response.query_result.fulfillment_text
    )


if __name__ == "__main__":
    env = Env()
    env.read_env()
    credentials = service_account.Credentials.from_service_account_file(
        env.str('GOOGLE_APPLICATION_CREDENTIALS')
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
            echo_with_dialogflow_creds = partial(
                echo,
                credentials=credentials,
                project_id=project_id
            )
            dispatcher.add_handler(
                MessageHandler(
                    Filters.text & ~Filters.command,
                    echo_with_dialogflow_creds
                )
            )
            logging.info('Бот Telegram успешно запущен!')
            updater.start_polling()
            updater.idle()
        except Exception as e:
            exception_out(
                'Шеф, у нас неожиданная ошибка: ', e
            )
