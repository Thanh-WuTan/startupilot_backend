from django.urls import path
from .api import UploadAvatarView
urlpatterns = [
    path('upload/', UploadAvatarView.as_view(), name='upload_avatar')
]
