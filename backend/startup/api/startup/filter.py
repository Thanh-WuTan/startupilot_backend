from django_filters import rest_framework as filters
from ... models import Startup
from django.db.models import Count

class StartupFilter(filters.FilterSet):
    categories__name = filters.CharFilter(method='filter_categories', distinct=True)

    class Meta:
        model = Startup
        fields = ['phase', 'status', 'priority', 'batch__name', 'categories__name']

    def filter_categories(self, queryset, name, value):
        # Get all values passed for categories__name as a list
        categories = list(set(self.request.GET.getlist('categories__name')))
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