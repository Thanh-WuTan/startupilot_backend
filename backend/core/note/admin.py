from django.contrib import admin 
from ..models import Note


class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'content_type', 'object_id', 'created_at', 'updated_at')
    search_fields = ('content',)

admin.site.register(Note, NoteAdmin)