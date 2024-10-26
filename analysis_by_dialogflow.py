import os

from google.cloud import dialogflow


def analyse_message(message, unique_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(
        os.environ['DIALOGFLOW_PROJECT_ID'],
        unique_id
    )
    text_input = dialogflow.TextInput(
        text=message,
        language_code='RU'
    )
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response
