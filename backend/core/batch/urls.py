from django.urls import path , include
from .api import BatchListView

urlpatterns = [
    path('', BatchListView.as_view(), name='batch_list'),
]

