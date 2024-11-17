from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from ...models import Advisor, Startup
from .serializers import AdvisorSerializer

class AdvisorListView(APIView):
    """
    List all advisors and their associated mentorships.
    """
    permission_classes = [AllowAny]  # Adjust permission classes as needed

    def get(self, request):
        advisors = Advisor.objects.all()
        serializer = AdvisorSerializer(advisors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdvisorDetailView(APIView):
    """
    Retrieve the details of a specific advisor by their primary key (UUID).
    """
    permission_classes = [AllowAny]  # Adjust permission classes as needed

    def get(self, request, pk):
        advisor = get_object_or_404(Advisor, pk=pk)
        serializer = AdvisorSerializer(advisor)
        return Response(serializer.data, status=status.HTTP_200_OK)
