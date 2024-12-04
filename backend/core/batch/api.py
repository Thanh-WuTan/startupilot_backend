from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from ..models.batch_model import Batch
from .serializers import BatchSerializer

class BatchListView(APIView):
    """
    Retrieve a list of batches.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # Fetch all batches from the database
        batches = Batch.objects.all()

        # Serialize the batches data
        serializer = BatchSerializer(batches, many=True)

        # Return the response with the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class BatchCreateView(APIView):
    """
    Create a new batch.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Extract and clean the name from the request data
        name = ' '.join(request.data.get('name', '').strip().lower().split())

        # Check if a batch with the same name already exists
        if Batch.objects.filter(name=name).exists():
            return Response({'detail': 'A batch with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new batch
        batch_instance = Batch.objects.create(name=name)

        # Serialize and return the new batch
        serializer = BatchSerializer(batch_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
