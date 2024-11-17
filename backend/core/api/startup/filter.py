from django_filters import rest_framework as filters
from django.db.models import Count

from ... models.startup_model import Startup

class StartupFilter(filters.FilterSet):
    categories__name = filters.CharFilter(method='filter_categories', distinct=True)
    status = filters.CharFilter(field_name='status__name', lookup_expr='iexact')
    phase = filters.CharFilter(field_name='phase__name', lookup_expr='iexact')
    batch = filters.CharFilter(field_name='batch__name', lookup_expr='iexact')
    priority = filters.CharFilter(field_name='priority__name', lookup_expr='iexact')
    category = filters.CharFilter(field_name='categories__name', lookup_expr='iexact')  #
    class Meta:
        model = Startup
        fields = ['phase', 'status', 'priority', 'batch', 'category']

    def filter_categories(self, queryset, name, value):
        # Get all values passed for categories__name as a list
        categories = list(set(self.request.GET.getlist('category')))
        if categories:
            # Filter startups that contain all specified categories
            return queryset.filter(
                categories__name__in=categories
            ).annotate(
                num_categories=Count('categories')
            ).filter(
                num_categories=len(categories)
            ).distinct()
        return queryset