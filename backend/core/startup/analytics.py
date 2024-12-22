from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Count, Q
from ..models import Startup, Category, Batch, Priority, Phase, Status
from .filter import StartupFilter

class StartupAnalyticsView(APIView):
    """
    View to return analytics data for startups.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # Apply the StartupFilter to dynamically filter startups based on query parameters
        queryset = StartupFilter(request.GET, queryset=Startup.objects.all()).qs

        # All categories
        categories = Category.objects.annotate(
            count=Count('startups', filter=Q(startups__in=queryset))
        )

        # All statuses
        statuses = Status.objects.all()

        # Aggregating dynamic priority data
        priorities = Priority.objects.all()
        priority_count = {}
        for priority in priorities:
            priority_data = {}
            for category in categories:
                priority_data[category.name] = queryset.filter(
                    category=category, priority=priority
                ).count()
            priority_count[priority.name] = priority_data
        priority_count['Total'] = {
            category.name: queryset.filter(priority=priority).count()
            for category in categories
        }

        # Aggregating batch-wise data
        batches = Batch.objects.all()
        batches_count = {}
        for batch in batches:
            batch_data = {}
            for category in categories:
                category_status_data = {}
                for status in statuses:
                    category_status_data[status.name] = queryset.filter(
                        batch=batch, category=category, status=status
                    ).count()

                batch_data[category.name] = category_status_data

            batch_data['Total'] = {
                status.name: queryset.filter(batch=batch, status=status).count()
                for status in statuses
            }
            batches_count[batch.name] = batch_data

        batch_data = {}
        for category in categories:
            category_status_data = {}
            for status in statuses:
                category_status_data[status.name] = queryset.filter(
                    category=category, status=status
                ).count()
            batch_data[category.name] = category_status_data
        
        batch_data['Total'] = {
            status.name: queryset.filter(status=status).count()
            for status in statuses
        }
        batches_count['Total'] = batch_data

        # Aggregating phase-wise data
        phases = Phase.objects.all()
        phases_count = {}
        for batch in batches:
            phase_data = {}
            for phase in phases:
                phase_data[phase.name] = {
                    'count': queryset.filter(batch=batch, phases=phase).count()
                }
            phases_count[batch.name] = phase_data

        phase_data = {}
        for phase in phases:
            phase_data[phase.name] = {
                'count': queryset.filter(phases=phase).count()
            }
        phases_count['Total'] = phase_data

        # Final JSON structure
        startup_data = {
            'priority_count': priority_count,
            'batches_count': batches_count,
            'phases_count': phases_count,
        }

        return Response(startup_data)
