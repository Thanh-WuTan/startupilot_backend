from django import forms
from .models import Startup, Founder, Category, Batch

class StartupForm(forms.ModelForm):
    class Meta:
        model = Startup
        fields = '__all__'

    # Many-to-many fields handled as multiple selections
    # categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)
    # founders = forms.ModelMultipleChoiceField(queryset=Founder.objects.all(), widget=forms.CheckboxSelectMultiple)
    batch = forms.ModelChoiceField(
        queryset=Batch.objects.all(),
        widget=forms.Select(attrs={'class': 'batch-select'})
    )

