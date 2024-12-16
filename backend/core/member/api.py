from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from .serializers import MemberSerializer, MemberListSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny 
from ..models import Person, StartupMembership, Startup, Note

class MemberCreateView(APIView):
    """
    API Handler for creating a new Person (Member).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        # Validate name field
        name = data.get('name', '').strip()
        if not name:
            return Response({'detail': 'Name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        email = data.get('email', '').strip()

        shorthand = f"{name}({email})" if email else name

        if Person.objects.filter(shorthand=shorthand).exists():
            return Response({'detail': f'A person with shorthand "{shorthand}" already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new Person instance
        person_data = {
            'name': name,
            'phone': data.get('phone'),
            'email': email,
            'linkedin_url': data.get('linkedin_url'),
            'facebook_url': data.get('facebook_url'),
            'avatar': data.get('avatar'),
        } 

        serializer = MemberSerializer(data=person_data)
        if serializer.is_valid():
            person = serializer.save()
            person.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MemberListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        members = Person.objects.all()
        serializer = MemberListSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MemberDetailView(APIView):
    """
    Retrieve a member's information by their primary key (PK) and list the startups they are associated with,
    along with their roles in each startup, categorized as current engagements and past engagements.
    Also includes notes associated with the member.
    """
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAuthenticated()]   
        return [AllowAny()]   

    
    def get(self, request, pk):
        person = get_object_or_404(Person, pk=pk)
        serializer = MemberSerializer(person)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """
        Delete a member and their associated startup memberships, only if the user is authenticated.
        """
        person = get_object_or_404(Person, pk=pk)
        notes = Note.objects.filter(content_type__model='person', object_id=pk)
        notes.delete()  # Delete all related notes
        person.delete()
        return Response({'detail': 'Member deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, pk):
        """
        Update a member's information.
        """
        person = get_object_or_404(Person, pk=pk)
        serializer = MemberSerializer(person, data=request.data, partial=True)

        if serializer.is_valid():
            # Ensure the updated shorthand (name + email) is unique
            name = serializer.validated_data.get('name', person.name).strip()
            email = serializer.validated_data.get('email', person.email).strip()
            shorthand = f"{name}({email})" if email else name

            if Person.objects.filter(shorthand=shorthand).exclude(pk=pk).exists():
                return Response({'detail': f'A person with shorthand "{shorthand}" already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            # Save the updated details
            serializer.save(shorthand=shorthand)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)