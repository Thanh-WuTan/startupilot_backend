from django.db.models import Count, Q
from ...models import Startup, Founder, Batch, Category, Avatar, Pitchdeck
from django.core.exceptions import ObjectDoesNotExist

from .serializers import StartupSerializer
from ..avatar.service import get_avatar_by_url
from ..pitchdeck.service import get_pitchdeck_by_url

def get_startup_by_id(pk):
    """
    Retrieve a Startup instance by its primary key.
    
    Args:
        pk (UUID): The primary key of the Startup instance.
    
    Returns:
        Startup: The retrieved Startup instance or None if not found.
    """
    try:
        return Startup.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return None

def filter_startups(queryset,
    categories_names=None, 
    batch_name=None,
    phase=None,
    status=None,
    priority=None
):
    """
    Filters startups based on the provided parameters.
    """
    if categories_names: 
        queryset = queryset.filter(categories__name__in=categories_names) \
                           .annotate(num_categories=Count('categories', filter=Q(categories__name__in=categories_names))) \
                           .filter(num_categories=len(categories_names))
        
    if batch_name:
        queryset = queryset.filter(batch__name=batch_name)

    if phase:
        queryset = queryset.filter(phase=phase)

    if status:
        queryset = queryset.filter(status=status)

    if priority:
        queryset = queryset.filter(priority=priority)

    return queryset

def get_column_data(startup, columns):
    """
    Collects data for specified columns.
    """
    data = {}
    for column in columns:
        if column == "categories":
            data[column] = ", ".join([c.name for c in startup.categories.all()])
        elif column == "founders":
            data[column] = ", ".join([f.name for f in startup.founders.all()])
        elif column == "batch":
            data[column] = startup.batch.name if startup.batch else ""
        else:
            data[column] = getattr(startup, column, "")
    return data

def create_startup(data):
    """
    Create a new Startup instance based on the provided data.
    """
    # Handle founders
    founders_data = data.get("founders", [])
    founder_objects = []
    for founder_info in founders_data:
        founder_name = founder_info.get("name", "")
        founder_email = founder_info.get("email", "")
        founder_shorthand = f"{founder_name} ({founder_email})" if founder_email else founder_name

        founder, created = Founder.objects.get_or_create(
            name=founder_name,
            email=founder_email,
            defaults={'shorthand': founder_shorthand}  # Set shorthand only when creating
        ) 
        founder_objects.append(founder)
    data['founders'] = [founder.shorthand for founder in founder_objects]  # Only include founder shorthands

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


    # Handle avatar:
    avatar_url = data.pop("avatar", "/media/avatar/default_9kV34NX.png")
    avatar = get_avatar_by_url(avatar_url)

    # Handle pitchdeck
    pitchdeck_url = data.pop("pitch_deck", None)
    pitch_deck = get_pitchdeck_by_url(pitchdeck_url) if pitchdeck_url else None

    # Prepare data for the serializer
    data['avatar'] = avatar.name if avatar else ""
    data['pitch_deck'] = pitch_deck.name if pitch_deck else ""
    data['batch'] = batch.name if batch else ""

    # Serialize and save the Startup instance
    serializer = StartupSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    startup = serializer.save(founders=founder_objects, categories=category_objects)

    return serializer.data