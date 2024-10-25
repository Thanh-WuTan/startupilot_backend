# from django.contrib import admin

# # Register your models here.
# from .models import Startup

# admin.site.register(Startup)


from django.contrib import admin
from .models import Startup, Category, Founder, Batch
from .forms import StartupForm

# Inline for Founder
class FounderInline(admin.TabularInline):  # You can also use admin.StackedInline for a different layout
    model = Startup.founders.through  # Use the through model for ManyToMany relations
    extra = 1  # Number of empty forms to display

# Inline for Category
class CategoryInline(admin.TabularInline):
    model = Startup.categories.through
    extra = 1

class StartupAdmin(admin.ModelAdmin):
    inlines = [FounderInline, CategoryInline]  # Include the inlines
    exclude = ('founders', 'categories')  # To prevent showing both the inlines and the many-to-many widget

    autocomplete_fields = ['batch']

admin.site.register(Startup, StartupAdmin)
admin.site.register(Category)
admin.site.register(Founder)

class BatchAdmin(admin.ModelAdmin):
    search_fields = ['name']  # Enable search by batch name

admin.site.register(Batch, BatchAdmin)
