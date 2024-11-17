from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from ...models.batch_model import Batch
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