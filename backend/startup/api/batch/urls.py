from django.urls import path , include
from .api import batch_list

urlpatterns = [
    path('', batch_list, name='batch_list'),
]

