from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from ...models.category_model import Category
from .serializers import CategorySerializer

class CategoryListView(APIView):
    """
    Retrieve a list of categories.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # Fetch all categories from the database
        categories = Category.objects.all()

        # Serialize the categories data
        serializer = CategorySerializer(categories, many=True)

        # Return the response with the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
