from django.db import models


class LogEntry(models.Model):
    uid = models.CharField(max_length=50)
    package = models.CharField(max_length=100)
    out_time = models.CharField(max_length=8)
