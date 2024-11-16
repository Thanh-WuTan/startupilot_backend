from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, filters
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from ...models import Startup
from .serializers import StartupSerializer
from django.db.models import Case, When, Value, IntegerField
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from rest_framework.filters import SearchFilter

from .service import create_startup, get_startup_by_id


from .filter import StartupFilter

class StartupListView(generics.ListAPIView):
    queryset = Startup.objects.all()
    permission_classes = [AllowAny]
    serializer_class = StartupSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = StartupFilter
    search_fields = ['$name'] 

class StartupDetailView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a single startup.
    """
    queryset = Startup.objects.all()
    serializer_class = StartupSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_startup_by_id(pk)

    def retrieve(self, request, *args, **kwargs):
        startup = self.get_object()
        if not startup:
            return Response({'error': 'Startup not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(startup)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        startup = self.get_object()
        if not startup:
            return Response({'error': 'Startup not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        try:
            startup.delete()
            result = create_startup(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        startup = self.get_object()
        if not startup:
            return Response({'error': 'Startup not found'}, status=status.HTTP_404_NOT_FOUND)

        startup.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
