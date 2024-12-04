from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from ..models.category_model import Category
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

class CategoryCreateView(APIView):
    """
    Create a new category.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get the 'name' from the request data
        name = ' '.join(request.data.get('name', '').strip().lower().split())

        print (name)
        if not name:
            return Response({'error': 'Category name is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a category with the same name already exists
        if Category.objects.filter(name=name).exists():
            return Response({'error': 'Category with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new category
        category = Category.objects.create(name=name)

        # Serialize the created category
        serializer = CategorySerializer(category)

        return Response(serializer.data, status=status.HTTP_201_CREATED)