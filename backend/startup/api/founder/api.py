from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from ...models import Founder
from .serializers import FounderSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def founder_detail(request, pk):
    try:
        founder = Founder.objects.get(pk=pk)
    except Founder.DoesNotExist:
        return JsonResponse({'error': 'Founder not found'}, status=404)

    serializer = FounderSerializer(founder)
    
    return JsonResponse(serializer.data)