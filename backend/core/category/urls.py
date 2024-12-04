from django.urls import path 
from .api import CategoryListView, CategoryCreateView

urlpatterns = [
    path('', CategoryListView.as_view(), name='categories_list'),
    path('create/', CategoryCreateView.as_view(), name='create_new_category')
]

