from django.urls import path
from .api import UploadAvatarView
urlpatterns = [
    path('upload/', UploadAvatarView.as_view(), name='upload_avatar'),
    # path('update/', UpdateAvatarView.as_view(), name='update_avatar'),
    # path('delete/', DeleteAvatarView.as_view(), name='delete_avatar')
]
