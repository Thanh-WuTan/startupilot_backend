from django.urls import path

from .crud_api import StartupListView, StartupDetailView 

urlpatterns = [
    path('', StartupListView.as_view(), name='startups-list'),
    path('<uuid:pk>', StartupDetailView.as_view(), name='startup-detail')
]

