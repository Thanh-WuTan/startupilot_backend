from django.urls import path , include

urlpatterns = [
    path('startups/', include('core.startup.urls')),
    path('members/', include('core.member.urls')),
    path('avatar/', include('core.avatar.urls')),
    path('pitchdeck/', include('core.pitchdeck.urls')),
    path('categories/', include('core.category.urls')),
    path('notes/', include('core.note.urls')),
    path('batches/', include('core.batch.urls')),
    path('roles/', include('core.role.urls')),
    path('priorities/', include('core.priority.urls')),
    path('statuses/', include('core.status.urls')),
    path('phases/', include('core.phase.urls')),
    path('advisors/', include('core.advisor.urls')),
]

