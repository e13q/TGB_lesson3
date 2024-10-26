import random
import os
import logging

from environs import Env
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from analysis_by_dialogflow import analyse_message
from bot_logging import setup_logger, exception_out


def echo(event, vk_api):
    analyse_response = analyse_message(
        event.text, event.user_id
    )
    if analyse_response.query_result.intent.is_fallback:
        return None
    vk_api.messages.send(
        user_id=event.user_id,
        message=analyse_response.query_result.fulfillment_text,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    env = Env()
    env.read_env()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = env.str(
        'GOOGLE_APPLICATION_CREDENTIALS'
    )
    os.environ['DIALOGFLOW_PROJECT_ID'] = env.str('DIALOGFLOW_PROJECT_ID')
    vk_session = vk.VkApi(token=env.str('VK_GROUP_TOKEN'))
    setup_logger(
        env.str('TELEGRAM_LOGGER_BOT_TOKEN'),
        env.str('TELEGRAM_CHAT_ID')
    )
    logging.info('Бот для группы VK успешно запущен!')
    while (True):
        try:
            vk_api = vk_session.get_api()
            longpoll = VkLongPoll(vk_session)
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    echo(event, vk_api)
        except Exception as e:
            exception_out(
                'Шеф, у нас неожиданная ошибка: ', e
            )
