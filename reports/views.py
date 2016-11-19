from django.shortcuts import render
from .models import LogEntry
from plotly.offline import plot
from plotly.graph_objs import Bar, Layout, Figure
from .forms import DepartmentForm, TimeForm


def plot_stacked_bar_chart(query_set):
    dept_data = {}
    data = []
    for entry in query_set:
        if entry.department not in dept_data.keys():
            dept_data[entry.department] = {}
        if entry.package in dept_data[entry.department].keys():
            dept_data[entry.department][entry.package] += 1
        else:
            dept_data[entry.department][entry.package] = 1

    for dept, data_dict in dept_data.items():
        data.append(Bar(x=[], y=[], name=dept))
        for package, count in data_dict.items():
            data[-1]['x'].append(package)
            data[-1]['y'].append(count)
    layout = Layout(barmode='stack')
    fig = Figure(data=data, layout=layout)
    graph = plot(fig, auto_open=False, output_type='div')
    return graph


def report_view(request):
    entry_list = LogEntry.objects.all()
    return render(request, 'reports.html', context={'entry_list': entry_list})


def graph_view(request):
    entry_list = LogEntry.objects.all()
    graph = plot_stacked_bar_chart(entry_list)
    return render(request, 'graphs.html', {'graph': graph})


def departments_view(request):
    if request.method == 'POST':
        dept = request.POST.get('department')
        form = DepartmentForm()
        x = []
        y = []
        for entry in LogEntry.objects.filter(department=dept):
            if entry.package in x:
                y[x.index(entry.package)] += 1
            else:
                x.append(entry.package)
                y.append(1)
            data = [Bar(x=x, y=y)]
            fig = Figure(data=data)
            graph = plot(fig, auto_open=False, output_type='div')
        return render(request, 'departments.html', {'form': form,
                                                    'department': dept,
                                                    'graph': graph})
    else:
        form = DepartmentForm()
    return render(request, 'departments.html', {'form': form})


def time_view(request):
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        form = TimeForm()

        entry_list = LogEntry.objects.filter(out_time__gte=start_time,
                                             out_time__lte=end_time)
        if len(entry_list) == 0:
            return render(request, 'time.html', {'form': form,
                                                 'message': 'No Activity'})
        else:
            graph = plot_stacked_bar_chart(entry_list)
        return render(request, 'time.html', {'form': form, 'graph': graph,
                                             'start_time': start_time,
                                             'end_time': end_time})
    else:
        form = TimeForm()
    return render(request, 'time.html', {'form': form})
