import django_filters
from ..models import Startup

class MultipleValueFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass

class StartupFilter(django_filters.FilterSet):
    phase_names = MultipleValueFilter(field_name='phases__name', lookup_expr='in', distinct=True)
    category_names = MultipleValueFilter(field_name='category__name', lookup_expr='in', distinct=True)
    status_names = MultipleValueFilter(field_name='status__name', lookup_expr='in', distinct=True)
    priority_names = MultipleValueFilter(field_name='priority__name', lookup_expr='in', distinct=True)
    batch_names = MultipleValueFilter(field_name='batch__name', lookup_expr='in', distinct=True)
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', distinct=True)

    class Meta:
        model = Startup
        fields = ['phase_names', 'category_names', 'status_names', 'priority_names', 'batch_names', 'name']
