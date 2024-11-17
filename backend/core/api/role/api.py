from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from ...models.role_model import Role
from .serializers import RoleSerializer

class RoleListView(APIView):
    """
    Retrieve a list of roles.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # Fetch all roles from the database
        roles = Role.objects.all()

        # Serialize the roles data
        serializer = RoleSerializer(roles, many=True)

        # Return the serialized data directly, without wrapping it in 'data'
        return Response(serializer.data, status=status.HTTP_200_OK)