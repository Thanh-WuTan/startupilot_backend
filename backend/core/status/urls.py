from django.urls import path
from .api import StatusListView

urlpatterns = [
    path('', StatusListView.as_view(), name='status-list')
]