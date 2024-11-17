from django.contrib import admin
from django import forms
from .models import Startup, Category, Batch, Avatar, Pitchdeck, Person, Role, StartupMembership, Note, Status, Priority, Phase, Advisor
from django.contrib.contenttypes.admin import GenericTabularInline

class StartupCategoryInline(admin.TabularInline):
    model = Startup.categories.through
    extra = 1

class MemberInline(admin.TabularInline):
    model = Startup.members.through
    extra = 1 

class StartupMembershipForm(forms.ModelForm):
    class Meta:
        model = StartupMembership
        fields = ['person', 'startup', 'roles', 'status'] 

    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        required=False,  
        widget=forms.CheckboxSelectMultiple, 
        label="Roles"
    )

class RoleInline(admin.TabularInline):
    model = StartupMembership.roles.through
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

class StartupNoteInline(GenericTabularInline):
    model = Note
    extra = 1  # The number of empty forms to show
    fields = ('content', 'created_at', 'updated_at')  # Fields you want to show
    readonly_fields = ('created_at', 'updated_at')  # Make these fields read-only
    fk_name = 'content_object'  # Ensure this is linked to the generic FK

    # Filter notes to only show those related to the specific startup
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(content_type__model='startup') 


class StartupAdmin(admin.ModelAdmin):
    list_display = ('name', 'phase', 'status', 'priority', 'id')
    exclude = ('members', 'categories', 'advisors')
    inlines = [StartupCategoryInline, StartupMembershipInline, AdvisorInline, StartupNoteInline] 


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

class PersonMembershipInline(admin.TabularInline):
    model = StartupMembership
    form = StartupMembershipForm
    extra = 1
    show_change_link = True 

class MemberNoteInline(GenericTabularInline):
    model = Note
    extra = 1
    fields = ('content', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        # Filter to only show notes related to Person (members)
        return Note.objects.filter(content_type__model='person')

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'id')
    inlines = [PersonMembershipInline, MemberNoteInline]

class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'content_type', 'object_id', 'created_at', 'updated_at')
    search_fields = ('content',)
 
admin.site.register(Note, NoteAdmin)
admin.site.register(Status)
admin.site.register(Phase)
admin.site.register(Priority)
admin.site.register(Batch) 
admin.site.register(Role, RoleAdmin)
admin.site.register(Avatar)
admin.site.register(Person, PersonAdmin)
admin.site.register(Pitchdeck)
admin.site.register(Startup, StartupAdmin)
admin.site.register(Category)
admin.site.register(Advisor, AdvisorAdmin)
admin.site.register(StartupMembership)
