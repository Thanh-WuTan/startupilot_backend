from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from .serializers import MemberSerializer, ManyMemberSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny 
from ...models import Person, StartupMembership, Role, Startup, Note

class MemberListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        members = Person.objects.all()
        serializer = ManyMemberSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MemberDetailView(APIView):
    """
    Retrieve a member's information by their primary key (PK) and list the startups they are associated with,
    along with their roles in each startup, categorized as current engagements and past engagements.
    Also includes notes associated with the member.
    """
    permission_classes = [AllowAny]

    
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
        person = get_object_or_404(Person, pk=pk)
        data = request.data

        # Start a database transaction
        try:
            with transaction.atomic():
                # Update member information
                allowed_fields = ['name', 'phone', 'email', 'linkedin_url', 'facebook_url']
                member_data = data.get('member', {})
                for attr, value in member_data.items():
                    if attr in allowed_fields:
                        setattr(person, attr, value)
                person.save()

                # Helper function to get or create roles
                def get_or_create_roles(role_names):
                    roles = []
                    for role_name in role_names:
                        role, created = Role.objects.get_or_create(name=role_name)
                        roles.append(role)
                    return roles

                # Update current memberships
                current_memberships_data = data.get('current_memberships', [])
                for membership_data in current_memberships_data:
                    membership_id = membership_data.get('id')
                    roles = membership_data.get('roles', [])
                    membership_status = membership_data.get('status')

                    if membership_id:
                        membership = get_object_or_404(StartupMembership, pk=membership_id, person=person)
                        # Update roles
                        if roles:
                            membership.roles.set(get_or_create_roles(roles))
                        else:
                            membership.roles.clear()  # Clear roles if roles is empty
                        # Update status
                        if membership_status is not None:
                            membership.status = membership_status
                        membership.save()

                # Create new memberships
                new_memberships_data = data.get('new_memberships', [])
                for new_membership_data in new_memberships_data:
                    startup_name = new_membership_data.get('startup', {}).get('name')
                    roles = new_membership_data.get('roles', [])
                    membership_status = new_membership_data.get('status', True)  # Default to True if not provided

                    if startup_name:
                        # Check if the person already has a membership with the same startup
                        existing_membership = StartupMembership.objects.filter(person=person, startup__name=startup_name).first()
                        if existing_membership:
                            raise ValidationError(f"Member is already associated with the startup '{startup_name}'.")

                        startup = get_object_or_404(Startup, name=startup_name)
                        new_membership = StartupMembership.objects.create(
                            person=person,
                            startup=startup,
                            status=membership_status  # Status passed from the request
                        )
                        if roles:
                            new_membership.roles.set(get_or_create_roles(roles))
                        else:
                            new_membership.roles.clear()  # Clear roles if roles is empty
                        new_membership.save()
            return Response({'detail': 'Member information updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'An error occurred during the update.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)