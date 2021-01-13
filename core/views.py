import requests
import json

from django.conf import settings
from django.core.mail import mail_managers

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .serializers import InquirySerializer


def ip_is_abusive(ip_addr, api_key, threshold=90):
    """Check if the given IP has an abuse confidence score greater than the given threshold percentage."""

    # The AbuseIPDB API endpoint
    url = 'https://api.abuseipdb.com/api/v2/check'

    querystring = {
        'ipAddress': ip_addr,
        'maxAgeInDays': '90'
    }

    headers = {
        'Accept': 'application/json',
        'Key': api_key,
    }

    response = requests.request(method='GET', url=url, headers=headers, params=querystring)
    data = json.loads(response.text)
    return data['data']['abuseConfidenceScore'] > threshold


@api_view(['POST'])
@permission_classes([AllowAny])
def submit_inquiry(request):
    """Process messages sent from the front end form."""
    serializer = InquirySerializer(data=request.data)
    if serializer.is_valid():

        # Filter messages from abusive IP addresses
        if ip_is_abusive(request.META['REMOTE_ADDR'], settings.ABUSEIPDB_API_KEY):
            return Response(
                {'error': 'Your IP has been blocked from sending message because it has been'
                          ' reported to have a high risk of abuse. If you think this is a'
                          ' mistake, try messaging from another network and let me know.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer.save(ip_address=request.META['REMOTE_ADDR'])

        mail_managers(
            f'ChrisKumm.com: message from {serializer.validated_data["email"]}',
            serializer.validated_data['message']
        )

        return Response({'success': 'message saved'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
