from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from ...models.priority_model import Priority
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
 