from django.contrib import admin
from ..models import Priority

class PriorityAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

admin.site.register(Priority, PriorityAdmin)