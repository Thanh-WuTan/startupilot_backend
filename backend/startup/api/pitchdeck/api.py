from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .service import create_pitchdeck
from .serializers import PitchdeckSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser


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
        
        # Use the service function to create a Pitchdeck instance
        pitchdeck_instance = create_pitchdeck(file)
        
        # Serialize the instance for response
        serializer = PitchdeckSerializer(pitchdeck_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)