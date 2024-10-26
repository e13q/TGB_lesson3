import logging
import os

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from environs import Env
from google.cloud import dialogflow



logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(
        os.environ['DIALOGFLOW_PROJECT_ID'],
        update.message.chat_id
    )

    text_input = dialogflow.TextInput(text=update.message.text, language_code='RU')

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
        
    await update.message.reply_text(str(response.query_result.fulfillment_text))


def main():
    env = Env()
    env.read_env()
    application = Application.builder().token(
        env.str('TELEGRAM_MAIN_BOT_TOKEN')
    ).build()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = env.str('GOOGLE_APPLICATION_CREDENTIALS')
    os.environ['DIALOGFLOW_PROJECT_ID'] = env.str('DIALOGFLOW_PROJECT_ID')
    application.add_handler(
        MessageHandler(filters.TEXT, echo)
    )
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()