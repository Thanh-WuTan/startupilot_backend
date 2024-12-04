from django.contrib import admin 
from ..models import Phase


class PhaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

admin.site.register(Phase, PhaseAdmin)