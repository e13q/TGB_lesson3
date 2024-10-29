import argparse
import json

import requests
from environs import Env
from google.cloud import dialogflow
from google.oauth2 import service_account


def load_intents(intents: list, credentials, dataflow_project_id):
    intents_client = dialogflow.IntentsClient(credentials=credentials)
    parent = dialogflow.AgentsClient.agent_path(
       dataflow_project_id
    )
    for name, intent in intents.items():
        training_phrases = []
        for training_phrases_part in intent['questions']:
            part = dialogflow.Intent.TrainingPhrase.Part(
                text=training_phrases_part
            )
            training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
            training_phrases.append(training_phrase)
        text = dialogflow.Intent.Message.Text(text=[intent['answer']])
        message = dialogflow.Intent.Message(text=text)
        intent = dialogflow.Intent(
            display_name=name,
            training_phrases=training_phrases,
            messages=[message]
        )
        intents_client.create_intent(
            request={"parent": parent, "intent": intent}
        )


def load_parser():
    parser = argparse.ArgumentParser(
        description='Upload JSON intents to DialogFlow by API'
    )
    parser.add_argument(
        '--path',
        help='Path to .json',
        nargs='?'
    )
    parser.add_argument(
        '--url',
        help='Url to .json',
        nargs='?'
    )
    return parser


if __name__ == '__main__':
    parser = load_parser()
    parser = parser.parse_args()
    path = parser.path
    url = parser.url
    env = Env()
    env.read_env()
    credentials = service_account.Credentials.from_service_account_file(
        env.str('GOOGLE_APPLICATION_CREDENTIALS')
    )
    dataflow_project_id = env.str('DIALOGFLOW_PROJECT_ID')
    intents = None
    if url or path:
        if url:
            response = requests.get(url)
            response.raise_for_status()
            intents = response.json()
        elif path:
            with open(path, "r", encoding="utf-8") as file:
                intents = json.load(file)
        load_intents(intents, credentials, dataflow_project_id)
        print("Intents created")
    else:
        print('Specify path to data file using one of arguments: --url, --path') # noqa
