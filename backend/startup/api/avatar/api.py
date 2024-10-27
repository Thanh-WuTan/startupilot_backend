# api.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .service import create_avatar
from .serializers import AvatarSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

@api_view(['POST'])
@permission_classes([AllowAny])
def upload_avatar(request):
    """
    Handle the upload of a new avatar file.
    """
    file = request.FILES.get('avatar')
    if not file:
        return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

    # Use the service function to create an Avatar instance
    avatar_instance = create_avatar(file)

    # Serialize the instance for response
    serializer = AvatarSerializer(avatar_instance)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


