from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import json
import openai
from decouple import config

openai.api_key = config("OPENAI_API_KEY")


# Function to verify reCAPTCHA token (You need to implement this)
def verify_token(recaptcha_token: str) -> dict:
    # TODO: Implement the reCAPTCHA verification logic
    return {"success": True}


@api_view(['POST'])
def chat_api(request):
    """Handle chat completions using OpenAI API."""

    if request.method != 'POST':
        return Response({"message": "Method not allowed"}, status=405)

    try:
        request_data = json.loads(request.body)
        client_messages = request_data.get('clientMessages', [])
        recaptcha_token = request_data.get('recaptchaToken', '')

        if not client_messages or not recaptcha_token:
            return Response({"message": "Bad request: Invalid form data"}, status=400)

        verification = {}
        if settings.DEBUG:
            verification = {
                "success": True,
                "challenge_ts": "2020-05-01T00:00:00Z",
                "hostname": "chriskumm.com",
            }
        else:
            verification = verify_token(recaptcha_token)

        if not verification.get("success"):
            return Response({"message": "Bad request: reCAPTCHA token failed verification."}, status=400)

        # TODO: Get this value from a Django model
        system_message_content = "You are a web developer named Chris."
        system_message = {
            "role": "system",
            "content": system_message_content
        }
        messages = [system_message, *client_messages]

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )

        result = completion.choices[0].message.content
        if not result:
            return Response({"error": "Something went wrong"}, status=500)

        return Response({"result": result}, status=200)

    except Exception as e:
        print(f"An error occurred: {e}")
        return Response({"message": "Internal server error"}, status=500)
