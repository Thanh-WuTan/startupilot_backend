import re

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .service import upload_pitchdeck
from .serializers import PitchdeckSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

MAX_PITCHDECK_FILE_SIZE = 10 * 1024 * 1024  # 10MB
VALID_PITCHDECK_TYPES = ['application/pdf']  # Only PDF files allowed
FILENAME_REGEX = r'^[a-zA-Z0-9]+$'  # Only alphanumeric characters allowed

class UploadPitchdeckView(APIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        """
        Handle the upload of a new pitchdeck file.
        """
        file = request.FILES.get('pitchdeck')
        if not file:
            return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # check if the file is a PDF
        if file.content_type not in VALID_PITCHDECK_TYPES:
            return Response({'error': 'Invalid file type. Only PDF files are supported.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # check if the file is too large
        if file.size > MAX_PITCHDECK_FILE_SIZE:
            return Response({'error': 'File too large. Size should not exceed 10MB.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # validate file name with regex: not containing special characters, spaces, etc.
        if re.match(FILENAME_REGEX, file.name):
            return Response({'error': 'Invalid file name. Avoid special characters and spaces.'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        # Use the service function to create a Pitchdeck instance
        pitchdeck_instance = upload_pitchdeck(file)
        
        # Serialize the instance for response
        serializer = PitchdeckSerializer(pitchdeck_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)