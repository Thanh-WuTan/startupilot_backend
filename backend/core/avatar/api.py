import re

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import AvatarSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from .service import upload_avatar


MAX_AVATAR_SIZE = 5 * 1024 * 1024 # 5MB
VALID_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/jpg'] # Only JPEG and PNG images allowed
FILENAME_REGEX = r'^[a-zA-Z0-9]+$' # Only alphanumeric characters allowed

class UploadAvatarView(APIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        """
        Handle the upload of a new avatar url.
        """
        file = request.FILES.get('avatar')
        if not file:
            return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # check if the file is an image
        if file.content_type not in VALID_IMAGE_TYPES:
            return Response({'error': 'Invalid file type. Only JPEG, PNG and JPG images are supported.'}, status=status.HTTP_400_BAD_REQUEST)       
        
        # check if the file is too large
        if file.size > MAX_AVATAR_SIZE:
            return Response({'error': 'File too large. Size should not exceed 5MB.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # validate file name with regex: not containing special characters, spaces, etc.
        if re.match(FILENAME_REGEX, file.name):
            return Response({'error': 'Invalid file name. Avoid special characters and spaces.'}, status=status.HTTP_400_BAD_REQUEST)        
        
        # Use the service function to create an Avatar instance
        avatar_instance = upload_avatar(file)
        
        # Serialize the instance for response
        serializer = AvatarSerializer(avatar_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)