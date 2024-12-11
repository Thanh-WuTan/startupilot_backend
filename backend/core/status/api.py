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
