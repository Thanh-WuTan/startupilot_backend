from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from ...models import Founder, Startup
from .serializers import FounderSerializer, StartupSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def founders_list(request):
    founders = Founder.objects.all()

    serializer = FounderSerializer(founders, many=True)
    return JsonResponse({'data': serializer.data})
