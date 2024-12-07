from django.urls import path
from .api import PriorityListView, PriorityCreateView

urlpatterns = [
    path('', PriorityListView.as_view(), name='priority-list'),
    path('create', PriorityCreateView.as_view(), name='create-new-priority')
]
