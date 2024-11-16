from django.contrib import admin
from django import forms
from .models import Startup, Category, Batch, Avatar, Pitchdeck, Person, Role, StartupMembership, Note, Status, Priority, Phase, Advisor


class NoteInline(admin.TabularInline):  # You can use `StackedInline` for a different layout
    model = Note
    extra = 1  # Number of empty note forms displayed by default
    fields = ('content', 'created_at', 'updated_at')  # Customize fields to show in the inline form
    readonly_fields = ('created_at', 'updated_at')  # Make timestamps read-only


class StartupMembershipForm(forms.ModelForm):
    class Meta:
        model = StartupMembership
        fields = ['person', 'startup', 'roles'] 

    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        required=False,  
        widget=forms.CheckboxSelectMultiple, 
        label="Roles"
    )

class RoleInline(admin.TabularInline):
    model = StartupMembership.roles.through
    extra = 1

class StartupCategoryInline(admin.TabularInline):
    model = Startup.categories.through
    extra = 1

class MemberInline(admin.TabularInline):
    model = Startup.members.through
    extra = 1  

class StartupMembershipInline(admin.TabularInline):
    model = StartupMembership
    extra = 1
    form = StartupMembershipForm  
    inlines = [RoleInline]  

    autocomplete_fields = ['roles']

class AdvisorInline(admin.TabularInline):
    model = Startup.advisors.through
    extra = 1

class RoleAdmin(admin.ModelAdmin):
    search_fields = ['name']  

class StartupAdmin(admin.ModelAdmin):
    list_display = ('name', 'phase', 'status', 'priority', 'id')
    exclude = ('members', 'categories', 'advisors')
    inlines = [StartupCategoryInline, StartupMembershipInline, NoteInline, AdvisorInline] 


class AdvisorCategoryInline(admin.TabularInline):
    model = Advisor.categories.through
    extra = 1

class AdvisorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'id')
    exclude = ['categories']
    inlines = [AdvisorCategoryInline]

admin.site.register(Status)
admin.site.register(Phase)
admin.site.register(Priority)
admin.site.register(Batch)
admin.site.register(Note)
admin.site.register(Role, RoleAdmin)
admin.site.register(Avatar)
admin.site.register(Person)
admin.site.register(Pitchdeck)
admin.site.register(Startup, StartupAdmin)
admin.site.register(Category)
admin.site.register(Advisor, AdvisorAdmin)
