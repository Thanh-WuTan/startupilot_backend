from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
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
        content_type_str = request.data.get('content_type')  # Expecting 'startup' or 'person'
        object_id = request.data.get('object_id')

        if not content or not content_type_str or not object_id:
            return Response({"error": "Content, content_type, and object_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Map the string content_type to the ContentType model
        if content_type_str == 'startup':
            content_type = ContentType.objects.get_for_model(Startup)
        elif content_type_str == 'member':
            content_type = ContentType.objects.get_for_model(Person)
        else:
            return Response({"error": "Invalid content_type. Must be 'startup' or 'member'."}, status=status.HTTP_400_BAD_REQUEST)

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
        content = request.data.get('content')

        if not content:
            return Response({"error": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the note's content
        note.content = content

        # Optionally, validate the content length if necessary
        try:
            note.clean()  # This will call the clean method to ensure no word limit is exceeded
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Save the updated note
        note.save()

        # Serialize the updated note and return the response
        serializer = NoteSerializer(note)
        return Response(serializer.data, status=status.HTTP_200_OK)