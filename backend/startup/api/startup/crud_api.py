from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from ...models import Startup
from .serializers import StartupSerializer
from .service import filter_startups, get_startup_by_id, create_startup


@api_view(['GET'])
@permission_classes([AllowAny])
def startups_list(request):
    startups = Startup.objects.all()
    query = request.GET.get('query', '')
    categories_names = request.GET.getlist('categories_names', [])
    categories_names = request.GET.getlist('categories_names', [])
    batch_name = request.GET.get('batch_name', '')
    phase = request.GET.get('phase', '')
    status = request.GET.get('status', '')
    priority = request.GET.get('priority', '')

    startups = filter_startups(
        query = query,
        queryset=startups,
        categories_names=categories_names,  
        batch_name=batch_name,
        phase=phase,
        status=status,
        priority=priority
    )

    serializer = StartupSerializer(startups, many=True)
    return JsonResponse({'data': serializer.data})


@api_view(['POST'])
@permission_classes([AllowAny])
def create_new_startup(request):
    """
    API endpoint to create a new Startup instance.
    """
    data = request.data.copy()
    try:
        result = create_startup(data)
    except Exception as e:
        return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    return Response(result, status=status.HTTP_201_CREATED)


class StartupDetailView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a single startup.
    """
    queryset = Startup.objects.all()
    serializer_class = StartupSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_startup_by_id(pk)

    def retrieve(self, request, *args, **kwargs):
        startup = self.get_object()
        if not startup:
            return Response({'error': 'Startup not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(startup)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        startup = self.get_object()
        if not startup:
            return Response({'error': 'Startup not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        try:
            startup.delete()
            result = create_startup(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        startup = self.get_object()
        if not startup:
            return Response({'error': 'Startup not found'}, status=status.HTTP_404_NOT_FOUND)

        startup.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)