from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Pizza
from .serializers import PizzaSerializer


@api_view(['GET'])
def home(request):
    # TODO: Delete this example home view.
    pizzas = Pizza.objects.all()

    serializer = PizzaSerializer(pizzas, many=True)
    return Response(serializer.data)
