from django.contrib import admin
from ..models import Category



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

admin.site.register(Category, CategoryAdmin)