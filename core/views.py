from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import InquirySerializer


@api_view(['POST'])
def submit_inquiry(request):
    serializer = InquirySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': 'message saved'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
