from django.shortcuts import render
from .models import LogEntry


def report_view(request):
    entry_list = LogEntry.objects.all()
    return render(request, 'reports.html', context={'entry_list': entry_list})
