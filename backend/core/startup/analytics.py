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

        # Aggregating category-wise data
        categories = Category.objects.annotate(
            count=Count('startups', filter=Q(startups__in=queryset))
        )
        categories_count = {}
        for category in categories:
            categories_count[category.name] = {
                'count': category.count,
            }

        # Aggregating dynamic status data
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

                category_priority_data = {}
                for priority in priorities:
                    category_priority_data[priority.name] = queryset.filter(
                        batch=batch, category=category, priority=priority
                    ).count()

                batch_data[category.name] = {
                    'status': category_status_data,
                    'priority': category_priority_data,
                }

            batch_data['Total'] = {
                category.name: queryset.filter(batch=batch, category=category).count()
                for category in categories
            }
            batches_count[batch.name] = batch_data

        # Aggregating phase-wise data
        phases = Phase.objects.all()
        phases_count = {}
        for batch in batches:
            phase_data = {}
            for phase in phases:
                phase_status_data = {}
                for status in statuses:
                    phase_status_data[status.name] = queryset.filter(
                        batch=batch, phases=phase, status=status
                    ).count()
                phase_data[phase.name] = {
                    'status': phase_status_data,
                    'count': queryset.filter(batch=batch, phases=phase).count()
                }
            phases_count[batch.name] = phase_data

        phase_data = {}
        for phase in phases:
            phase_status_data = {}
            for status in statuses:
                phase_status_data[status.name] = queryset.filter(
                    phases=phase, status=status
                ).count()
            phase_data[phase.name] = {
                'status': phase_status_data,
                'count': queryset.filter(phases=phase).count()
            }
        phases_count['Total'] = phase_data

        # Final JSON structure
        startup_data = {
            'categories_count': categories_count,
            'priority_count': priority_count,
            'batches_count': batches_count,
            'phases_count': phases_count,
        }

        return Response(startup_data)
