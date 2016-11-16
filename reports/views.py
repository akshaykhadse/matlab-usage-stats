from django.shortcuts import render
from .models import LogEntry
import plotly.offline as opy
import plotly.graph_objs as go


def report_view(request):
    entry_list = LogEntry.objects.all()
    return render(request, 'reports.html', context={'entry_list': entry_list})


def graph_view(request):
    dept_data = {}
    data = []
    entry_list = LogEntry.objects.all()
    for entry in entry_list:
        if entry.department not in dept_data.keys():
            dept_data[entry.department] = {}
        if entry.package in dept_data[entry.department].keys():
            dept_data[entry.department][entry.package] += 1
        else:
            dept_data[entry.department][entry.package] = 1

    for dept, data_dict in dept_data.items():
        data.append(go.Bar(x=[], y=[], name=dept))
        for package, count in data_dict.items():
            data[-1]['x'].append(package)
            data[-1]['y'].append(count)

    layout = go.Layout(barmode='stack')
    fig = go.Figure(data=data, layout=layout)
    graph = opy.plot(fig, auto_open=False, output_type='div')

    return render(request, 'graphs.html', {'graph': graph})
