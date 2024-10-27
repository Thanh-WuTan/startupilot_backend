from django.urls import path
from .api import upload_pitchdeck

urlpatterns = [
    path('upload/', upload_pitchdeck, name='upload_pitchdeck')
]
