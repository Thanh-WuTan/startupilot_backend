from django.urls import path
from .api import upload_avatar

urlpatterns = [
    path('upload/', upload_avatar, name='upload_avatar')
]
