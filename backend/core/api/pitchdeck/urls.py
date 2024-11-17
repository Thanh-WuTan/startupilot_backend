from django.urls import path
from .api import UploadPitchdeckView

urlpatterns = [
    path('upload-pitchdeck/', UploadPitchdeckView.as_view(), name='upload-pitchdeck'),
]