from django.urls import path , include
from .api import BatchListView, BatchCreateView

urlpatterns = [
    path('', BatchListView.as_view(), name='batch_list'),
    path('create/', BatchCreateView.as_view(), name='create-new-batch')
]

