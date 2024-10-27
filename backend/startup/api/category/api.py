from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from ...models import Category
from .serializers import CategorySerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def categories_list(request):
    categories = Category.objects.all()

    serializer = CategorySerializer(categories, many=True)
    return JsonResponse({'data': serializer.data})
