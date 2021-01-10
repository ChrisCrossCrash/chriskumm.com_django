from .models import Pizza, Topping

from rest_framework import serializers


class ToppingSerializer(serializers.ModelSerializer):
    # TODO: Delete this ToppingSerializer example.

    class Meta:
        model = Topping
        fields = ('name', 'pk')


class PizzaSerializer(serializers.ModelSerializer):
    # TODO: Delete this PizzaSerializer example.

    # You can nest a serializer.
    toppings = ToppingSerializer(many=True)

    # You can also serialize model methods.
    topping_count = serializers.IntegerField(source='get_topping_count')

    class Meta:
        model = Pizza
        fields = ('name', 'price', 'pk', 'topping_count', 'toppings')
