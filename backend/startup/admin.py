from django.contrib import admin
from django import forms
from .models import Startup, Category, Batch, Avatar, Pitchdeck, Person, Role, StartupMembership

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

class CategoryInline(admin.TabularInline):
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

class RoleAdmin(admin.ModelAdmin):
    search_fields = ['name']  

admin.site.register(Role, RoleAdmin)

class StartupAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    exclude = ('members', 'categories')
    inlines = [CategoryInline, StartupMembershipInline] 

admin.site.register(Avatar)
admin.site.register(Person)
admin.site.register(Pitchdeck)
admin.site.register(Startup, StartupAdmin)
admin.site.register(Category)
admin.site.register(Batch)
