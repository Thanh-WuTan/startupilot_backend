from django.urls import path , include

urlpatterns = [
    path('startups/', include('startup.api.startup.urls')),
    path('batch/', include('startup.api.batch.urls')),
    path('categories/', include('startup.api.category.urls')),
    path('pitchdeck/', include('startup.api.pitchdeck.urls')),
    path('avatar/', include('startup.api.avatar.urls')),
]

