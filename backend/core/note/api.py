from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import IsAuthenticated, AllowAny 
from .serializers import NoteSerializer  # Assuming you have a serializer for the Note model
from ..models import Startup, Person, Note

class NoteCreateView(APIView):
    """
    Create a new note for a specified content type (Startup or Person).
    """
    permission_classes = [IsAuthenticated]  # Adjust permission classes as needed

    def post(self, request):
        content = request.data.get('content')
        content_type_id = request.data.get('content_type')
        object_id = request.data.get('object_id')

        if not content or not content_type_id or not object_id:
            return Response({"error": "Content, content_type, and object_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the ContentType object
        try:
            content_type = ContentType.objects.get(id=content_type_id)
        except ContentType.DoesNotExist:
            return Response({"error": "Invalid content_type."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the object_id exists in the corresponding model
        if content_type.model == 'startup':
            try:
                # Validate the startup object exists
                startup = Startup.objects.get(id=object_id)
            except Startup.DoesNotExist:
                return Response({"error": "Startup not found."}, status=status.HTTP_400_BAD_REQUEST)
        elif content_type.model == 'person':
            try:
                # Validate the person object exists
                person = Person.objects.get(id=object_id)
            except Person.DoesNotExist:
                return Response({"error": "Person not found."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Unsupported content type."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the note
        note = Note.objects.create(
            content=content,
            content_type=content_type,
            object_id=object_id
        )

        # Serialize and return the created note
        serializer = NoteSerializer(note)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class NoteDetailView(APIView):
    """
    Retrieve a note's details by its primary key (UUID).
    """
    permission_classes = [AllowAny]  # Adjust permission classes as needed

    def get(self, request, pk):
        # Fetch the note instance by its UUID
        note = get_object_or_404(Note, pk=pk)
        
        # Serialize the note instance
        serializer = NoteSerializer(note)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk): 
        note = get_object_or_404(Note, pk=pk)
         
        note.delete()
        
        return Response({"detail": "Note deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, pk):
        # Fetch the note instance by its UUID
        note = get_object_or_404(Note, pk=pk)
        
        # Deserialize the request data and validate it
        serializer = NoteSerializer(note, data=request.data, partial=False)
        
        if serializer.is_valid():
            # Save the updated note
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)