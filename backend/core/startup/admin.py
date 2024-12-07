from django.contrib import admin
from django import forms
from ..models import Startup, StartupMembership, Note
from django.contrib.contenttypes.admin import GenericTabularInline


class MemberInline(admin.TabularInline):
    model = Startup.members.through
    extra = 1 

class StartupMembershipForm(forms.ModelForm):
    class Meta:
        model = StartupMembership
        fields = ['person', 'startup', 'role', 'status'] 

class StartupMembershipInline(admin.TabularInline):
    model = StartupMembership
    extra = 1
    form = StartupMembershipForm  


class AdvisorInline(admin.TabularInline):
    model = Startup.advisors.through
    extra = 1


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

class StartupPhaseInline(admin.TabularInline):
    model = Startup.phases.through
    extra = 1


class StartupAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'batch', 'priority', 'status', 'id')
    exclude = ('members',  'advisors', 'phases')
    inlines = [StartupPhaseInline, StartupMembershipInline, AdvisorInline, StartupNoteInline] 

admin.site.register(Startup, StartupAdmin)


  