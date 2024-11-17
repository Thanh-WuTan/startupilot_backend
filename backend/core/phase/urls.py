from django.urls import path
from .api import PhaseListView

urlpatterns = [
    path('', PhaseListView.as_view(), name='status-list')
]