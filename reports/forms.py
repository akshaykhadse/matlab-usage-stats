from django import forms
from .models import LogEntry


class DepartmentForm(forms.Form):
    """
    Class Based Form for user input to select department.

    **Attributes:**

    *department: ModelChoiceField*
        Choice field to accquire department select input from user.
        Queryset is all the distinct values for department from all the
        LogEntry model objects
    """
    department = forms.ModelChoiceField(queryset=LogEntry.objects.
                                        values_list('department', flat=True).
                                        distinct())


class TimeForm(forms.Form):
    """
    Class Based Form for user inputs to select timeframe.

    **Attributes:**

    *start_time: DateField*
        Text Field to get start time input from user for timewise graph.
        DateInput widget is used to generate the time only.

    *end_time: DateField*
        Text Field to get end time input from user for timewise graph.
        DateInput widget is used to generate the time only.
    """
    start_time = forms.DateField(widget=forms.DateInput(attrs={'class':
                                                               'timepicker'}))
    end_time = forms.DateField(widget=forms.DateInput(attrs={'class':
                                                             'timepicker'}))
