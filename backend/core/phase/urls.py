from django.urls import path
from .api import PhaseListView, PhaseCreateView

urlpatterns = [
    path('', PhaseListView.as_view(), name='phase-list'),
    path('create', PhaseCreateView.as_view(), name='create-new-phase')
]   