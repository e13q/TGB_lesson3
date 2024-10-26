import os
import argparse
import json

import requests
from environs import Env
from google.cloud import dialogflow


def load_intents(intents: list, dataflow_project_id):
    intents_client = dialogflow.IntentsClient()
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
        response = intents_client.create_intent(
            request={"parent": parent, "intent": intent}
        )
        print("Intent created: {}".format(response))


def request_json(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


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
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = env.str(
        "GOOGLE_APPLICATION_CREDENTIALS"
    )
    dataflow_project_id = env.str('DIALOGFLOW_PROJECT_ID')
    if url:
        intents = request_json(url)
    elif path:
        intents = load_json(path)
    else:
        print('Specify path to data file using one of arguments: --url, --path')
        exit()
    load_intents(intents, dataflow_project_id)
