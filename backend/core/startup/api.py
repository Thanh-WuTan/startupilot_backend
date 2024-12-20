from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import StartupSerializer, ManyStartupSerializer  
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.pagination import PageNumberPagination
from openpyxl import Workbook
from io import BytesIO
from django.db import transaction
from ..models import Startup, Category, Batch, Priority, Phase, Person, Advisor, Status, Note, StartupMembership
from .serializers import StartupSerializer
from .filter import StartupFilter
from django.http import HttpResponse

import uuid

class CreateStartupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Retrieve data from the request
        data = request.data
        
        try: 
            with transaction.atomic(): 
                phase_ids = data.get('phases', [])
                phase_ids = list(set(phase_ids)) 
                phases = []
                for phase_id in phase_ids:
                    try:
                        phase = Phase.objects.get(id=phase_id)
                        phases.append(phase)
                    except Phase.DoesNotExist:
                        return Response({'error': f'Phase with id {phase_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    status_id = data.get('status')
                    status_instance = Status.objects.get(id=status_id) if status_id else None
                except Status.DoesNotExist:
                    return Response({'error': 'Status does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    priority_id = data.get('priority')
                    priority = Priority.objects.get(id=priority_id) if priority_id else None
                except Priority.DoesNotExist:
                    return Response({'error': 'Priority does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    batch_id = data.get('batch')
                    batch = Batch.objects.get(id=batch_id) if batch_id else None
                except Batch.DoesNotExist:
                    return Response({'error': 'Batch does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    category_id = data.get('category')
                    category = Category.objects.get(id=category_id) if category_id else None
                except Category.DoesNotExist:
                    return Response({'error': 'Category does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

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
                
                # Create the Startup instance using the serializer
                startup_data = {
                    'name': data.get('name'),
                    'short_description': data.get('short_description'),
                    'description': data.get('description'),
                    'email': data.get('contact_email'),
                    'linkedin_url': data.get('linkedin_url'),
                    'facebook_url': data.get('facebook_url'),
                    'pitch_deck': data.get('pitch_deck'),
                    'avatar': data.get('avatar'),
                    'status': status_instance,  
                    'priority': priority,       
                    'batch': batch,       
                    'phases': phases,           
                    'category': category,   
                    'memberships': memberships,    
                }
                
                # Use the serializer to validate and save the startup
                serializer = StartupSerializer(data=startup_data)
                
                if serializer.is_valid():
                    startup = serializer.save()  # Save the startup instance

                    # Save the memberships
                    for membership in memberships:
                        membership.startup = startup
                        membership.save()

                    startup.advisors.set(advisors)
                    
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e: 
            return Response({'error': f'Failed to create startup: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        
class StartupListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Startup.objects.all()
    serializer_class = ManyStartupSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = StartupFilter
    search_fields = ['name']
    pagination_class = PageNumberPagination
    ordering_fields = ['batch__name', 'priority__name', 'name']

class StartupDetailView(APIView):
    """
    Retrieve a startup's details by its primary key (UUID).
    """
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAuthenticated()]   
        return [AllowAny()]   

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
        
        data = request.data
        
        try:
            with transaction.atomic():
                # Update phases 
                phase_ids = data.get('phases', [])
                phase_ids = list(set(phase_ids))
                phases = []
                for phase_id in phase_ids:
                    try:
                        phase = Phase.objects.get(id=phase_id)
                        phases.append(phase)
                    except Phase.DoesNotExist:
                        return Response({'error': f'Phase with id {phase_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)    
                
                # Update status
                status_id = data.get('status')
                try:
                    status_instance = Status.objects.get(id=status_id) if status_id else None
                except Status.DoesNotExist:
                    return Response({'error': 'Status does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Update priority
                priority_id = data.get('priority')
                try:
                    priority = Priority.objects.get(id=priority_id) if priority_id else None
                except Priority.DoesNotExist:
                    return Response({'error': 'Priority does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Update batch
                batch_id = data.get('batch')
                try:
                    batch = Batch.objects.get(id=batch_id) if batch_id else None
                except Batch.DoesNotExist:
                    return Response({'error': 'Batch does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Update category
                category_id = data.get('category')
                try:
                    category = Category.objects.get(id=category_id) if category_id else None
                except Category.DoesNotExist:
                    return Response({'error': 'Category does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

                # Update memberships
                memberships_data = data.get('memberships', [])
                memberships = []
                processed_member_ids = set()

                for member_data in memberships_data:
                    member_id = member_data['id']
                    
                    if member_id in processed_member_ids:
                        return Response({'error': f'Duplicate member ID {member_id} found.'}, status=status.HTTP_400_BAD_REQUEST)

                    try:
                        member = Person.objects.get(id=member_id)
                        role = member_data.get('role')
                        member_status = member_data.get('status')
                        membership = StartupMembership(startup=startup, person=member, role=role, status=member_status)
                        memberships.append(membership)
                        processed_member_ids.add(member_id)
                    except Person.DoesNotExist:
                        return Response({'error': f'Person with id {member_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Update advisors
                mentorship_ids = data.get('mentorships', [])
                advisors = []
                processed_advisor_ids = set()

                for advisor_id in mentorship_ids:
                    if advisor_id in processed_advisor_ids:
                        return Response({'error': f'Duplicate advisor ID {advisor_id} found.'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    try:
                        advisor = Advisor.objects.get(id=advisor_id)
                        advisors.append(advisor)
                        processed_advisor_ids.add(advisor_id)
                    except Advisor.DoesNotExist:
                        return Response({'error': f'Advisor with id {advisor_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Update startup fields
                startup.name = data.get('name', startup.name)
                startup.short_description = data.get('short_description', startup.short_description)
                startup.description = data.get('description', startup.description)
                startup.email = data.get('contact_email', startup.email)
                startup.linkedin_url = data.get('linkedin_url', startup.linkedin_url)
                startup.facebook_url = data.get('facebook_url', startup.facebook_url)
                startup.pitch_deck = data.get('pitch_deck', startup.pitch_deck)
                startup.avatar = data.get('avatar', startup.avatar)
                startup.status = status_instance
                startup.priority = priority
                startup.batch = batch
                startup.category = category

                # Save the updated startup instance
                startup.save()

                # Update categories and advisors
                startup.phases.set(phases)
                startup.advisors.set(advisors)

                # Update memberships
                StartupMembership.objects.filter(startup=startup).delete()  # Clear old memberships
                for membership in memberships:
                    membership.save()
                
                serializer = StartupSerializer(startup)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f'Failed to update startup: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


class StartupExportView(APIView):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = StartupFilter
    search_fields = ['name']

    def get(self, request):
        # Apply filters
        filters = StartupFilter(request.GET, queryset=Startup.objects.all())
        if not filters.is_valid():
            return Response({"detail": "Invalid filters."}, status=400)

        # Get filtered startups
        startups = filters.qs

        # Parse 'columns' parameter
        columns_param = request.GET.get('columns', None)
        all_columns = [
            'id', 'name', 'short_description', 'description', 'email', 
            'linkedin_url', 'facebook_url', 'category', 'status', 'priority',
            'phases', 'batch', 'members', 'advisors', 'pitch_deck', 'avatar'
        ]
        columns = columns_param.split(',') if columns_param else all_columns

        # Validate columns
        invalid_columns = [col for col in columns if col not in all_columns]
        if invalid_columns:
            return Response({"detail": f"Invalid columns: {', '.join(invalid_columns)}"}, status=400)

        # Create Excel workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Startups"

        # Add headers
        ws.append(columns)

        # Add data rows
        for startup in startups:
            row = []
            for col in columns:
                # Handle special fields
                if col == 'id':
                    row.append(str(startup.id))  # Convert UUID to string
                elif col == 'category':
                    row.append(startup.category.name if startup.category else "")
                elif col == 'status':
                    row.append(startup.status.name if startup.status else "")
                elif col == 'priority':
                    row.append(startup.priority.name if startup.priority else "")
                elif col == 'phases':
                    row.append(', '.join([phase.name for phase in startup.phases.all()]))
                elif col == 'batch':
                    row.append(startup.batch.name if startup.batch else "")
                elif col == 'members':
                    row.append(', '.join([member.name for member in startup.members.all()]))
                elif col == 'advisors':
                    row.append(', '.join([advisor.name for advisor in startup.advisors.all()]))
                else:
                    value = getattr(startup, col, "")
                    row.append(value if not isinstance(value, uuid.UUID) else str(value))  # Convert UUID to string

            ws.append(row)

        # Save workbook to BytesIO
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        # Create response
        response = HttpResponse(
            buffer,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = 'attachment; filename=startups_export.xlsx'
        return response
