from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import StartupSerializer, ManyStartupSerializer 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .filter import StartupFilter
from django.db import transaction

from ..models import Startup, Category, Batch, Priority, Phase, Person, Advisor, Status, Note, StartupMembership
from .serializers import StartupSerializer

class CreateStartupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Retrieve data from the request
        data = request.data
        
        try: 
            with transaction.atomic(): 
                category_ids = data.get('categories', [])
                category_ids = list(set(category_ids)) 
                categories = []
                for category_id in category_ids:
                    try:
                        category = Category.objects.get(id=category_id)
                        categories.append(category)
                    except Category.DoesNotExist:
                        return Response({'error': f'Category with id {category_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
                
                try:
                    status_instance = Status.objects.get(id=data.get('status'))  # Renamed variable
                except Status.DoesNotExist:
                    return Response({'error': 'Status does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    priority = Priority.objects.get(id=data.get('priority'))
                except Priority.DoesNotExist:
                    return Response({'error': 'Priority does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
                 
                try:
                    batch = Batch.objects.get(id=data.get('batch'))
                except Batch.DoesNotExist:
                    return Response({'error': 'Batch does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
                 
                try:
                    phase = Phase.objects.get(id=data.get('phase'))
                except Phase.DoesNotExist:
                    return Response({'error': 'Phase does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Validate members and create StartupMembership instances
                memberships_data = data.get('memberships', [])
                memberships = []
                processed_member_ids = set()  # To track the processed member IDs

                for member_data in memberships_data:
                    member_id = member_data['id']
                    
                    if member_id in processed_member_ids:
                        return Response({'error': f'Duplicate member ID {member_id} found.'}, status=status.HTTP_400_BAD_REQUEST)

                    try:
                        member = Person.objects.get(id=member_id)
                        # Validate member role and status
                        role = member_data.get('role')
                        member_status = member_data.get('status')
                        membership = StartupMembership(startup=None, person=member, role=role, status=member_status)
                        memberships.append(membership)
                        processed_member_ids.add(member_id)  # Mark this ID as processed
                    except Person.DoesNotExist:
                        return Response({'error': f'Person with id {member_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
 
                startup = Startup(
                    name=data.get('name'),
                    short_description=data.get('short_description'),
                    description=data.get('description'),
                    email=data.get('contact_email'),
                    linkedin_url=data.get('linkedin_url'),
                    facebook_url=data.get('facebook_url'),
                    launch_date=data.get('launch_date'),
                    pitch_deck=data.get('pitch_deck'),
                    avatar=data.get('avatar'),
                    status=status_instance,  # Use the renamed variable
                    priority=priority, 
                    batch=batch,
                    phase=phase
                )
 
                startup.save()
 
                startup.categories.set(categories)
                 
                for membership in memberships:
                    membership.startup = startup
                    membership.save()
                 
                mentorship_ids = data.get('mentorships', [])
                advisors = []
                processed_advisor_ids = set()  # To track the processed advisor IDs

                for advisor_id in mentorship_ids:
                    if advisor_id in processed_advisor_ids:
                        return Response({'error': f'Duplicate advisor ID {advisor_id} found.'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    try:
                        advisor = Advisor.objects.get(id=advisor_id)
                        advisors.append(advisor)
                        processed_advisor_ids.add(advisor_id)  # Mark this advisor as processed
                    except Advisor.DoesNotExist:
                        return Response({'error': f'Advisor with id {advisor_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

                startup.advisors.set(advisors)

             
            serializer = StartupSerializer(startup)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e: 
            return Response({'error': f'Failed to create startup: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


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
        
        