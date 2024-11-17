from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import AvatarSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from .service import create_avatar


class UploadAvatarView(APIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        """
        Handle the upload of a new pitchdeck file.
        """
        file = request.FILES.get('avatar')
        if not file:
            return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Use the service function to create a Pitchdeck instance
        avatar_instance = create_avatar(file)
        
        # Serialize the instance for response
        serializer = AvatarSerializer(avatar_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)