from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from ...models import Startup, Founder, Batch, Category
from .serializers import StartupSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def startups_list(request):
    startups = Startup.objects.all()

    # Filter
    categories_names = request.GET.getlist('categories_names', [])
    founders_names = request.GET.getlist('founders_names', [])
    batch_name = request.GET.get('batch_name', '')
    phase = request.GET.get('phase', '')
    status = request.GET.get('status', '')
    priority = request.GET.get('priority', '')

    for startup in startups:
        print(startup.name, startup.status)

    # Filtering startups based on query parameters
    if categories_names:
        startups = startups.filter(categories__name__in=categories_names).distinct()

    if founders_names:
        startups = startups.filter(founders__name__in=founders_names).distinct()

   
    if batch_name:
        # Filter startups by batch name
        startups = startups.filter(batch__name=batch_name)


    if phase:
        startups = startups.filter(phase=phase)

    if status:
        startups = startups.filter(status=status)

    if priority:
        startups = startups.filter(priority=priority)

    serializer = StartupSerializer(startups, many=True)

    return JsonResponse({
        'data': serializer.data,
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def startups_detail(request, pk):
    try:
        startup = Startup.objects.get(pk=pk)
    except Startup.DoesNotExist:
        return JsonResponse({'error': 'Startup not found'}, status=404)

    serializer = StartupSerializer(startup, many=False)
    
    return JsonResponse(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_new_startup(request):
    data = request.data.copy()  

    founders_data = data.get("founders", [])
    founder_objects = []
    for founder_info in founders_data:
        founder_name = founder_info.get("name", "")
        founder_email = founder_info.get("email", "")
        founder_shorthand = f"{founder_name} ({founder_email})" if founder_email else founder_name

        print(founder_email, founder_name, founder_shorthand)
        founder, created = Founder.objects.get_or_create(
            name=founder_name,
            email=founder_email,
            defaults={'shorthand': founder_shorthand}  # Set shorthand only when creating
        )
        print(founder.name, founder.email, founder.shorthand, created)  # Debugging output
        founder_objects.append(founder)

    # Handle categories
    categories_data = data.get("categories", [])
    category_objects = []
    for category_name in categories_data:
        category, created = Category.objects.get_or_create(name=category_name)
        category_objects.append(category)

    # Handle batch
    batch_name = data.get('batch')
    if batch_name:
        batch, created = Batch.objects.get_or_create(name=batch_name)
        data['batch'] = batch

    # Check the pitch deck file size
    pitch_deck_file = request.FILES.get('pitch_deck')
    if pitch_deck_file and pitch_deck_file.size > 1 * 1024 * 1024:  # 1 MB limit
        return Response({"error": "Pitch deck file size must be under 1MB."}, status=status.HTTP_400_BAD_REQUEST)


    data['founders'] = [founder.shorthand for founder in founder_objects]  # Only include founder names
    
    # Create the startup instance
    serializer = StartupSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    # Save the startup instance with founders and categories
    startup = serializer.save(founders=founder_objects, categories=category_objects)

    return Response(serializer.data, status=status.HTTP_201_CREATED)