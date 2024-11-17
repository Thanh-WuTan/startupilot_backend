from django.urls import path , include

urlpatterns = [
    path('startups/', include('core.api.startup.urls')),
    path('members/', include('core.api.member.urls')),
    path('avatar/', include('core.api.avatar.urls')),
    path('pitchdeck/', include('core.api.pitchdeck.urls')),
    path('categories/', include('core.api.category.urls')),
    path('notes/', include('core.api.note.urls')),
    path('batches/', include('core.api.batch.urls')),
    path('roles/', include('core.api.role.urls')),
    path('priorities/', include('core.api.priority.urls')),
    path('statuses/', include('core.api.status.urls')),
    path('phases/', include('core.api.phase.urls')),
    path('advisors/', include('core.api.advisor.urls')),
]

