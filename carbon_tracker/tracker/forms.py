from django import forms
from .models import ActivityLog

class ActivityLogForm(forms.ModelForm):
    """
    Form for creating a new ActivityLog instance.
    """
    class Meta:
        model = ActivityLog
        fields = ['date', 'category', 'value']
        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'category': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'value': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'e.g., 10.5'}
            ),
        }