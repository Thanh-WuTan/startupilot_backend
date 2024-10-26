import os
import openpyxl

from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse

from .service import filter_startups, get_column_data

from ...models import Startup

@api_view(['GET'])
@permission_classes([AllowAny])
def export_startups(request):
    categories_names = request.GET.getlist('categories_names')
    batch_name = request.GET.get('batch')
    phase = request.GET.get('phase')
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    
    columns = request.GET.getlist('columns')
    default_columns = [
        'name', 'short_description', 'description', 'phase', 'status',
        'priority', 'contact_email', 'linkedin_url', 'facebook_url', 
        'categories', 'founders', 'batch'
    ]
    columns = columns or default_columns

    queryset = filter_startups(
        Startup.objects.all(),
        categories_names=categories_names,
        batch_name=batch_name,
        phase=phase,
        status=status,
        priority=priority
    )

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Startups"

    ws.append(columns)

    for startup in queryset:
        row_data = get_column_data(startup, columns)
        ws.append([row_data[col] for col in columns])

    export_path = os.path.join(settings.MEDIA_ROOT, 'export')
    os.makedirs(export_path, exist_ok=True)
    file_path = os.path.join(export_path, 'startups_export.xlsx')
    wb.save(file_path)

    response = HttpResponse(open(file_path, 'rb').read(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=startups_export.xlsx'
    
    return response
