import json

from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from decouple import config
import openai

# TODO: Is this where the client should be defined?
client = openai.OpenAI(api_key=config("OPENAI_API_KEY"))


def construct_critter_description_prompt(form_data) -> str:
    # TODO: process the form data to construct the prompt
    return "You are a critter in a fantasy world. Describe yourself."


class CritterDescriptionConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        prompt = construct_critter_description_prompt(text_data_json)

        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )

        for chunk in stream:
            print(chunk.choices[0].delta.content, end="")
            self.send(
                text_data=json.dumps(
                    {
                        "content": chunk.choices[0].delta.content or "",
                        "finish_reason": chunk.choices[0].finish_reason,
                    }
                )
            )
