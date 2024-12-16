from django.urls import path
from .api import PhaseListView, PhaseCreateView, PhaseDetailView

urlpatterns = [
    path('', PhaseListView.as_view(), name='phase-list'),
    path('create', PhaseCreateView.as_view(), name='create-new-phase'),
    path('<uuid:pk>', PhaseDetailView.as_view(), name='phase-detail'),
]   