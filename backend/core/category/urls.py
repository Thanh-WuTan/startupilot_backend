from django.urls import path 
from .api import CategoryListView, CategoryCreateView, CategoryDetailView

urlpatterns = [
    path('', CategoryListView.as_view(), name='categories_list'),
    path('create', CategoryCreateView.as_view(), name='create_new_category'),
    path('<uuid:pk>', CategoryDetailView.as_view(), name='category-detail'),
]

