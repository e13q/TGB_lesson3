import os

from environs import Env

from telegram_bot import bot_start


if __name__ == "__main__":
    env = Env()
    env.read_env()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = env.str(
        'GOOGLE_APPLICATION_CREDENTIALS'
    )
    os.environ['DIALOGFLOW_PROJECT_ID'] = env.str('DIALOGFLOW_PROJECT_ID')
    bot_start(env.str('TELEGRAM_MAIN_BOT_TOKEN'))
