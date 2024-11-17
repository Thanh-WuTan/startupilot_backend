from django.urls import path
from .api import PriorityListView

urlpatterns = [
    path('', PriorityListView.as_view(), name='priority-list'),
]
