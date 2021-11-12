from .models import Inquiry

from rest_framework import serializers


class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = ("name", "email", "message")
