import json
import logging
from typing import NamedTuple

from channels.generic.websocket import WebsocketConsumer
from decouple import config
import openai


logger = logging.getLogger(__name__)


client = openai.OpenAI(api_key=config("OPENAI_API_KEY"))


logger.info(f"OpenAI API client created: {client.user_agent}")


# TODO: Load these from a file or database
allowed_characteristics = [
    "cute",
    "scary",
    "goofy",
    "noble",
    "tiny",
    "small",
    "medium",
    "large",
    "giant",
    "dog",
    "insect",
    "dinosaur",
    "bird",
    "fish",
    "flight",
    "walking",
    "swimming",
    "desert",
    "sea",
    "jungle",
]


class ClientMessage(NamedTuple):
    characteristics: list[str]


class CritterGenerationConsumer(WebsocketConsumer):
    """Generates a critter description and image based on user input."""

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json: ClientMessage = json.loads(text_data)

        # Description Generation

        characteristics = text_data_json["characteristics"]

        # Validate the characteristics

        invalid_characteristics = []
        for characteristic in characteristics:
            if characteristic not in allowed_characteristics:
                invalid_characteristics.append(characteristic)
        if invalid_characteristics:
            self.send(
                text_data=json.dumps(
                    {
                        "type": "error",
                        "error": f"Invalid characteristics: {', '.join(invalid_characteristics)}",
                    }
                )
            )
            return

        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a critter description generator. Whenever a user sends a list of characteristics, you describe a critter with those characteristics.",
                },
                {"role": "user", "content": ", ".join(characteristics)},
            ],
            stream=True,
        )

        description = ""

        for chunk in stream:
            description += chunk.choices[0].delta.content or ""
            self.send(
                text_data=json.dumps(
                    {
                        "type": "completion_chunk",
                        "content": chunk.choices[0].delta.content or "",
                        "finish_reason": chunk.choices[0].finish_reason,
                    }
                )
            )

        # Image Generation

        try:
            image_response = client.images.generate(
                model="dall-e-3",
                prompt=description,
                size="1024x1024",
                n=1,
                quality="standard",
            )
        except openai.BadRequestError as e:
            # You might end up here if an image violates OpenAI's content policy
            self.send(
                text_data=json.dumps(
                    {
                        "type": "error",
                        "error": str("An error occurred while generating the image."),
                    }
                )
            )
            return

        image_url = image_response.data[0].url

        self.send(
            text_data=json.dumps(
                {
                    "type": "image_generation_result",
                    "image_url": image_url,
                }
            )
        )
