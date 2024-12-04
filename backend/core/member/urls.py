from django.urls import path

from .api import MemberListView, MemberDetailView, MemberCreateView

urlpatterns = [
    path('', MemberListView.as_view(), name='members-list'),
    path('<uuid:pk>', MemberDetailView.as_view(), name='member-detail'),
    path('create/', MemberCreateView.as_view(), name='member-create') 
]
