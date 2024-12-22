from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from ..models import Advisor, Startup
from .serializers import AdvisorSerializer


class AdvisorCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Adjust permission classes as needed

    def post(self, request):
        data = request.data

        # Validate name field
        name = data.get('name', '').strip()
        if not name:
            return Response({'detail': 'Name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        email = data.get('email', '').strip()

        shorthand = f"{name}({email})" if email else name

        if Advisor.objects.filter(shorthand=shorthand).exists():
            return Response({'detail': f'A person with shorthand "{shorthand}" already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new Person instance
        person_data = {
            'name': name,
            'phone': data.get('phone'),
            'email': email,
            'linkedin_url': data.get('linkedin_url'),
            'facebook_url': data.get('facebook_url'),
            'area_of_expertise': data.get('area_of_expertise'),
            'avatar': data.get('avatar'),
        } 

        serializer = AdvisorSerializer(data=person_data)
        if serializer.is_valid():
            person = serializer.save()
            person.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAuthenticated]   
        return [AllowAny]

    def get(self, request, pk):
        advisor = get_object_or_404(Advisor, pk=pk)
        serializer = AdvisorSerializer(advisor)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        """
        Delete an advisor by their primary key.
        """
        advisor = get_object_or_404(Advisor, pk=pk)

        # Check if the advisor is linked to any startups
        if advisor.startups.exists():
            return Response(
                {'detail': 'Cannot delete advisor because they are linked to startups.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        advisor.delete()
        return Response({'detail': 'Advisor deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        """
        Update advisor information.
        """
        advisor = get_object_or_404(Advisor, pk=pk)
        data = request.data

        # Validate name field
        name = data.get('name', '').strip()
        if not name:
            return Response({'detail': 'Name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        email = data.get('email', '').strip()
        shorthand = f"{name}({email})" if email else name

        # Check for duplicate shorthand
        if Advisor.objects.filter(shorthand=shorthand).exclude(pk=pk).exists():
            return Response(
                {'detail': f'Another advisor with shorthand "{shorthand}" already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update the advisor instance
        advisor.name = name
        advisor.email = email
        advisor.phone = data.get('phone', advisor.phone)
        advisor.linkedin_url = data.get('linkedin_url', advisor.linkedin_url)
        advisor.facebook_url = data.get('facebook_url', advisor.facebook_url)
        advisor.area_of_expertise = data.get('area_of_expertise', advisor.area_of_expertise)
        advisor.avatar = data.get('avatar', advisor.avatar)

        advisor.save()
        serializer = AdvisorSerializer(advisor)
        return Response(serializer.data, status=status.HTTP_200_OK)
