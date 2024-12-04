import re
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .service import upload_file, sanitize_filename, generate_random_string

MAX_AVATAR_SIZE = 5 * 1024 * 1024  # 5MB
VALID_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/jpg']  # Only JPEG and PNG images allowed
VALID_PDF_TYPES = ['application/pdf']  # Only PDF files allowed
FILENAME_REGEX = r'^[a-zA-Z0-9._]+$'  # Allow alphanumeric characters, dot and underscore

class UploadFileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        file_type = request.data.get('type')

        if not file:
            return Response({'detail': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        if not file_type or file_type not in ['avatar', 'pitchdeck']:
            return Response({'detail': 'Invalid type. It must be either "avatar" or "pitchdeck".'}, status=status.HTTP_400_BAD_REQUEST)

        # File validation based on type
        if file_type == 'avatar':
            if file.content_type not in VALID_IMAGE_TYPES:
                return Response({'error': 'Invalid file type for avatar. Only JPEG, PNG, and JPG images are supported.'}, status=status.HTTP_400_BAD_REQUEST)
            if file.size > MAX_AVATAR_SIZE:
                return Response({'error': 'File too large for avatar. Size should not exceed 5MB.'}, status=status.HTTP_400_BAD_REQUEST)

        elif file_type == 'pitchdeck':
            if file.content_type not in VALID_PDF_TYPES:
                return Response({'error': 'Invalid file type for pitchdeck. Only PDF files are supported.'}, status=status.HTTP_400_BAD_REQUEST)

        # Sanitize the filename and generate a unique name if needed
        sanitized_filename = sanitize_filename(file.name)
        if not re.match(FILENAME_REGEX, sanitized_filename):
            return Response({'error': 'Invalid file name. Only alphanumeric characters, dot, and underscore are allowed.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a unique name for the file
        unique_filename = f"{generate_random_string()}_{sanitized_filename}"

        # Upload file using the service
        file_url = upload_file(file, file_type, unique_filename)

        return Response({'file_url': file_url}, status=status.HTTP_200_OK)
