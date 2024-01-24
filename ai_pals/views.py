from rest_framework.decorators import api_view
from rest_framework.response import Response
from openai import OpenAI


client = OpenAI()


def generate_image_prompt(characteristics: list[str], description: str) -> str:
    """Given a list of characteristics and a description for a creature,
    generate an image prompt for the OpenAI API."""

    characteristic_string = ", ".join(characteristics)

    return f"Generate a cute illustration of a creature with the following characteristics: {characteristic_string}. Here is a description of the creature: {description}"


@api_view(["POST"])
def new_character(request):
    """Create a new character."""

    characteristics = request.data.get("characteristics", [])

    if not characteristics:
        return Response({"message": "Bad request: Invalid form data"}, status=400)

    description_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You generate a description of a creature from a list of characteristics provided by the user.",
            },
            {
                "role": "user",
                "content": ", ".join(characteristics),
            },
        ],
    )

    description = description_response.choices[0].message.content

    if not description:
        return Response({"error": "Something went wrong"}, status=500)

    image_prompt = generate_image_prompt(characteristics, description)

    image_response = client.images.generate(
        model="dall-e-3", prompt=image_prompt, size="1024x1024", n=1, quality="standard"
    )

    image_url = image_response.data[0].url

    if not image_url:
        return Response({"error": "Something went wrong"}, status=500)

    return Response({"description": description, "image_url": image_url})
