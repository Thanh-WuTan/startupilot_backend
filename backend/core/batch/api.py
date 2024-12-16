from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

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
        # Initialize the serializer with the request data
        serializer = BatchSerializer(data=request.data)

        # Validate the data
        if serializer.is_valid():
            # Ensure the batch name is cleaned and check for duplicates
            name = ' '.join(serializer.validated_data.get('name', '').strip().split())
            if Batch.objects.filter(name=name).exists():
                return Response({'detail': 'A batch with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            # Save the new batch
            serializer.save(name=name)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Return errors if the data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BatchDetailView(APIView):
    """
    Retrieve, update, or delete batch information by its primary key (UUID).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        View batch details by ID.
        """
        batch = get_object_or_404(Batch, pk=pk)
        serializer = BatchSerializer(batch)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Update batch information.
        """
        batch = get_object_or_404(Batch, pk=pk)
        serializer = BatchSerializer(batch, data=request.data, partial=True)

        if serializer.is_valid():
            # Ensure the updated name is unique (if provided)
            name = serializer.validated_data.get('name', None)
            if name:
                cleaned_name = ' '.join(name.strip().split())
                if Batch.objects.filter(name=cleaned_name).exclude(pk=pk).exists():
                    return Response({'detail': 'A batch with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

                serializer.validated_data['name'] = cleaned_name

            # Save the updates
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a batch by its primary key.
        """
        batch = get_object_or_404(Batch, pk=pk)

        # Delete the batch instance
        batch.delete()
        return Response({'detail': 'Batch deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
