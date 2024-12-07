from django.urls import path

from .api import NoteDetailView, NoteCreateView

urlpatterns = [
    path('<uuid:pk>', NoteDetailView.as_view(), name='note-detail'),
    path('create', NoteCreateView.as_view(), name='note-create'),
]
