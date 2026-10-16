from django import forms
from .models import Scholarship


class ScholarshipForm(forms.ModelForm):
    class Meta:
        model = Scholarship
        fields = ['name', 'country', 'deadline', 'coverage', 'link', 'status', 'notes']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }