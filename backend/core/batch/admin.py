from django.contrib import admin
from ..models import Batch

class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
admin.site.register(Batch, BatchAdmin)