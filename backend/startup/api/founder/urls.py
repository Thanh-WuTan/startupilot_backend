from django.urls import path , include
from .api import founders_list

urlpatterns = [
    path('', founders_list, name='founders_list'),
]

