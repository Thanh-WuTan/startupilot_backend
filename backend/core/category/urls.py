from django.urls import path , include
from .api import CategoryListView

urlpatterns = [
    path('', CategoryListView.as_view(), name='categories_list'),
]

