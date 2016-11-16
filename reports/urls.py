from django.conf.urls import url
from .views import report_view, graph_view

urlpatterns = [
    url(r'^$', report_view, name='report_view'),
    url(r'^graphs$', graph_view, name='report_view'),
]
