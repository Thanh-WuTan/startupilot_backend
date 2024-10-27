from django.urls import path , include
from .api import categories_list

urlpatterns = [
    path('', categories_list, name='categories_list'),
]

