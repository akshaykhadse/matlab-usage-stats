from django.test import TestCase
from reports.models import LogEntry


class Test_reports_models(TestCase):
    def test_trivial_LogEntry_creation(self):
        entry = LogEntry()
        self.assertTrue(isinstance(entry, LogEntry))

    def test_str_metdod_LogEntry(self):
        entry = LogEntry(uid='testuid1', package='sample matlab package',
                         out_time='13:05:57')
        self.assertTrue(isinstance(entry, LogEntry))
