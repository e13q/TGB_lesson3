import random
import logging

from environs import Env
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from google.oauth2 import service_account

from working_with_dialogflow import request_to_dialogflow
from bot_logging import setup_logger, exception_out


def echo(event, vk_api, credentials, project_id):
    analyse_response = request_to_dialogflow(
        event.text,
        f'vk-{event.user_id}',
        credentials,
        project_id
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
    credentials = service_account.Credentials.from_service_account_file(
        env.str('GOOGLE_APPLICATION_CREDENTIALS')
    )
    project_id = env.str('DIALOGFLOW_PROJECT_ID')
    vk_session = vk.VkApi(token=env.str('VK_GROUP_TOKEN'))
    setup_logger(
        env.str('TELEGRAM_LOGGER_BOT_TOKEN_VK'),
        env.str('TELEGRAM_CHAT_ID')
    )
    while (True):
        try:
            vk_api = vk_session.get_api()
            longpoll = VkLongPoll(vk_session)
            logging.info('Бот для группы VK успешно запущен!')
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    echo(event, vk_api, credentials, project_id)
        except Exception as e:
            exception_out(
                'Шеф, у нас неожиданная ошибка: ', e
            )
