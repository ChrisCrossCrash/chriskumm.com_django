from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .serializers import InquirySerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def submit_inquiry(request):
    serializer = InquirySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': 'message saved'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
