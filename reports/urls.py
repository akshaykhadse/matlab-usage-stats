from django.conf.urls import url
from .views import report_view, graph_view, departments_view, time_view

app_name = 'reports'

urlpatterns = [
    url(r'^$', report_view, name='index'),
    url(r'^list/$', report_view, name='list'),
    url(r'^graphs/$', graph_view, name='graphs'),
    url(r'^departments/$', departments_view, name='departments'),
    url(r'^time/$', time_view, name='time'),
]
