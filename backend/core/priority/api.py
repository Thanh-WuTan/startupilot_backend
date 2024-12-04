from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..models.priority_model import Priority
from .serializers import PrioritySerializer

class PriorityListView(APIView):
    """
    Retrieve a list of all priorities.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        priorities = Priority.objects.all()
        serializer = PrioritySerializer(priorities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PriorityCreateView(APIView):
    """
    Create a new priority.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Extract and clean the name from the request data
        name = ' '.join(request.data.get('name', '').strip().lower().split())

        # Check if a priority with the same name already exists
        if Priority.objects.filter(name=name).exists():
            return Response({'detail': 'A priority with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new priority
        priority = Priority.objects.create(name=name)

        # Serialize and return the new priority
        serializer = PrioritySerializer(priority)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
