from django.urls import path , include

urlpatterns = [
    path('startups/', include('startup.api.startup.urls')),
]

