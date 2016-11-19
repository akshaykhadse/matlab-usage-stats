from django.db import models


class LogEntry(models.Model):
    """
    Model Class for entries to be aggregated in database. To be used by parser
    app and not by any user.

    Attributes:
    -----
    uid: CharField
        Character Field to store LDAP userid of user from logs in database.
        Maximum length is set to 50.

    package: CharField
        Character Field to store MATLAB package name from logs in database.
        Maximum length is set to 100.

    out_time: CharField
        Character Field to store timestamp for package request from license
        pool. Timestamp is of format 'HH:MM:SS'
        CharField used for simplicity as these objects will not be populated
        from forms.
        Maximum length is set to 8.

    emp_number: CharField
        Character Field to store rollnumber of user. Roll Numners are typically
        of 9 characters.
        Maximum length is set to 10.

    emp_type: CharField
        Character Field to store type of user (eg. pg, ug, rs, prjstaff etc.)
        Maximum length is set to 10.

    department: CharField
        Character Field to store department of user.
        Maximum length is set to 30.

    in_time: CharField
        Character Field to store timestamp for package return to license pool.
        Timestamp is of format 'HH:MM:SS'
        CharField used for simplicity as these objects will not be populated
        from forms.
        Maximum length is set to 8.
    """
    uid = models.CharField(max_length=50)
    package = models.CharField(max_length=100)
    out_time = models.CharField(max_length=8)
    emp_number = models.CharField(max_length=10)
    emp_type = models.CharField(max_length=10)
    department = models.CharField(max_length=30)
    in_time = models.CharField(max_length=8)

    def __str__(self):
        return self.out_time + ' ' + self.package
