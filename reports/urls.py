from django.conf.urls import url
from .views import report_view

urlpatterns = [
    url(r'^$', report_view, name='report_view'),
]
