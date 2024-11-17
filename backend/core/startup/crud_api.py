from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import StartupSerializer, ManyStartupSerializer 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from ..models import Startup, Note

from .filter import StartupFilter

class StartupListView(generics.ListAPIView):
    queryset = Startup.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ManyStartupSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = StartupFilter
    search_fields = ['$name'] 



class StartupDetailView(APIView):
    """
    Retrieve a startup's details by its primary key (UUID).
    """
    permission_classes = [AllowAny]  # Adjust permission classes as needed

    def get(self, request, pk):
        # Fetch the startup instance by its UUID
        startup = Startup.objects.filter(id=pk).first()
        
        if startup is None:
            return Response({"detail": "Startup not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the startup instance
        serializer = StartupSerializer(startup)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        startup = Startup.objects.filter(id=pk).first()
        
        if not startup:
            return Response({"detail": "Startup not found."}, status=status.HTTP_404_NOT_FOUND)
        
        notes = Note.objects.filter(content_type__model='startup', object_id=pk)
        notes.delete()  # Delete all related notes
        # Delete the startup instance
        startup.delete()
        
        # Return a success message with status 204 (No Content), indicating successful deletion
        return Response({"detail": "Startup deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        startup = Startup.objects.filter(id=pk).first()
        
        if not startup:
            return Response({"detail": "Startup not found."}, status=status.HTTP_404_NOT_FOUND)
        
        