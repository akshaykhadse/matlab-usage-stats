from django.shortcuts import render
from .models import LogEntry
from plotly.offline import plot
from plotly.graph_objs import Bar, Layout, Figure
from .forms import DepartmentForm, TimeForm


def plot_stacked_bar_chart(query_set):
    """
    Plots stacked bar chart for given QuerySet from model using plotly offline.

    Args:
    -----
    query_set: QuerySet
        QuerySet of objects from a model in database according to filter.
        (eg. LogEntry.objects.all(), LogEntry.objects.filter(uid='some_user'))

    Returns:
    -------
    graph: String
        Returns string containing HTML div tag and javascript to generate
        graph in browser in standalone fashion.
    """
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
    """
    Function based view to generate list of all the instances of LogEntry
    model from database and format in form of table.

    Every row in this table represents activity of a user in form of
    out_time, package, userid, department, employeetype and in_time.

    This view is rendered on reports/templates/reports.html template and can
    be accessed at /reports/list/
    """
    entry_list = LogEntry.objects.all()
    return render(request, 'reports.html', context={'entry_list': entry_list})


def graph_view(request):
    """
    Function based view to generate graph with each bar as package split
    according to departments of intended users. Also, these bars include number
    of denied requests.

    This view is rendered on reports/templates/graphs.html template and can
    be accessed at /reports/graphs/
    """
    entry_list = LogEntry.objects.all()
    graph = plot_stacked_bar_chart(entry_list)
    return render(request, 'graphs.html', {'graph': graph})


def departments_view(request):
    """
    Function based view to generate graph of usage of packages of a particular
    department according user supplied input. Each bar represents a package.

    This view is responsible providing and processing DepartmentForm. Empty
    instance of DepartmentForm is provided everytime this view is accessed.
    If request.POST is not empty, graph is generated.

    This view is rendered on reports/templates/departments.html template and
    can be accessed at /reports/departments/
    """
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
    """
    Function based view to generate graph of overall usage in a partciular
    timeframe according user supplied input. Each bar represents a package
    split according number of request from each departments in given timeframe.

    This view is responsible providing and processing TimeForm. Empty instance
    of TimeForm is provided everytime this view is accessed. If request.POST is
    not empty, graph is generated.

    This view is rendered on reports/templates/time.html template and can be
    accessed at /reports/time/
    """
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
