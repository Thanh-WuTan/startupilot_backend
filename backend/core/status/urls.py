from django.urls import path
from .api import StatusListView, StatusCreateView

urlpatterns = [
    path('', StatusListView.as_view(), name='status-list'),
    path('create', StatusCreateView.as_view(), name='create_new_status'),
]