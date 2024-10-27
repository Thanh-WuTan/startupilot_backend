from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from ...models import Batch
from .serializers import BatchSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def batch_list(request):
    batch = Batch.objects.all()

    serializer = BatchSerializer(batch, many=True)
    return JsonResponse({'data': serializer.data})
