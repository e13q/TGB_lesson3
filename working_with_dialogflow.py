from google.cloud import dialogflow


def request_to_dialogflow(message, unique_id, credentials, project_id):
    session_client = dialogflow.SessionsClient(credentials=credentials)
    session = session_client.session_path(
        project_id,
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
