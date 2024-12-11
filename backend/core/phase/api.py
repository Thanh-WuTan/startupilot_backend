from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from ..models.phase_model import Phase
from .serializers import PhaseSerializer

class PhaseListView(APIView):
    """
    Retrieve a list of all statuses.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        statuses = Phase.objects.all()
        serializer = PhaseSerializer(statuses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PhaseCreateView(APIView):
    """
    Create a new phase.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Extract and clean the name from the request data
        name = ' '.join(request.data.get('name', '').strip().split())
        
        # Check if a phase with the same name already exists
        if Phase.objects.filter(name=name).exists():
            return Response({'detail': 'A phase with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new phase
        phase = Phase.objects.create(name=name)

        # Serialize and return the new phase
        serializer = PhaseSerializer(phase)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
