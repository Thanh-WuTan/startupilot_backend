from django.urls import path
from .api import UploadFileView
urlpatterns = [
    path('upload/', UploadFileView.as_view(), name='upload_avatar'),
]
