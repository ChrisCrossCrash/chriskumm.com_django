from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def index(request):
    """Index page for the API."""
    return Response({"message": "Welcome to the AI Chat API!"})
