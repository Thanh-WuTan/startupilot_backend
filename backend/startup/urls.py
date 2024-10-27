from django.urls import path , include

urlpatterns = [
    path('startups/', include('startup.api.startup.urls')),
    path('pitchdeck/', include('startup.api.pitchdeck.urls')),
    path('avatar/', include('startup.api.avatar.urls')),
    
]

