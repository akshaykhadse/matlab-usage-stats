from django.test import TestCase
from reports.models import LogEntry
from django.test.utils import setup_test_environment
from django.test import Client
setup_test_environment()


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


class Test_reports_report_view(TestCase):
    def setUp(self):
        entry = LogEntry(uid='testuid1', package='some matlab package',
                         out_time='22:22:22', emp_number='123456789',
                         department='DEPT', emp_type='xx', in_time='23:23:23')
        entry.save()

    def tearDown(self):
        LogEntry.objects.all().delete()

    def test_report_view_status(self):
        c = Client()
        response = c.get('/reports/')
        self.assertEqual(response.status_code, 200)

    def test_report_view_context(self):
        c = Client()
        response = c.get('/reports/')
        self.assertEqual(len(response.context['entry_list']), 1)

    def test_report_view_content(self):
        c = Client()
        response = c.get('/reports/')
        self.assertIn('testuid1', str(response.content))
        self.assertIn('some matlab package', str(response.content))
        self.assertIn('DEPT', str(response.content))
