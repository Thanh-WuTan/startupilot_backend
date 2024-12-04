from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..models.status_model import Status
from .serializers import StatusSerializer

class StatusListView(APIView):
    """
    Retrieve a list of all statuses.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        statuses = Status.objects.all()
        serializer = StatusSerializer(statuses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class StatusCreateView(APIView):
    """
    Create a new status.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Extract and clean the name from the request data
        name = ' '.join(request.data.get('name', '').strip().lower().split())

        # Check if a status with the same name already exists
        if Status.objects.filter(name=name).exists():
            return Response({'detail': 'A status with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new status
        status_instance = Status.objects.create(name=name)

        # Serialize and return the new status
        serializer = StatusSerializer(status_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
