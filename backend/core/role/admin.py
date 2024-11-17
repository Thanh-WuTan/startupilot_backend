
from django.contrib import admin
from ..models import Role

class RoleAdmin(admin.ModelAdmin):
    search_fields = ['name']  
    
admin.site.register(Role, RoleAdmin)