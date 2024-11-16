from django.urls import path

from .crud_api import startups_list, create_new_startup, StartupDetailView
from .export_api import export_startups


urlpatterns = [
    path('',startups_list, name='startups_list' ),
    path('<uuid:pk>/',StartupDetailView.as_view(), name='startups_detail'),
    path('create/', create_new_startup, name='create_new_startup'),
    path('export/', export_startups, name='export_startups'),
]


