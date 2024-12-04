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
    permission_classes = [AllowAny]  # Adjust permission classes as needed

    def get(self, request, pk):
        advisor = get_object_or_404(Advisor, pk=pk)
        serializer = AdvisorSerializer(advisor)
        return Response(serializer.data, status=status.HTTP_200_OK)
