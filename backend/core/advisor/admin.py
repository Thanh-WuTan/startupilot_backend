from django.contrib import admin 
from ..models import Startup, Advisor



class AdvisorCategoryInline(admin.TabularInline):
    model = Advisor.categories.through
    extra = 1

class StartupAdvisorInline(admin.TabularInline):
    model = Startup.advisors.through  # Use the through model for the many-to-many relationship
    extra = 1  # Number of extra empty forms shown in the admin


class AdvisorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'id')
    exclude = ['categories']
    inlines = [AdvisorCategoryInline, StartupAdvisorInline] 

admin.site.register(Advisor, AdvisorAdmin)