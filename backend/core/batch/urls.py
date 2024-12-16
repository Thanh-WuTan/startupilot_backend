from django.urls import path , include
from .api import BatchListView, BatchCreateView, BatchDetailView

urlpatterns = [
    path('', BatchListView.as_view(), name='batch_list'),
    path('create', BatchCreateView.as_view(), name='create-new-batch'),
    path('<uuid:pk>', BatchDetailView.as_view(), name='batch-detail'),
]

