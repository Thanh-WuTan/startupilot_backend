from django.urls import path
from .api import AdvisorListView, AdvisorDetailView

urlpatterns = [
    path('', AdvisorListView.as_view(), name='advisor-list'),
    path('<uuid:pk>/', AdvisorDetailView.as_view(), name='advisor-detail'),
]