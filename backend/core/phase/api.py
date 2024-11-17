from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
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