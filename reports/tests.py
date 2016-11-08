from django.test import TestCase
from reports.models import LogEntry


class Test_reports_models(TestCase):
    def test_trivial_LogEntry_creation(self):
        entry = LogEntry()
        self.assertTrue(isinstance(entry, LogEntry))
        self.assertEqual(entry.__str__(), entry.out_time + ' ' + entry.package)

    def test_str_metdod_LogEntry(self):
        entry = LogEntry(uid='testuid1', package='sample matlab package',
                         out_time='13:05:57', emp_number='123456789',
                         emp_type='xx', department='DEPT', in_time='22:10:16')
        self.assertTrue(isinstance(entry, LogEntry))
        self.assertEqual(entry.__str__(), entry.out_time + ' ' + entry.package)

    def test_save_objects_LogEntry(self):
        LogEntry.objects.all().delete()
        entry = LogEntry(uid='testuid2')
        entry.save()
        del entry
        self.assertEqual(len(LogEntry.objects.filter(uid='testuid2')), 1)
