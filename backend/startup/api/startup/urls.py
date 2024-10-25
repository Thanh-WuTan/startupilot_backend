from django.urls import path

from .views import startups_list, startups_detail

urlpatterns = [
    path('',startups_list, name='startups_list' ),
    path('<uuid:pk>/',startups_detail, name='startups_detail'),
]


