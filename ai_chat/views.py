from rest_framework.decorators import api_view
from rest_framework.response import Response
from decouple import config
import openai

openai.api_key = config("OPENAI_API_KEY")

@api_view(['POST'])
def chat_api(request):
    """A simple endpoint that returns {success: true} on POST request."""
    return Response({"success": True})
