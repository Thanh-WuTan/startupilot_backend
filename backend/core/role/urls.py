from django.urls import path
from .api import RoleListView

urlpatterns = [
    path('', RoleListView.as_view(), name='role-list'),
]
