from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from ..models.phase_model import Phase
from .serializers import PhaseSerializer

class PhaseListView(APIView):
    """
    Retrieve a list of all phases.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        phases = Phase.objects.all()
        serializer = PhaseSerializer(phases, many=True)
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

class PhaseDetailView(APIView):
    """
    Retrieve, update, or delete a specific phase by its primary key (PK).
    """
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request, pk):
        """
        Retrieve details of a specific phase.
        """
        phase = get_object_or_404(Phase, pk=pk)
        serializer = PhaseSerializer(phase)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Update a specific phase.
        """
        phase = get_object_or_404(Phase, pk=pk)
        serializer = PhaseSerializer(phase, data=request.data, partial=True)

        if serializer.is_valid():
            # Check if the updated name is unique
            name = serializer.validated_data.get('name', phase.name).strip()
            if Phase.objects.filter(name=name).exclude(pk=pk).exists():
                return Response({'detail': 'A phase with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            # Save the updated phase
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific phase.
        """
        phase = get_object_or_404(Phase, pk=pk)
        phase.delete()
        return Response({'detail': 'Phase deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
