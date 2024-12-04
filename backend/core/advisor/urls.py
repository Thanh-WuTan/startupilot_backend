from django.urls import path
from .api import AdvisorListView, AdvisorDetailView, AdvisorCreateView

urlpatterns = [
    path('', AdvisorListView.as_view(), name='advisor-list'),
    path('<uuid:pk>/', AdvisorDetailView.as_view(), name='advisor-detail'),
    path('create/', AdvisorCreateView.as_view(), name='advisor-create')
]