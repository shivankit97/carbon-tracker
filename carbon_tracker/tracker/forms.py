from django import forms
from .models import ActivityLog, Goal

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


class GoalForm(forms.ModelForm):
    """
    Form for setting a user's carbon footprint goal.
    """
    class Meta:
        model = Goal
        fields = ['target_footprint']
        widgets = {
            'target_footprint': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'e.g., 1000'}
            ),
        }