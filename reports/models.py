from django.db import models


class LogEntry(models.Model):
    uid = models.CharField(max_length=50)
    package = models.CharField(max_length=100)
    out_time = models.CharField(max_length=8)
    emp_number = models.CharField(max_length=100)
    emp_type = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    in_time = models.CharField(max_length=100)

    def __str__(self):
        return self.out_time + ' ' + self.package
