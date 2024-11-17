from django.contrib import admin
from django import forms
from ..models import Person, Role, StartupMembership, Note
from django.contrib.contenttypes.admin import GenericTabularInline


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


admin.site.register(Person, PersonAdmin)