from django.urls import path

from .crud_api import StartupListView, StartupDetailView, CreateStartupView

urlpatterns = [
    path('', StartupListView.as_view(), name='startups-list'),
    path('<uuid:pk>', StartupDetailView.as_view(), name='startup-detail'),
    path('create/', CreateStartupView.as_view(), name='startup-create'),
]

