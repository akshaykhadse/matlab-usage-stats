from django import forms
from .models import LogEntry


class DepartmentForm(forms.Form):
    department = forms.ModelChoiceField(queryset=LogEntry.objects.
                                        values_list('department', flat=True).
                                        distinct())


class TimeForm(forms.Form):
    start_time = forms.DateField(widget=forms.DateInput(attrs={'class':
                                                               'timepicker'}))
    end_time = forms.DateField(widget=forms.DateInput(attrs={'class':
                                                             'timepicker'}))
